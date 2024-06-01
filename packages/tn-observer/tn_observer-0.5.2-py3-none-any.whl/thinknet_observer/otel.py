
import os

from urllib.parse import urlparse

from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, BatchSpanProcessor, ConsoleSpanExporter

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from opentelemetry.instrumentation.kafka import KafkaInstrumentor

from opentelemetry.semconv.trace import SpanAttributes

from .metrics.metrics import PrometheusMiddleware


DEBUG_LOG_OTEL_TO_PROVIDER = False
DISABLE_TRACE = (os.getenv("OTEL_DISABLE_TRACE", False) == True)
DEFAULT_EXCLUDED_ROUTES = "metric,healthy,healthz,readyz,livez,startz,favicon.ico"
ENV_EXCLUDED_URLS = os.getenv("OTEL_PYTHON_EXCLUDED_URLS", "")


class TNObserver:

    def __init__(self, service_name, service_version=None):
        self.resource = TNObserver.setup_resource(service_name, service_version)


    @classmethod
    def with_default_service_info(cls):
        service_name = TNObserver.get_service_name()
        service_version = os.getenv("APP_VERSION")
        return cls(service_name, service_version)
        

    @staticmethod
    def get_service_name():
        prefix = os.getenv("SERVICE_NAME_PREFIX", None)
        name = os.getenv("SERVICE_NAME", "")

        if prefix:
            return f"{prefix}/{name}"
        return name


    @property
    def resources(self,) -> Resource:
        return self.resource


    @staticmethod
    def setup_resource(service_name: str, service_version: str):
        resource =  Resource.create({
            "service.name": service_name,
            "service.version": service_version if service_version else "1.0.0"
        })
        return resource
    


    @staticmethod
    def setup_trace(name, resource=None):

        trace_provider = TracerProvider(resource=resource)

        if not DISABLE_TRACE:
            if DEBUG_LOG_OTEL_TO_PROVIDER :
                trace_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
            else:
                otel_endpoint_url = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
                # otlp_span_exporter = OTLPSpanExporter(endpoint=otel_endpoint_url,headers=otel_http_headers)
                otlp_span_exporter = OTLPSpanExporter(endpoint=otel_endpoint_url)
                trace_provider.add_span_processor(BatchSpanProcessor(otlp_span_exporter))

            trace.set_tracer_provider(trace_provider)
            tracer = trace.get_tracer(name)

            return tracer
        
        return None


    @staticmethod
    def setup_metrics(name, resource=None):
        # print (DEBUG_LOG_OTEL_TO_PROVIDER)
        if DEBUG_LOG_OTEL_TO_PROVIDER :
            metric_provider = MeterProvider(
                metric_readers=[PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=5000)],
                resource=resource
                )
        else:
            otel_endpoint_url = os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', "http://localhost:4317")
            metric_provider = MeterProvider(
                metric_readers=[PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=otel_endpoint_url), export_interval_millis=50000)],
                resource=resource
                )

        metrics.set_meter_provider(metric_provider)
        meter = metrics.get_meter(name)
        return meter
    

    @staticmethod
    def _str_exclude_urls(excluded_urls):

        str_excludes_routes = DEFAULT_EXCLUDED_ROUTES
        if ENV_EXCLUDED_URLS != "":
            str_excludes_routes += f",{ENV_EXCLUDED_URLS}"
            
        if isinstance(excluded_urls, list):
            temp_urls = []
            for url in excluded_urls:
                if isinstance(url, dict) and "route" in url:
                    url = url["route"][1:] if url["route"][0] == "/" else url["route"]
                    temp_urls.append(url)
                elif isinstance(url, str):
                    url = url [1:] if url[0] == "/" else url
                    temp_urls.append(url)

            str_urls = ",".join(temp_urls)
            return str_excludes_routes + "," + str_urls
        elif isinstance(excluded_urls, str):
            return str_excludes_routes + "," + excluded_urls
        else:
            return str_excludes_routes
    

    @staticmethod
    def _requests_request_hook(span: trace.Span, req):
        url = req.url
        o = urlparse(url)
        if span and span.is_recording():
            span.update_name(f"{req.method} {o.path}")
            span.set_attribute(SpanAttributes.HTTP_ROUTE, o.path)
        

    @staticmethod
    def flask_instrumentation(app, excluded_urls=None):
        excluded_urls = TNObserver._str_exclude_urls(excluded_urls)
        return FlaskInstrumentor().instrument_app(app, excluded_urls=excluded_urls)
    
    
    @staticmethod
    def fast_instrumentation(app, excluded_urls=None):
        excluded_urls = TNObserver._str_exclude_urls(excluded_urls)
        return FastAPIInstrumentor().instrument_app(app, excluded_urls=excluded_urls)
    
    
    @staticmethod
    def pymongo_instrumentation():
        return PymongoInstrumentor().instrument()
    

    @staticmethod
    def requests_instrumentation():
        return RequestsInstrumentor().instrument(request_hook=TNObserver._requests_request_hook)
    

    @staticmethod
    def kafka_instrumentation():
        return KafkaInstrumentor().instrument()
    

    @staticmethod
    def _list_str_exclude_urls(str_exclude):
        return [{"route": f"/{url}"} for url in str_exclude.split(",")]
    

    @staticmethod
    def _list_exclude_urls(excluded_urls):
        list_excluded_route = []

        list_excluded_route.extend(TNObserver._list_str_exclude_urls(DEFAULT_EXCLUDED_ROUTES))
        list_excluded_route.extend(TNObserver._list_str_exclude_urls(ENV_EXCLUDED_URLS))

        if isinstance(excluded_urls, str):
            list_excluded_route.extend(TNObserver._list_str_exclude_urls(excluded_urls))

        if isinstance(excluded_urls, list):
            for url in excluded_urls:
                if isinstance(url, str):
                    list_excluded_route.append({"route": f"/{url}"})
                elif isinstance(url, dict):
                    url['route'] = f"/{url['route']}" if url['route'][0] != "/" else url['route']
                    list_excluded_route.append(url)
                    
        return list_excluded_route
    

    @staticmethod
    def register_metrics(app, is_multiprocessing: bool=False, excluded_urls:list=[]):
        prom_middleware = PrometheusMiddleware(app, is_multiprocessing=is_multiprocessing)
        list_exclude = TNObserver._list_exclude_urls(excluded_urls)
        prom_middleware.add_exclude(list_exclude)
        prom_middleware.register_metrics()
    
