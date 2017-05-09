from flask import Blueprint, jsonify, request
import json
from src.app.models.product import Product as ProductModel
from src.app import db
from src.app.exceptions import DataException
from src.app.utils import get_current_timestamp, authenticate_route
from flasgger.utils import swag_from

product_controller = Blueprint("product_controller", __name__)


@product_controller.route("/", methods=["GET"])
@authenticate_route
@swag_from('api_docs/get_products_handler.yml')
def get_products_handler():
    entities = ProductModel.query.order_by(ProductModel.name)
    db.session.commit()
    products = [e.serialize() for e in entities]
    return jsonify({"success": True, "data": products})


@product_controller.route("/<int:product_id>", methods=["GET"])
@authenticate_route
@swag_from('api_docs/get_product_handler.yml')
def get_product_handler(product_id):
    product_entity = ProductModel.query.filter_by(id=product_id).first()
    if not product_entity:
        raise DataException(msg="Product with given id doesn't exist", code=DataException.INVALID_RESOURCE_REQUESTED)
    return jsonify({"success": True, "data": product_entity.serialize()})


@product_controller.route("/add", methods=["POST"])
@authenticate_route
@swag_from('api_docs/add_product_handler.yml')
def add_product_handler():
    request_data = json.loads(request.get_data())
    entity = ProductModel(
        name=request_data.get('name'),
        description=request_data.get('description'),
        category_id=request_data.get('category_id'),
        price=request_data.get('price'),
        is_active=request_data.get('is_active'),
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify({"success": True, "data": {"message": "successfully added"}})


@product_controller.route("/update/<int:product_id>", methods=["PUT"])
@authenticate_route
@swag_from('api_docs/update_product_handler.yml')
def update_product_handler(product_id):
    product_entity = ProductModel.query.filter_by(id=product_id).first()
    if not product_entity:
        raise DataException(msg="Product with given id doesn't exist", code=DataException.INVALID_DATA_MANIPULATION)
    request_data = json.loads(request.get_data())
    product_entity.name = request_data.get('name')
    product_entity.description = request_data.get('description')
    product_entity.category_id = request_data.get('category_id')
    product_entity.price = request_data.get('price')
    product_entity.is_active = request_data.get('is_active')
    product_entity.updated_at = get_current_timestamp()
    db.session.commit()
    return jsonify({"success": True, "data": {"message": "successfully updated"}})


@product_controller.route("/delete/<int:product_id>", methods=["DELETE"])
@authenticate_route
@swag_from('api_docs/delete_product_handler.yml')
def delete_product_handler(product_id):
    product_entity = ProductModel.query.filter_by(id=product_id).first()
    if not product_entity:
        raise DataException(msg="Product with given id doesn't exist", code=DataException.INVALID_DATA_MANIPULATION)
    db.session.delete(product_entity)
    db.session.commit()
    return jsonify({"success": True, "data": {"message": "successfully deleted"}})
