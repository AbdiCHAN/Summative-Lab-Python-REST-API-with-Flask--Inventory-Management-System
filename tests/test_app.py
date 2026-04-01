from app import app

def test_get_inventory():
    client = app.test_client()
    res = client.get('/inventory')
    assert res.status_code == 200

def test_post_inventory():
    client = app.test_client()
    res = client.post('/inventory', json={"id": 1, "name": "Milk"})
    assert res.status_code == 201

def test_delete_inventory():
    client = app.test_client()
    client.post('/inventory', json={"id": 2, "name": "Eggs"})
    res = client.delete('/inventory/2')
    assert res.status_code == 200