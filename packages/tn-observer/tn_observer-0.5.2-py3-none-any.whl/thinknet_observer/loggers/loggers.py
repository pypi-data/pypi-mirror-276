import json
import logging
import traceback
from logging import NOTSET

from time import strftime, gmtime
from typing import Union, Dict, Any

# from opentelemetry.instrumentation.logging import LoggingInstrumentor

# from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler, LogRecord
from opentelemetry.sdk._logs._internal import LogLimits
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, SimpleLogRecordProcessor, ConsoleLogExporter
from opentelemetry.sdk.resources import Resource

from opentelemetry.trace.span import TraceFlags

from ..otel import TNObserver
"""
We have options in python for stdout (streamhandling) and file logging
File logging has options for a Rotating file based on size or time (daily)
or a watched file, which supports logrotate style rotation
Most of the changes happen in the handlers, lets define a few standards
"""


_TNLogLimits = LogLimits(
    max_attributes=LogLimits.UNSET,
    max_attribute_length=LogLimits.UNSET,
)


class TNLogRecord(LogRecord):
    
    def __init__(self, timestamp: int  = None, observed_timestamp: int  = None, 
                 trace_id: int  = None, span_id: int  = None, trace_flags: TraceFlags  = None, 
                 severity_text: str  = None, severity_number: int  = None, 
                 body: Any  = None, resource: Resource  = None, 
                 attributes: Any  = None, 
                 source: str  = None,
                 limits: LogLimits  = _TNLogLimits,
                 ):
        
        super().__init__(timestamp, observed_timestamp, trace_id, span_id, trace_flags, severity_text, severity_number, body, resource, attributes, limits)
        self.source = source
        self.severity_number = severity_number


    def to_json(self, indent=4) -> str:
        otel_log = json.loads(super().to_json(indent))
        otel_resource = otel_log['resource'].replace("'", "\"")
        otel_log['source'] = self.source
        otel_log['severity_number'] = self.severity_number

        # remove prefix '0x' from super class #
        otel_log['trace_id'] = otel_log['trace_id'][2:]
        otel_log['span_id'] = otel_log['span_id'][2:]

        otel_log['resource'] = json.loads(otel_resource)
        return json.dumps(otel_log)
    


class TNLoggingHandler(LoggingHandler):
    def __init__(self, level=logging.NOTSET, logger_provider=None, source='') -> None:
        super().__init__(level, logger_provider)
        self.source = source

    def _translate(self, record: logging.LogRecord) -> LogRecord:
        
        rc = super()._translate(record)
        severity_number = record.levelno

        return TNLogRecord(timestamp=rc.timestamp, observed_timestamp=rc.observed_timestamp, trace_id=rc.trace_id,
                           span_id=rc.span_id, trace_flags=rc.trace_flags, severity_text=rc.severity_text, 
                           severity_number=severity_number,
                           body=rc.body, resource=rc.resource, source=self.source, attributes=rc.attributes)
    
    

class TNLogger(logging.Logger):

    def __init__(self, name: str=None, level=logging.NOTSET, resource: Resource = None ):

        super().__init__(name, level)

        self.resource = resource
        logger_provider = LoggerProvider(resource=self.resource)

        exporter = ConsoleLogExporter()
        logger_provider.add_log_record_processor(SimpleLogRecordProcessor(exporter))

        # self.handler = LoggingHandler(logger_provider=logger_provider)
        self.handler = TNLoggingHandler(logger_provider=logger_provider, source=name)

        super().addHandler(self.handler)

    

    @property
    def get_handlers(self,):
        return self.handler


    @classmethod
    def with_service_detail(cls, name, level):
        # resource = TNObserver.setup_resource(service_name, version)
        observer = TNObserver.with_default_service_info()
        return cls (name, level, resource=observer.resources)
    

    @staticmethod
    def set_resource(service_name, service_version):
        resource =  Resource.create({
            "service.name": service_name,
            "service.version": service_version if service_version else "1.0.0"
        })
        return resource
    


    @staticmethod
    def set_attributes(app_attribute, duration):
        time_attributes = {
            "duration": duration,
            "timestamp": strftime("%Y-%m-%dT%H:%M:%S",gmtime()),
        }
        attributes = {**app_attribute, **time_attributes}

        return attributes



class TNAPIError(Exception):

    http_status: int
    message: str

    handler_code: str = None
    service_code: str = None
    external_service_code: str = None
    payload: Union[Dict [str, str], str, None] = None
    attributes: Union[Dict [str, str], str, None] = None
    stack: str = None
    resource: Resource = None

    error_log = TNLogger("error", logging.ERROR, resource)
    

    def __init__(self, handler_code: str, service_code: str, external_service_code: str, 
                 payload: Union[Dict [str, str], str, None], attributes: Union[Dict [str, str], str, None], stack: str):
        
        self.handler_code = handler_code
        self.service_code = service_code
        self.external_service_code = external_service_code
        self.payload = payload
        self.attributes = attributes
        self.stack = stack

        self.body = {
            "httpStatus": self.http_status,
            "handlerCode": self.handler_code if self.handler_code else "",
            "serviceCode": self.service_code if self.service_code else "",
            "externalServiceCode": self.external_service_code if self.external_service_code else "",
            "message": self.message,
            "payload": self.payload if self.payload else {},
            "stack": self.stack
        }
        
        # self._logs()

    
    @property
    def errors(self):
        return {"error": self.message}
    

    @property
    def msg_body(self):
        return self.body
    

    def _logs(self,):
        
        if self.http_status == 500:
            self.error_log.error(self.body, stack_info=True, exc_info=True, extra=self.attributes)
        else:
            self.error_log.error(self.body, extra=self.attributes)
        


class NotFoundError(TNAPIError):
    http_status = 404
    message = "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again"

    def __init__(self, handler_code: str=None, service_code: str=None, external_service_code: str=None, message: str=None, 
                 payload =None, attributes=None, stack:str=None):
        
        super().__init__(handler_code, service_code, external_service_code, payload, attributes, stack=stack)



class UnExpectedError(TNAPIError):
    http_status = 500
    message = "Internal Server Error"

    def __init__(self, handler_code: str=None, service_code: str=None, external_service_code: str=None, message: str=None, 
                 payload =None, attributes=None, exc: Exception=None):
        
        trace_stack = {
                "type": type(exc).__name__,
                "message": str(exc),
                "stacktrace": traceback.format_exc()
            }
        
        # super().message = message
        super().__init__(handler_code, service_code, external_service_code, payload, attributes, stack=trace_stack)

