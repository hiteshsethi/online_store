from flask import Blueprint, jsonify, request
import json
from src.app.models.user import User as UserModel
from src.app import db
from flasgger import swag_from
user_controller = Blueprint("user_controller", __name__)


@user_controller.route("/signup", methods=["POST"])
@swag_from('api_docs/signup_handler.yml')
def signup_handler():
    request_data = json.loads(request.get_data())
    entity = UserModel(
        user_name=request_data.get('user_name'),
        password=request_data.get('password'),
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify({"success": True, "data": {"message": "successfully added"}})
