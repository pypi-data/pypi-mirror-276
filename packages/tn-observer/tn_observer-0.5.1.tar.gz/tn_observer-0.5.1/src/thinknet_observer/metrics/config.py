import os


_DEFAULT_BUCKETS_BACKUP = [0.05, 0.1, 0.5, 0.9, 0.95]
_DEFAULT_BUCKETS = [
    0.05,
    0.1,
    0.5,
    1.0,
    1.5,
    3.0,
    5.0,
]
_DEFAULT_LABELS = ["method", "path", "status", "serviceName", "namespace"]

UNDEFINED = "UNDEFINED"

NAMESPACE = os.getenv("SERVICE_NAME_PREFIX", UNDEFINED)
SERVICENAME = os.getenv("SERVICE_NAME", UNDEFINED)
EXCLUDE_URLS = os.getenv("OTEL_PYTHON_EXCLUDED_URLS", "")
DICT_REQURIED_LABELS = {"namespace": NAMESPACE, "serviceName": SERVICENAME}
