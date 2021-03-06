import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import default_exceptions, HTTPException
import config
import exceptions
from flasgger import Swagger

import flask.json
import decimal

def init():
    from controllers import register_blueprints
    register_blueprints()
    formatter = logging.Formatter(
        "[ %(asctime)s ] [ %(levelname)s ] [%(filename)s:%(lineno)s - %(funcName)20s() ] [ %(message)s ]")
    log_file_name = config.LOGGER_PATH + '/' + "online_store_logs"
    handler = TimedRotatingFileHandler(log_file_name, 'midnight')
    handler.suffix = "%Y-%m-%d.log"
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    loggers = [app.logger, logging.getLogger("werkzeug"), logging.getLogger("app")]

    for logger in loggers:
        logger.addHandler(handler)

class JSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return float(obj)
        return super(JSONEncoder, self).default(obj)

class JSONExceptionHandler(object):
    def __init__(self, app=None):
        if app:
            self.initApp(app)

    def std_handler(self, error):
        error_code = error.code if hasattr(error, "code") else None
        response = jsonify({"success": False,
                            "error": {
                                "message": error.message if hasattr(error, "message") and error.message != "" else str(
                                    error),
                                "code": error_code if error_code is not None else 500}})
        response_status_code = 400 if error_code is not None and error_code < 4001 else 500
        if error_code and error_code < 1000:
            response_status_code = error_code
        response.status_code = response_status_code
        # response.status_code = error.code if isinstance(error, HTTPException) else 200
        return response

    def initApp(self, app):
        self.app = app
        self.register(HTTPException)
        for code, v in default_exceptions.iteritems():
            self.register(code)

    def register(self, exception_or_code, handler=None):
        self.app.errorhandler(exception_or_code)(handler or self.std_handler)


app = Flask(__name__)
app.json_encoder = JSONEncoder
exceptionHandler = JSONExceptionHandler(app)
# Configurations
app.config.from_object('config.FlaskConfig')
appLogger = app.logger

db = SQLAlchemy(app)
init()
Swagger(app)  # For Documentation
