from flask import Blueprint, request, jsonify, abort
from models.inventory_model import Product
from services.external_api_service import fetch_product

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/products', methods=['GET'])
def get_all():
    products = Product.get_all()
    return jsonify([product.to_dict() for product in products]), 200

@inventory_bp.route('/products/<int:item_id>', methods=['GET'])
def get_one(item_id):
    item = Product.get_by_id(item_id)
    return jsonify(item.to_dict()) if item else abort(404, description="Product not found")

@inventory_bp.route('/products', methods=['POST'])
def add():
    data = request.json
    errors = Product.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    product = Product(**data)
    product.save()
    return jsonify(product.to_dict()), 201

@inventory_bp.route('/products/<int:item_id>', methods=['PATCH'])
def update(item_id):
    data = request.json
    errors = Product.validate(data, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400
    item = Product.get_by_id(item_id)
    if not item:
        abort(404, description="Product not found")
    for key, value in data.items():
        setattr(item, key, value)
    item.save()
    return jsonify(item.to_dict())

@inventory_bp.route('/products/<int:item_id>', methods=['DELETE'])
def delete(item_id):
    item = Product.get_by_id(item_id)
    if not item:
        abort(404, description="Product not found")
    item.delete()
    return ("Deleted", 200)

@inventory_bp.route('/products/search', methods=['GET'])
def search():
    name = request.args.get('name', '')
    if not name:
        return jsonify({"error": "Name parameter is required"}), 400
    products = Product.search_by_name(name)
    return jsonify([product.to_dict() for product in products]), 200


@inventory_bp.route('/products/stats', methods=['GET'])
def stats():
    stats = Product.get_stats()
    return jsonify(stats), 200

@inventory_bp.route('/products/fetch/<barcode>', methods=['GET'])
def fetch(barcode):
    product = fetch_product(barcode)
    return jsonify(product) if product else abort(404, description="Product not found")

@inventory_bp.route('/products/fetch', methods=['POST'])
def save_fetched():
    data = request.json
    if not data or 'barcode' not in data:
        return jsonify({"error": "Barcode is required"}), 400
    
    barcode = data['barcode']
    product = fetch_product(barcode)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    existing = Product.get_by_id(barcode)
    if existing:
        return jsonify({"error": "Product with this barcode already exists"}), 400
    
    new_product = Product(
        name=product.get('name', ''),
        category=product.get('category', ''),
        price=product.get('price', 0.0),
        quantity=product.get('quantity', 0),
        barcode=barcode,
        brand=product.get('brand', ''),
        ingredients=product.get('ingredients', ''),
        description=product.get('description', '')
    )
    new_product.save()
    return jsonify(new_product.to_dict()), 201