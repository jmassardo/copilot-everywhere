import pytest
from fastapi.testclient import TestClient

from app import store
from app.main import app


@pytest.fixture(autouse=True)
def reset_store():
    store.reset()
    yield
    store.reset()


@pytest.fixture
def client():
    return TestClient(app)


def _items():
    return [
        {"sku": "WIDGET-1", "description": "Widget", "quantity": 2, "unit_price_cents": 1500},
        {"sku": "GIZMO-9", "description": "Gizmo", "quantity": 1, "unit_price_cents": 4000},
    ]


def test_create_order_returns_201(client):
    response = client.post("/orders", json={"customer_id": "cust-001", "items": _items()})
    assert response.status_code == 201
    body = response.json()
    assert body["customer_id"] == "cust-001"
    assert body["status"] == "pending"
    assert len(body["items"]) == 2


def test_create_order_unknown_customer_returns_400(client):
    response = client.post("/orders", json={"customer_id": "nope", "items": _items()})
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "customer_not_found"


def test_create_order_empty_items_returns_400(client):
    response = client.post("/orders", json={"customer_id": "cust-001", "items": []})
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "empty_order"


def test_get_order_returns_the_order(client):
    created = client.post("/orders", json={"customer_id": "cust-001", "items": _items()}).json()
    response = client.get(f"/orders/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_missing_order_returns_404(client):
    response = client.get("/orders/ord-missing")
    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "order_not_found"


def test_list_orders_filters_by_customer(client):
    client.post("/orders", json={"customer_id": "cust-001", "items": _items()})
    client.post("/orders", json={"customer_id": "cust-002", "items": _items()})

    assert len(client.get("/orders").json()) == 2
    filtered_orders = client.get("/orders", params={"customer_id": "cust-001"}).json()
    assert filtered_orders
    assert all(order["customer_id"] == "cust-001" for order in filtered_orders)

    customer_without_orders = client.post(
        "/customers", json={"email": "empty@example.com", "name": "Empty Customer"}
    ).json()
    assert (
        client.get(
            "/orders", params={"customer_id": customer_without_orders["id"]}
        ).json()
        == []
    )
    assert client.get("/orders", params={"customer_id": "cust-unknown"}).json() == []


def test_delete_order_returns_204(client):
    created = client.post("/orders", json={"customer_id": "cust-001", "items": _items()}).json()
    assert client.delete(f"/orders/{created['id']}").status_code == 204
    assert client.get(f"/orders/{created['id']}").status_code == 404
