from flask import Blueprint, request, jsonify
from models import inventory_model as model
from services.external_api_service import fetch_product

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory', methods=['GET'])
def get_all():
    return jsonify(model.get_all())

@inventory_bp.route('/inventory/<int:item_id>', methods=['GET'])
def get_one(item_id):
    item = model.get_one(item_id)
    return jsonify(item) if item else ("Not Found", 404)

@inventory_bp.route('/inventory', methods=['POST'])
def add():
    data = request.json
    model.add_item(data)
    return jsonify(data), 201

@inventory_bp.route('/inventory/<int:item_id>', methods=['PATCH'])
def update(item_id):
    data = request.json
    item = model.update_item(item_id, data)
    return jsonify(item) if item else ("Not Found", 404)

@inventory_bp.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete(item_id):
    model.delete_item(item_id)
    return ("Deleted", 200)

# External API
@inventory_bp.route('/fetch/<barcode>', methods=['GET'])
def fetch(barcode):
    product = fetch_product(barcode)
    return jsonify(product) if product else ("Not Found", 404)