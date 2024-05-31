# thinknet-observer-python

A library use for collect metrics, log and tracing via opentelemetry.



## Installation
```
pip install tn-observer
```


## Prerequisites
you should these enviroment in your `.env` file, 

```env
OTEL_EXPORTER_OTLP_ENDPOINT="[OTEL_ENDPOINT]"
APP_VERSION="[APP_VERSION]"
SERVICE_NAME_PREFIX="[SERVICE_NAME_PREFIX]"
SERVICE_NAME="[SERVICE_NAME]"
LOG_LEVEL="info"
OTEL_DISABLE_TRACE="False" or "True"
OTEL_PYTHON_EXCLUDED_URLS="hello,testy"

```


## Get started
1. in `main.py` or `server.py` import thinknet observer library
```python
from thinknet_observer import TNObserver
``` 

2. call setup otel 
```python
tn_observer = TNObserver.with_default_service_info()

tracer = TNObserver.setup_trace(__name__, tn_observer.resources)
meter = TNObserver.setup_metrics(__name__, tn_observer.resources)

```



### Flask Instrumentation

```python
# import library
from flask import Flask, request

from thinknet_observer import TNObserver
from thinknet_observer import FlaskLoggerMiddleware

tn_observer = TNObserver.with_default_service_info()

# create web server
app = Flask(__name__)

# trace setup
tracer = TNObserver.setup_trace(__name__, tn_observer.resources)
# metrics setup
TNObserver.register_metrics(app)
# instrument flask
TNObserver.flask_instrumentation(app)
# logging
app.wsgi_app = FlaskLoggerMiddleware(app.wsgi_app, resource=tn_observer.resources)
```

### FastAPI Instrumentation

```python
# import libraries
from fastapi import FastAPI, APIRouter

from thinknet_observer import TNObserver
from thinknet_observer import FastAPILogger

tn_observer = TNObserver.with_default_service_info()

app = FastAPI()
router = APIRouter(route_class=FastAPILogger)

TNObserver.register_metrics(app)
# instrument fastaPI
TNObserver.fast_instrumentation(app)
...

```


### pymongo instrumentation
insert the commands to `mongo.py` or file with use pymongo 
ex.

```python
from thinknet_observer import TNObserver

TNObserver.pymongo_instrumentation()
client = pymongo.MongoClient(MONGO_URI)

```

### requests instrumentation
when use lib requests to connect other services or graphQL
example

```python
import requests
from thinknet_observer import TNObserver

TNObserver.requests_instrumentation()
res = request.get(url)

```

### kafka instrumentation

```python
from thinknet_observer import TNObserver
from kafka import KafkaProducer, KafkaConsumer

TNObserver.kafka_instrumentation()

producer = KafkaProducer(bootstrap_servers=["KAFKA_HOST"])
...
```



### LOGGING

```python
from thinknet_observer import TNLogger, TNObserver

# use if service name and service version in env #
tn_observer = TNObserver.with_default_service_info()

# use if not service name and service version in env #
tn_observer = TNObserver(service_name, service_version)

logger = TNLogger("NAME", resource=tn_observer.resources)
logger.info("start consumer")

logger.info("extra attribute", extra={'a':1})

```

#### error logging

1. in file such as `error.py`

```
from thinknet_observer import TNAPIError

class DatabaseError(TNAPIError):
    http_status = 404
    message = "service can't connect database."

```
2. in controller

```
try:
    .....
except Exception as exc:
    raise DatabaseError(service_code="service can't connect database.")
```


### custom tracing

```python
from thinknet_observer import TNObserver

tracer = TNObserver.setup_trace(__name__, tn_observer.resources)

#sample function
def do_roll():
    with tracer.start_as_current_span("do_roll") as rollspan:
        res =  randint(1, 6)
        rollspan.set_attribute("roll.value", res)

```

### custom metrics

#### counter
```python
from  thinknet_observer  import  MetricCollector


CUSTOM_COUNTER = MetricCollector.counter(
    "CUSTOM_COUNTER", "desc of CUSTOM_COUNTER", ["something"]
)
CUSTOM_COUNTER_NOLABEL = MetricCollector.counter(
    "CUSTOM_COUNTER_NOLABEL", "desc of CUSTOM_COUNTER_NOLABEL"
)

# example to use count
@app.route("/count/<number>", methods=["POST"])
def count_metric(number):
    CUSTOM_COUNTER.labels("something's value").inc(float(number))
    CUSTOM_COUNTER_NOLABEL.inc(float(number))
    return {"msg": f"count {number}"}

```


#### gauge

```python
from thinknet_observer  import  MetricCollector

# NOTE: metrics name(1st param) must be unique for each metrics

# Custom gauge 
# (for gauge metrics if using multiprocess add param 'multiprocess_mode="livesum"')
CUSTOM_GAUGE = MetricCollector.gauge(
    "CUSTOM_GAUGE", "desc of CUSTOM_GAUGE", ["something"]
)
CUSTOM_GAUGE_NOLABEL = MetricCollector.gauge(
    "CUSTOM_GAUGE_NOLABEL", "desc of CUSTOM_GAUGE_NOLABEL"
)

# example to use gauge in function
@app.route("/inc_gauge/<number>", methods=["POST"])
def inc_gauge(number):
    CUSTOM_GAUGE.labels("something's value").inc(float(number))
    CUSTOM_GAUGE_NOLABEL.inc(float(number))
    return {"msg": f"inc {number}"}

@app_flask.route("/dec_gauge/<number>", methods=["POST"])
def dec_gauge(number):
    CUSTOM_GAUGE.labels("something's value").dec(float(number))
    CUSTOM_GAUGE_NOLABEL.dec(float(number))
    return {"msg": f"dec {number}"}

```

#### histogram

```python
from thinknet_observer import MetricCollector

# Custom histogram
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

# example to use histogram
@app_flask.route("/histogram_observe/<number>", methods=["POST"])
def histogram_observe(number):
    CUSTOM_HISTOGRAM.labels("something's value").observe(float(number))
    CUSTOM_HISTOGRAM_NOLABEL.observe(float(number))
    return {"msg": f"histogram_observe {number}"}

@app_flask.route("/histogram_observe2/<number>", methods=["POST"])
def histogram_observe2(number):
    CUSTOM_HISTOGRAM_NOLABEL_CUSTOMBUCKET.observe(float(number))
    return {"msg": f"histogram_observe {number}"}

```

#### summary

```python
from thinknet_observer import  MetricCollector


# Custom summary
CUSTOM_SUMMARY = MetricCollector.summary(
    "CUSTOM_SUMMARY", "desc of CUSTOM_SUMMARY", ["something"]
)
CUSTOM_SUMMARY_NOLABEL = MetricCollector.summary(
    "CUSTOM_SUMMARY_NOLABEL",
    "desc of CUSTOM_SUMMARY_NOLABEL",
)

@app_flask.route("/summary_observe/<number>", methods=["POST"])
def summary_observe(number):
    CUSTOM_SUMMARY.labels("something's value").observe(float(number))
    CUSTOM_SUMMARY_NOLABEL.observe(float(number))
    return {"msg": f"summary_observe {number}"}


```