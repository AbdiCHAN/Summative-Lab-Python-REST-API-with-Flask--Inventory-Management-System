import pytest
import json
from app import create_app
from models.inventory_model import Product

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            Product.query.delete()
            db = Product.__table__.create(bind=Product.metadata.bind)
        yield client

def test_get_all_products(client):
    res = client.get('/products')
    assert res.status_code == 200
    assert isinstance(res.json, list)

def test_get_product_by_id(client):
    product = Product(
        name="Test Product",
        category="Test",
        price=10.0,
        quantity=5,
        barcode="123456"
    )
    product.save()
    
    res = client.get(f'/products/{product.id}')
    assert res.status_code == 200
    assert res.json['name'] == "Test Product"

def test_get_product_not_found(client):
    res = client.get('/products/999')
    assert res.status_code == 404

def test_create_product(client):
    data = {
        "name": "New Product",
        "category": "Test",
        "price": 15.0,
        "quantity": 10,
        "barcode": "654321"
    }
    res = client.post('/products', json=data)
    assert res.status_code == 201
    assert res.json['name'] == "New Product"

def test_create_product_validation_error(client):
    data = {
        "category": "Test",
        "price": 15.0,
        "quantity": 10
    }
    res = client.post('/products', json=data)
    assert res.status_code == 400

def test_update_product(client):
    product = Product(
        name="Update Test",
        category="Test",
        price=20.0,
        quantity=3,
        barcode="111111"
    )
    product.save()
    
    data = {"price": 25.0}
    res = client.patch(f'/products/{product.id}', json=data)
    assert res.status_code == 200
    assert res.json['price'] == 25.0

def test_update_product_not_found(client):
    data = {"price": 25.0}
    res = client.patch('/products/999', json=data)
    assert res.status_code == 404

def test_delete_product(client):
    product = Product(
        name="Delete Test",
        category="Test",
        price=30.0,
        quantity=2,
        barcode="222222"
    )
    product.save()
    
    res = client.delete(f'/products/{product.id}')
    assert res.status_code == 200

def test_delete_product_not_found(client):
    res = client.delete('/products/999')
    assert res.status_code == 404

def test_search_products(client):
    Product(
        name="Search Test 1",
        category="Test",
        price=10.0,
        quantity=5,
        barcode="333333"
    ).save()
    
    Product(
        name="Search Test 2",
        category="Test",
        price=15.0,
        quantity=3,
        barcode="444444"
    ).save()
    
    res = client.get('/products/search?name=Search')
    assert res.status_code == 200
    assert len(res.json) == 2

def test_search_products_empty(client):
    res = client.get('/products/search?name=NonExistent')
    assert res.status_code == 200
    assert len(res.json) == 0

def test_filter_products(client):
    Product(
        name="Filter Test 1",
        category="CategoryA",
        price=10.0,
        quantity=5,
        barcode="555555"
    ).save()
    
    Product(
        name="Filter Test 2",
        category="CategoryB",
        price=15.0,
        quantity=3,
        barcode="666666"
    ).save()
    
    res = client.get('/products?category=CategoryA')
    assert res.status_code == 200
    assert len(res.json) == 1

def test_filter_products_empty(client):
    res = client.get('/products?category=NonExistent')
    assert res.status_code == 200
    assert len(res.json) == 0

def test_get_stats(client):
    Product(
        name="Stat Test 1",
        category="Test",
        price=10.0,
        quantity=5,
        barcode="777777"
    ).save()
    
    Product(
        name="Stat Test 2",
        category="Test",
        price=20.0,
        quantity=3,
        barcode="888888"
    ).save()
    
    res = client.get('/products/stats')
    assert res.status_code == 200
    assert res.json['total_products'] == 2
    assert res.json['total_quantity'] == 8
    assert res.json['total_value'] == 110.0

def test_fetch_product_from_api(client):
    res = client.get('/products/fetch/737628064502')
    assert res.status_code == 200
    assert 'name' in res.json

def test_fetch_product_not_found(client):
    res = client.get('/products/fetch/000000000000')
    assert res.status_code == 404

def test_save_fetched_product(client):
    res = client.post('/products/fetch', json={"barcode": "737628064502"})
    assert res.status_code == 201
    assert 'id' in res.json
    assert res.json['barcode'] == "737628064502"

def test_save_fetched_product_validation_error(client):
    res = client.post('/products/fetch', json={})
    assert res.status_code == 400

def test_save_fetched_product_duplicate(client):
    Product(
        name="Duplicate Test",
        category="Test",
        price=10.0,
        quantity=5,
        barcode="999999"
    ).save()
    
    res = client.post('/products/fetch', json={"barcode": "999999"})
    assert res.status_code == 400