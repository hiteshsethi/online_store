import logging

logger = logging.getLogger("app.controllers")

from product import product_controller
from category import category_controller
from user import user_controller
from src.app import app, db
import config
from flask import jsonify, request, render_template


def register_blueprints():
    # Register blueprint(s)
    app.register_blueprint(product_controller, url_prefix=config.API_PREFIX_V1 + "/product")
    app.register_blueprint(user_controller, url_prefix=config.API_PREFIX_V1 + "/user")
    app.register_blueprint(category_controller, url_prefix=config.API_PREFIX_V1 + "/category")


@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
    db.session.remove()


@app.route("/status")
def server_status_handler():
    return jsonify({"success": True, "data": {"running": "ok"}})


@app.errorhandler(404)
def page_not_found_handler(error):
    return jsonify({"success": False, "error": {"message": "you are at wrong place my friend!", "code": 404}}), 404


@app.before_request
def pre_request_handler():
    # Logging statement
    logger.info('\t'.join([
        request.remote_addr,
        request.method,
        request.url,
        request.data,
        ', '.join([': '.join(x) for x in request.headers])])
    )


@app.after_request
def post_request_handler(response):
    response_str = str(response.response)
    if len(response_str) >= 2000:
        response_str = response_str[:2000] + " ..Trimmed"
    logger.info('\t'.join([
        response.status,
        response_str,
        ', '.join([': '.join(x) for x in request.headers])])
    )
    return response
