import time

from datetime import datetime


start_time = time.time()

def get_healthy():
    uptime_ms = (time.time() - start_time) * 1000
    response = {
        "uptime": round(uptime_ms, 2),
        "timestamp": str(datetime.now()),
        "connection": {"HTTPServer": True, "mongo": True},
    }
    status = 200

    return response


def get_healthz():
    uptime_ms = (time.time() - start_time) * 1000
    response = {
        "uptime": round(uptime_ms, 2),
        "timestamp": str(datetime.now()),
        "connection": {"HTTPServer": True},
    }
    status = 200

    return response

