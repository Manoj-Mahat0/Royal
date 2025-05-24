import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from routes.cake_router import router
from fastapi import FastAPI

# routes/test_cake_router.py


app = FastAPI()
app.include_router(router)

@pytest.fixture
def client():
    return TestClient(app)

@patch("routes.cake_router.db")
def test_accept_order_loyalty_awarded(mock_db, client):
    # Setup
    order_id = "60af924b9e7e3e6b8c8b4567"
    order = {
        "_id": order_id,
        "phone_number": "9876543210",
        "price": 500
    }
    mock_db.cake_orders.find_one.return_value = order
    mock_db.cake_orders.update_one.return_value = MagicMock()
    mock_db.users.update_one.return_value = MagicMock(matched_count=1, modified_count=1)

    params = {
        "order_id": order_id,
        "status": "accepted",
        "payment_method": "Online",
        "remarks": "Good order"
    }

    response = client.patch("/store/order/status", params=params)
    assert response.status_code == 200
    assert "loyalty points awarded" in response.json()["message"]
    assert response.json()["payment_method"] == "Online"

@patch("routes.cake_router.db")
def test_accept_order_loyalty_user_not_found(mock_db, client):
    order_id = "60af924b9e7e3e6b8c8b4568"
    order = {
        "_id": order_id,
        "phone_number": "1234567890",
        "price": 400
    }
    mock_db.cake_orders.find_one.return_value = order
    mock_db.cake_orders.update_one.return_value = MagicMock()
    mock_db.users.update_one.return_value = MagicMock(matched_count=0, modified_count=0)

    params = {
        "order_id": order_id,
        "status": "accepted",
        "payment_method": "Cash",
        "remarks": ""
    }

    response = client.patch("/store/order/status", params=params)
    assert response.status_code == 200
    assert "user not found for loyalty update" in response.json()["message"]

@patch("routes.cake_router.db")
def test_accept_order_no_loyalty_points(mock_db, client):
    order_id = "60af924b9e7e3e6b8c8b4569"
    order = {
        "_id": order_id,
        "phone_number": "1234567890",
        "price": 200
    }
    mock_db.cake_orders.find_one.return_value = order
    mock_db.cake_orders.update_one.return_value = MagicMock()

    params = {
        "order_id": order_id,
        "status": "accepted",
        "payment_method": "",
        "remarks": ""
    }

    response = client.patch("/store/order/status", params=params)
    assert response.status_code == 200
    assert response.json()["message"].startswith("Order status updated to")

@patch("routes.cake_router.db")
def test_reject_order(mock_db, client):
    order_id = "60af924b9e7e3e6b8c8b4570"
    order = {
        "_id": order_id,
        "phone_number": "1234567890",
        "price": 500
    }
    mock_db.cake_orders.find_one.return_value = order
    mock_db.cake_orders.update_one.return_value = MagicMock()

    params = {
        "order_id": order_id,
        "status": "rejected",
        "payment_method": "",
        "remarks": "Out of stock"
    }

    response = client.patch("/store/order/status", params=params)
    assert response.status_code == 200
    assert response.json()["message"].startswith("Order status updated to")

@patch("routes.cake_router.db")
def test_invalid_status(mock_db, client):
    order_id = "60af924b9e7e3e6b8c8b4571"
    params = {
        "order_id": order_id,
        "status": "pending",
        "payment_method": "",
        "remarks": ""
    }
    response = client.patch("/store/order/status", params=params)
    assert response.status_code == 400
    assert "Invalid status" in response.json()["detail"]

@patch("routes.cake_router.db")
def test_invalid_order_id(mock_db, client):
    params = {
        "order_id": "invalidid",
        "status": "accepted",
        "payment_method": "",
        "remarks": ""
    }
    response = client.patch("/store/order/status", params=params)
    assert response.status_code == 400
    assert "Invalid order ID" in response.json()["detail"]

@patch("routes.cake_router.db")
def test_order_not_found(mock_db, client):
    order_id = "60af924b9e7e3e6b8c8b4572"
    mock_db.cake_orders.find_one.return_value = None

    params = {
        "order_id": order_id,
        "status": "accepted",
        "payment_method": "",
        "remarks": ""
    }
    response = client.patch("/store/order/status", params=params)
    assert response.status_code == 404
    assert "Order not found" in response.json()["detail"]