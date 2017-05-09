from flask import Blueprint, jsonify, request
import json
from src.app.models.category import Category as CategoryModel
from src.app import db
from src.app.exceptions import DataException
from src.app.utils import get_current_timestamp, authenticate_route
from flasgger.utils import swag_from

category_controller = Blueprint("category_controller", __name__)


@category_controller.route("/", methods=["GET"])
@authenticate_route
@swag_from('api_docs/get_categories_handler.yml', validation=True)
def get_categories_handler():
    is_active_filter = request.args.get('is_active')
    query = CategoryModel.query
    if is_active_filter is not None:
        query = query.filter_by(is_active=is_active_filter)
    entities = query.order_by(CategoryModel.name)
    db.session.commit()
    categories = [e.serialize() for e in entities]
    return jsonify({"success": True, "data": categories})


@category_controller.route("/<int:category_id>", methods=["GET"])
@authenticate_route
@swag_from('api_docs/get_category_handler.yml', validation=True)
def get_category_handler(category_id):
    category_entity = CategoryModel.query.filter_by(id=category_id).first()
    if not category_entity:
        raise DataException(msg="Category with given id doesn't exist", code=DataException.INVALID_RESOURCE_REQUESTED)
    return jsonify({"success": True, "data": category_entity.serialize()})


@category_controller.route("/add", methods=["POST"])
@authenticate_route
@swag_from('api_docs/add_category_handler.yml', validation=True)
def add_category_handler():
    request_data = json.loads(request.get_data())
    entity = CategoryModel(
        name=request_data.get('name'),
        is_active=request_data.get('is_active'),
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify({"success": True, "data": {"message": "successfully added"}})


@category_controller.route("/update/<int:category_id>", methods=["PUT"])
@authenticate_route
@swag_from('api_docs/update_category_handler.yml', validation=True)
def update_category_handler(category_id):
    category_entity = CategoryModel.query.filter_by(id=category_id).first()
    if not category_entity:
        raise DataException(msg="Category with given id doesn't exist", code=DataException.INVALID_DATA_MANIPULATION)
    request_data = json.loads(request.get_data())
    category_entity.name = request_data.get('name')
    category_entity.is_active = request_data.get('is_active')
    category_entity.updated_at = get_current_timestamp()
    db.session.commit()
    return jsonify({"success": True, "data": {"message": "successfully updated"}})


@category_controller.route("/delete/<int:category_id>", methods=["DELETE"])
@authenticate_route
@swag_from('api_docs/delete_category_handler.yml', validation=True)
def delete_category_handler(category_id):
    category_entity = CategoryModel.query.filter_by(id=category_id).first()
    if not category_entity:
        raise DataException(msg="Category with given id doesn't exist", code=DataException.INVALID_DATA_MANIPULATION)
    db.session.delete(category_entity)
    db.session.commit()
    return jsonify({"success": True, "data": {"message": "successfully deleted"}})
