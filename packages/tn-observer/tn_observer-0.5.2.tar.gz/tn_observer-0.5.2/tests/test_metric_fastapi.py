from random import random, randint
import unittest
import os
from pathlib import Path


import time
from flask import Flask
from flask_cors import CORS
from fastapi import FastAPI
from fastapi.testclient import TestClient


from src.thinknet_observer import TNObserver
from src.thinknet_observer import SingletonMeta
from src.thinknet_observer import MetricCollector

from src.thinknet_observer.metrics.config import NAMESPACE, SERVICENAME


CUSTOM_GAUGE = MetricCollector.gauge(
    "CUSTOM_GAUGE", "desc of CUSTOM_GAUGE", ["something"]
)
CUSTOM_GAUGE_NOLABEL = MetricCollector.gauge(
    "CUSTOM_GAUGE_NOLABEL", "desc of CUSTOM_GAUGE_NOLABEL"
)
CUSTOM_SUMMARY = MetricCollector.summary(
    "CUSTOM_SUMMARY", "desc of CUSTOM_SUMMARY", ["something"]
)
CUSTOM_SUMMARY_NOLABEL = MetricCollector.summary(
    "CUSTOM_SUMMARY_NOLABEL",
    "desc of CUSTOM_SUMMARY_NOLABEL",
)
CUSTOM_HISTOGRAM = MetricCollector.histogram(
    "CUSTOM_HISTOGRAM", "desc of CUSTOM_HISTOGRAM", ["something"]
)
CUSTOM_HISTOGRAM_NOLABEL = MetricCollector.histogram(
    "CUSTOM_HISTOGRAM_NOLABEL", "desc of CUSTOM_HISTOGRAM_NOLABEL"
)
CUSTOM_HISTOGRAM_NOLABEL_CUSTOMBUCKET = MetricCollector.histogram(
    "CUSTOM_HISTOGRAM_NOLABEL_CUSTOMBUCKET",
    "desc of CUSTOM_HISTOGRAM_NOLABEL_CUSTOMBUCKET",
    buckets=[0.5, 0.75, 1],
)
CUSTOM_COUNTER = MetricCollector.counter(
    "CUSTOM_COUNTER", "desc of CUSTOM_COUNTER", ["something"]
)
CUSTOM_COUNTER_NOLABEL = MetricCollector.counter(
    "CUSTOM_COUNTER_NOLABEL", "desc of CUSTOM_COUNTER_NOLABEL"
)


class PrometheusMiddlewareFastapiTestCase(unittest.TestCase):

    app_fastapi = FastAPI()

    @app_fastapi.get("/healthz")
    def health_check():
        return {"msg": "ok healthz"}

    @app_fastapi.get("/healthy")
    def healthy_check():
        return {"msg": "ok healthy"}

    @app_fastapi.get("/sleep")
    def get_sleep():
        time.sleep(1)
        return {"msg": "sleep for 1 sec"}

    @app_fastapi.post("/banana/{number}")
    def banana_number(number):
        return {"msg": f"add {number} banana"}

    @app_fastapi.post("/banana/{number}/eat")
    def eat_banana(number):
        return {"msg": f"ate {number} banana"}

    @app_fastapi.post("/inc_gauge/{number}")
    def inc_gauge(number):
        CUSTOM_GAUGE.labels("something'value").inc(float(number))
        CUSTOM_GAUGE_NOLABEL.inc(float(number))
        return {"msg": f"inc {number}"}

    @app_fastapi.post("/dec_gauge/{number}")
    def dec_gauge(number):
        CUSTOM_GAUGE.labels("something'value").dec(float(number))
        CUSTOM_GAUGE_NOLABEL.dec(float(number))
        return {"msg": f"dec {number}"}

    @app_fastapi.post("/summary_observe/{number}")
    def summary_observe(number):
        CUSTOM_SUMMARY.labels("something'value").observe(float(number))
        CUSTOM_SUMMARY_NOLABEL.observe(float(number))
        return {"msg": f"summary_observe {number}"}

    @app_fastapi.post("/histogram_observe/{number}")
    def histogram_observe(number):
        CUSTOM_HISTOGRAM.labels("something'value").observe(float(number))
        CUSTOM_HISTOGRAM_NOLABEL.observe(float(number))
        return {"msg": f"histogram_observe {number}"}

    @app_fastapi.post("/histogram_observe2/{number}")
    def histogram_observe2(number):
        CUSTOM_HISTOGRAM_NOLABEL_CUSTOMBUCKET.observe(float(number))
        return {"msg": f"histogram_observe {number}"}

    @app_fastapi.post("/count/{number}")
    def count_metric(number):
        CUSTOM_COUNTER.labels("something'value").inc(float(number))
        CUSTOM_COUNTER_NOLABEL.inc(float(number))
        return {"msg": f"count {number}"}

    def new_instance(self):
        SingletonMeta._instances = {}

    def clear_MULTIPROC_DIR(self):

        MULTIPROC_DIR = os.environ["PROMETHEUS_MULTIPROC_DIR"]
        if MULTIPROC_DIR:
            file_path = Path(MULTIPROC_DIR)
            if os.path.isdir(file_path):
                for f in os.listdir(file_path):
                    os.remove(os.path.join(file_path, f))
            else:
                os.mkdir(file_path)

    # NOTE: setUp method are called everytime before test cases.
    def setUp(self):
        self.app = self.app_fastapi
        TNObserver.register_metrics(self.app, is_multiprocessing=True)
        # self.middleware = PrometheusMiddleware(
        #     self.app_fastapi, is_multiprocessing=True
        # )
        # self.middleware.register_metrics()
        # self.middleware.clear_default_metrics()
        # self.middleware.exclude_list = self.middleware.default_exclude_list

    def tearDown(self):
        self.app = None
        self.middleware = None

    def test_client(self):
        test_client = TestClient(self.app)
        return test_client

    def test_case_001_exclude_list(self):
        """test get default exclude"""
        if (
            not isinstance(self.middleware.app, FastAPI)
            and SingletonMeta._instances is not {}
        ):
            self.new_instance()
        result = self.middleware.exclude_list
        self.assertEqual(result, [{"route": "/metrics/"}, {"route": "/metrics"}])

    def test_case_002_add_exclude(self):
        """add simple valid exclude to the middleware"""

        list_exclude = [{"route": "/first"}, {"route": "/second"}]
        self.middleware.add_exclude(list_exclude)
        result = self.middleware.exclude_list
        self.assertEqual(
            result,
            [
                {"route": "/metrics/"},
                {"route": "/metrics"},
                {"route": "/first"},
                {"route": "/second"},
            ],
        )

    def test_case_003_add_exclude(self):
        """add complex valid exclude to the middleware"""

        list_exclude = [
            {"route": "/third", "method": "get", "status_code": "200"},
            {"route": "/forth", "status_code": "400"},
        ]
        self.middleware.add_exclude(list_exclude)
        result = self.middleware.exclude_list
        self.assertEqual(
            result,
            [
                {"route": "/metrics/"},
                {"route": "/metrics"},
                {"route": "/third", "method": "get", "status_code": "200"},
                {"route": "/forth", "status_code": "400"},
            ],
        )

    def test_case_004_add_exclude(self):
        """add simple invalid exclude to the middleware"""

        list_exclude = [{"path": "/first"}, {"path": "/second"}]

        with self.assertRaises(ValueError):
            self.middleware.add_exclude(list_exclude)

    def test_case_005_add_exclude(self):
        """add simple invalid exclude to the middleware"""

        list_exclude = [{"path": "/first"}, {"path": "/second", "method": "post"}]
        with self.assertRaises(ValueError):
            self.middleware.add_exclude(list_exclude)

    def test_case_006_is_exclude(self):
        """test whether given param is exclude or not by give non-exclude param"""

        result = self.middleware.exclude_list
        self.assertEqual(result, [{"route": "/metrics/"}, {"route": "/metrics"}])
        self.assertFalse(self.middleware.is_exclude("get", "/first", "200"))

    def test_case_007_is_exclude(self):
        """test whether given param is exclude or not by give default-exclude param"""

        result = self.middleware.exclude_list
        self.assertEqual(result, [{"route": "/metrics/"}, {"route": "/metrics"}])
        self.assertTrue(self.middleware.is_exclude("get", "/metrics", "200"))

    def test_case_008_is_exclude(self):
        """test whether given param is exclude or not by give custom-exclude param"""

        result = self.middleware.exclude_list
        self.assertEqual(result, [{"route": "/metrics/"}, {"route": "/metrics"}])

        list_exclude = [
            {"route": "/first", "method": "get", "status_code": "200"},
            {"route": "/second", "status_code": "400"},
            {"status_code": "500"},
        ]
        self.middleware.add_exclude(list_exclude)
        self.assertTrue(self.middleware.is_exclude("get", "/first", "200"))
        self.assertFalse(self.middleware.is_exclude("get", "/first", "400"))
        self.assertTrue(self.middleware.is_exclude("get", "/second", "400"))
        self.assertTrue(self.middleware.is_exclude("get", "/second", "400"))
        self.assertTrue(self.middleware.is_exclude("any", "/whatever", "500"))

    def test_case_009_call_healthz(self):
        """call route /healthz and check response"""

        self.middleware.add_exclude([{"route": "/healthz"}])
        response = self.test_client().get("/healthz")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == '{"msg":"ok healthz"}')

        list_unexpected_data = [
            'http_request_duration_ht_ms_count{http_status="200",method="get",route="/healthz"} 1.0',
            'http_request_duration_summary_ms_count{http_status="200",method="get",route="/healthz"} 1.0',
            'http_request_total{http_status="200",method="get",route="/healthz"} 1.0',
        ]
        response = self.test_client().get("/metrics")
        metrics_data = str(response.text)
        self.assertTrue(
            not any(
                expected_data in metrics_data for expected_data in list_unexpected_data
            )
        )

    def test_case_010_call_healthy(self):
        """call route /healthy and check response"""

        response = self.test_client().get("/healthy")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == '{"msg":"ok healthy"}')

    def test_case_011_call_metrics(self):
        """call route /healthz and then check /metrics responses"""
        # 1st call
        response = self.test_client().get("/healthz")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == '{"msg":"ok healthz"}')

        list_expected_data_1 = [
            'http_request_duration_ms_ht_count{{http_status="200",method="get",namespace="{NAMESPACE}",route="/healthz",serviceName="{SERVICENAME}"}} 1.0'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME
            ),
            'http_request_duration_ms_summary_count{{http_status="200",method="get",namespace="{NAMESPACE}",route="/healthz",serviceName="{SERVICENAME}"}} 1.0'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME
            ),
            'http_request_total{{http_status="200",method="get",namespace="{NAMESPACE}",route="/healthz",serviceName="{SERVICENAME}"}} 1.0'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME
            ),
        ]
        response_metrics = self.test_client().get("/metrics")
        metrics_data = str(response_metrics.text)

        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            all(expected_data in metrics_data for expected_data in list_expected_data_1)
        )

        # 2nd call
        response = self.test_client().get("/healthz")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == '{"msg":"ok healthz"}')
        list_expected_data_2 = [
            'http_request_duration_ms_ht_count{{http_status="200",method="get",namespace="{NAMESPACE}",route="/healthz",serviceName="{SERVICENAME}"}} 2.0'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME
            ),
            'http_request_duration_ms_summary_count{{http_status="200",method="get",namespace="{NAMESPACE}",route="/healthz",serviceName="{SERVICENAME}"}} 2.0'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME
            ),
            'http_request_total{{http_status="200",method="get",namespace="{NAMESPACE}",route="/healthz",serviceName="{SERVICENAME}"}} 2.0'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME
            ),
        ]
        response_metrics = self.test_client().get("/metrics")
        metrics_data = str(response_metrics.text)

        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            all(expected_data in metrics_data for expected_data in list_expected_data_2)
        )

    def test_case_012_call_metrics(self):
        """call route /sleep and then check /metrics responses"""

        response = self.test_client().get("/sleep")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == '{"msg":"sleep for 1 sec"}')

        list_expected_data_1 = [
            'http_request_duration_ms_ht_count{{http_status="200",method="get",namespace="{NAMESPACE}",route="/sleep",serviceName="{SERVICENAME}"}} 1.0'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME
            ),
            'http_request_duration_ms_summary_count{{http_status="200",method="get",namespace="{NAMESPACE}",route="/sleep",serviceName="{SERVICENAME}"}} 1.0'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME
            ),
            'http_request_total{{http_status="200",method="get",namespace="{NAMESPACE}",route="/sleep",serviceName="{SERVICENAME}"}} 1.0'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME
            ),
        ]
        response_metrics = self.test_client().get("/metrics")
        metrics_data = str(response_metrics.text)
        timed_sleep = self.middleware.PROMETHEUS_REGISTRY.get_sample_value(
            "http_request_duration_ms_ht_sum",
            labels={
                "http_status": "200",
                "method": "get",
                "namespace": f"{NAMESPACE}",
                "route": "/sleep",
                "serviceName": f"{SERVICENAME}",
            },
        )

        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            all(expected_data in metrics_data for expected_data in list_expected_data_1)
        )
        self.assertTrue(1 <= timed_sleep <= 2)

    def test_case_013_call_metrics(self):
        """call dynamics routes and then check /metrics responses"""
        # 1st call
        num = randint(1, 10)
        response = self.test_client().post(f"/banana/{num}")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == f'{{"msg":"add {num} banana"}}')

        list_expected_data_1 = [
            'http_request_duration_ms_ht_count{{http_status="200",method="post",namespace="{NAMESPACE}",route="/banana/{{number}}",serviceName="{SERVICENAME}"}} 1.0'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME
            ),
            'http_request_duration_ms_summary_count{{http_status="200",method="post",namespace="{NAMESPACE}",route="/banana/{{number}}",serviceName="{SERVICENAME}"}} 1.0'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME
            ),
            'http_request_total{{http_status="200",method="post",namespace="{NAMESPACE}",route="/banana/{{number}}",serviceName="{SERVICENAME}"}} 1.0'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME
            ),
        ]
        response_metrics = self.test_client().get("/metrics")
        metrics_data = str(response_metrics.text)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            all(expected_data in metrics_data for expected_data in list_expected_data_1)
        )

        # 2nd call
        num = randint(1, 10)
        response = self.test_client().post(f"/banana/{num}/eat")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == f'{{"msg":"ate {num} banana"}}')
        list_expected_data_1 = [
            'http_request_duration_ms_ht_count{{http_status="200",method="post",namespace="{NAMESPACE}",route="/banana/{{number}}/eat",serviceName="{SERVICENAME}"}} 1.0'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME
            ),
            'http_request_duration_ms_summary_count{{http_status="200",method="post",namespace="{NAMESPACE}",route="/banana/{{number}}/eat",serviceName="{SERVICENAME}"}} 1.0'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME
            ),
            'http_request_total{{http_status="200",method="post",namespace="{NAMESPACE}",route="/banana/{{number}}/eat",serviceName="{SERVICENAME}"}} 1.0'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME
            ),
        ]
        response_metrics = self.test_client().get("/metrics")
        metrics_data = str(response_metrics.text)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            all(expected_data in metrics_data for expected_data in list_expected_data_1)
        )

    def test_case_014_call_custom_gauge_metrics(self):
        """call routes and then check /metrics responses for CUSTOM_GAUGE and CUSTOM_GAUGE_NOLABEL"""

        # 1st call
        num1 = randint(1, 10)
        response = self.test_client().post(f"/inc_gauge/{num1}")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == f'{{"msg":"inc {num1}"}}')
        list_expected_data = [
            'CUSTOM_GAUGE{{namespace="{NAMESPACE}",serviceName="{SERVICENAME}",something="something\'value"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(num1)
            ),
            'CUSTOM_GAUGE_NOLABEL{{namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(num1)
            ),
        ]
        response_metrics = self.test_client().get("/metrics")
        metrics_data = str(response_metrics.text)
        self.assertTrue(response.status_code == 200)
        # self.assertTrue(
        #     all(expected_data in metrics_data for expected_data in list_expected_data)
        # )

        # 2nd call
        num2 = randint(1, 10)
        response = self.test_client().post(f"/dec_gauge/{num2}")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == f'{{"msg":"dec {num2}"}}')
        list_expected_data = [
            'CUSTOM_GAUGE{{namespace="{NAMESPACE}",serviceName="{SERVICENAME}",something="something\'value"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(num1 - num2)
            ),
            'CUSTOM_GAUGE_NOLABEL{{namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(num1 - num2)
            ),
        ]
        response_metrics = self.test_client().get("/metrics")
        metrics_data = str(response_metrics.text)
        self.assertTrue(response.status_code == 200)
        # self.assertTrue(
        #     all(expected_data in metrics_data for expected_data in list_expected_data)
        # )

        CUSTOM_GAUGE.clear()
        CUSTOM_GAUGE_NOLABEL.clear()

    def test_case_015_call_custom_summary_metrics(self):
        """call routes and then check /metrics responses for CUSTOM_SUMMARY_NOLABEL and CUSTOM_SUMMARY_NOLABEL"""

        # 1st call
        num1 = random()
        response = self.test_client().post(f"/summary_observe/{num1}")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == f'{{"msg":"summary_observe {num1}"}}')
        list_expected_data = [
            'CUSTOM_SUMMARY_sum{{namespace="{NAMESPACE}",serviceName="{SERVICENAME}",something="something\'value"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(num1)
            ),
            'CUSTOM_SUMMARY_NOLABEL_sum{{namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(num1)
            ),
        ]
        response_metrics = self.test_client().get("/metrics")
        metrics_data = str(response_metrics.text)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            all(expected_data in metrics_data for expected_data in list_expected_data)
        )

        # 2nd call
        num2 = random()
        response = self.test_client().post(f"/summary_observe/{num2}")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == f'{{"msg":"summary_observe {num2}"}}')
        list_expected_data = [
            'CUSTOM_SUMMARY_sum{{namespace="{NAMESPACE}",serviceName="{SERVICENAME}",something="something\'value"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(num1 + num2)
            ),
            'CUSTOM_SUMMARY_NOLABEL_sum{{namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(num1 + num2)
            ),
        ]
        response_metrics = self.test_client().get("/metrics")
        metrics_data = str(response_metrics.text)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            all(expected_data in metrics_data for expected_data in list_expected_data)
        )

        CUSTOM_SUMMARY.clear()
        CUSTOM_SUMMARY_NOLABEL.clear()

    def test_case_016_call_custom_histogram_metrics(self):
        """call routes and then check /metrics responses for CUSTOM_HISTOGRAM and CUSTOM_HISTOGRAM_NOLABEL"""

        # 1st call
        num1 = 0.06
        response = self.test_client().post(f"/histogram_observe/{num1}")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == f'{{"msg":"histogram_observe {num1}"}}')
        list_expected_data = [
            'CUSTOM_HISTOGRAM_bucket{{le="0.05",namespace="{NAMESPACE}",serviceName="{SERVICENAME}",something="something\'value"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(0)
            ),
            'CUSTOM_HISTOGRAM_bucket{{le="0.1",namespace="{NAMESPACE}",serviceName="{SERVICENAME}",something="something\'value"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(1)
            ),
            'CUSTOM_HISTOGRAM_NOLABEL_bucket{{le="0.05",namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(0)
            ),
            'CUSTOM_HISTOGRAM_NOLABEL_bucket{{le="0.1",namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(1)
            ),
        ]
        response_metrics = self.test_client().get("/metrics")
        metrics_data = str(response_metrics.text)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            all(expected_data in metrics_data for expected_data in list_expected_data)
        )

        # # 2nd call
        num2 = 0.12
        response = self.test_client().post(f"/histogram_observe/{num2}")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == f'{{"msg":"histogram_observe {num2}"}}')
        list_expected_data = [
            'CUSTOM_HISTOGRAM_bucket{{le="0.05",namespace="{NAMESPACE}",serviceName="{SERVICENAME}",something="something\'value"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(0)
            ),
            'CUSTOM_HISTOGRAM_bucket{{le="0.1",namespace="{NAMESPACE}",serviceName="{SERVICENAME}",something="something\'value"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(1)
            ),
            'CUSTOM_HISTOGRAM_bucket{{le="0.5",namespace="{NAMESPACE}",serviceName="{SERVICENAME}",something="something\'value"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(2)
            ),
            'CUSTOM_HISTOGRAM_NOLABEL_bucket{{le="0.05",namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(0)
            ),
            'CUSTOM_HISTOGRAM_NOLABEL_bucket{{le="0.1",namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(1)
            ),
            'CUSTOM_HISTOGRAM_NOLABEL_bucket{{le="0.5",namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(2)
            ),
        ]
        response_metrics = self.test_client().get("/metrics")
        metrics_data = str(response_metrics.text)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            all(expected_data in metrics_data for expected_data in list_expected_data)
        )
        CUSTOM_HISTOGRAM.clear()
        CUSTOM_HISTOGRAM_NOLABEL.clear()

    def test_case_017_call_custom_counter_metrics(self):
        # 1st call
        num1 = randint(1, 10)
        response = self.test_client().post(f"/count/{num1}")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == f'{{"msg":"count {num1}"}}')
        list_expected_data = [
            'CUSTOM_COUNTER_total{{namespace="{NAMESPACE}",serviceName="{SERVICENAME}",something="something\'value"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=num1
            ),
            'CUSTOM_COUNTER_total{{namespace="{NAMESPACE}",serviceName="{SERVICENAME}",something="something\'value"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=num1
            ),
            'CUSTOM_COUNTER_NOLABEL_total{{namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=num1
            ),
            'CUSTOM_COUNTER_NOLABEL_total{{namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=num1
            ),
        ]
        response_metrics = self.test_client().get("/metrics")
        metrics_data = str(response_metrics.text)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            all(expected_data in metrics_data for expected_data in list_expected_data)
        )

        # 2nd call
        num2 = randint(1, 10)
        response = self.test_client().post(f"/count/{num2}")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == f'{{"msg":"count {num2}"}}')
        list_expected_data = [
            'CUSTOM_COUNTER_total{{namespace="{NAMESPACE}",serviceName="{SERVICENAME}",something="something\'value"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=num2 + num1
            ),
            'CUSTOM_COUNTER_total{{namespace="{NAMESPACE}",serviceName="{SERVICENAME}",something="something\'value"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=num2 + num1
            ),
            'CUSTOM_COUNTER_NOLABEL_total{{namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=num2 + num1
            ),
            'CUSTOM_COUNTER_NOLABEL_total{{namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=num2 + num1
            ),
        ]
        response_metrics = self.test_client().get("/metrics")
        metrics_data = str(response_metrics.text)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            all(expected_data in metrics_data for expected_data in list_expected_data)
        )
        CUSTOM_COUNTER.clear()
        CUSTOM_COUNTER_NOLABEL.clear()

    def test_case_018_call_custom_histogram_bucket_metrics(self):
        """call routes and then check /metrics responses for CUSTOM_HISTOGRAM_NOLABEL_CUSTOMBUCKET"""

        # 1st call
        num1 = 0.06
        response = self.test_client().post(f"/histogram_observe2/{num1}")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == f'{{"msg":"histogram_observe {num1}"}}')
        list_expected_data = [
            'CUSTOM_HISTOGRAM_NOLABEL_CUSTOMBUCKET_bucket{{le="0.5",namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(1)
            ),
            'CUSTOM_HISTOGRAM_NOLABEL_CUSTOMBUCKET_bucket{{le="0.75",namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(1)
            ),
        ]
        response_metrics = self.test_client().get("/metrics")
        metrics_data = str(response_metrics.text)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            all(expected_data in metrics_data for expected_data in list_expected_data)
        )

        # # 2nd call
        num2 = 0.8
        response = self.test_client().post(f"/histogram_observe2/{num2}")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.text == f'{{"msg":"histogram_observe {num2}"}}')
        list_expected_data = [
            'CUSTOM_HISTOGRAM_NOLABEL_CUSTOMBUCKET_bucket{{le="0.5",namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(1)
            ),
            'CUSTOM_HISTOGRAM_NOLABEL_CUSTOMBUCKET_bucket{{le="0.75",namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(1)
            ),
            'CUSTOM_HISTOGRAM_NOLABEL_CUSTOMBUCKET_bucket{{le="1.0",namespace="{NAMESPACE}",serviceName="{SERVICENAME}"}} {number}'.format(
                NAMESPACE=NAMESPACE, SERVICENAME=SERVICENAME, number=float(2)
            ),
        ]
        response_metrics = self.test_client().get("/metrics")
        metrics_data = str(response_metrics.text)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            all(expected_data in metrics_data for expected_data in list_expected_data)
        )
        CUSTOM_HISTOGRAM_NOLABEL_CUSTOMBUCKET.clear()
        self.clear_MULTIPROC_DIR()


if __name__ == "__main__":
    unittest.main()
