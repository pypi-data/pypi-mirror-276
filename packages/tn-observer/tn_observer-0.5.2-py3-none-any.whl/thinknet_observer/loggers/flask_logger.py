import os
import time
import logging


from werkzeug import Request, Response
from werkzeug.exceptions import InternalServerError, NotFound
from flask import current_app, make_response, jsonify

from .loggers import TNLogger, UnExpectedError, TNAPIError, NotFoundError


class FlaskLoggerMiddleware:

    def __init__(self, app, resource=None) -> None:
        self.app = app
        self.resource = resource

    
    def __call__(self, environ, start_response):
        
        tick = time.time()
        req = Request(environ)
        resp = Response(start_response)
        duration = time.time() - tick

        self._process_response(req, resp, duration)

        return self.app(environ, start_response)
    

    def _process_response(self, request, response, duration):

        access_logger = TNLogger("accesslog", logging.INFO, resource=self.resource)

        flask_attributes = {
            "remote_address": request.remote_addr,
            "referrer": request.referrer if request.referrer else "",
            "http.request.method": request.method,
            "http.route": request.full_path,
            "http.response.status_code": response.status_code,
            "user_agent.original": f"{request.user_agent}",
        }

        attributes = TNLogger.set_attributes(flask_attributes, duration)
        
        access_logger.info("access log", extra=attributes)




class FlaskErrorLogger:
    
    def __init__(self, app, resource=None) -> None:
        self.error_log = TNLogger("error", level=logging.ERROR, resource=resource)
        # self.init_app(app)


    def init_app(self, app):
        app.register_error_handler(404, NotFoundError)
        app.register_error_handler(500, UnExpectedError)


    def error_handler(self, exc: Exception):

        if isinstance(exc, TNAPIError):
            self._logs(exc)
            return jsonify(exc.errors), exc.http_status
        
        elif isinstance(exc, NotFound):
            obj_exc = NotFoundError()
            self._logs(obj_exc)
            return jsonify(obj_exc.errors), obj_exc.http_status
        else:
            # exc_type, exc_value, exc_tb = sys.exc_info() 
            # tb = traceback.TracebackException(exc_type, exc_value, exc_tb) 

            obj_exc = UnExpectedError("NO HANDLER ERROR", exc=exc)
            self._logs(obj_exc)

            return jsonify(obj_exc.errors), 500
        


    def _logs(self, obj_exc):

        if obj_exc.http_status == 500:
            self.error_log.error(obj_exc.msg_body, stack_info=True, exc_info=True, extra=obj_exc.attributes)
        else:
            self.error_log.error(obj_exc.msg_body, extra=obj_exc.attributes)

