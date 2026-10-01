from datetime import datetime, timedelta

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


def test_list_customers_returns_seeded_customers(client):
    for _ in range(3):
        body = client.get("/customers").json()
        assert len(body["customers"]) == 2
        assert all(
            datetime.fromisoformat(customer["created_at"]).utcoffset() == timedelta(0)
            for customer in body["customers"]
        )
        store.reset()


def test_get_customer_returns_customer(client):
    body = client.get("/customers/cust-001").json()
    assert body["email"] == "mona@example.com"


def test_get_missing_customer_returns_error_body(client):
    response = client.get("/customers/nope")
    # Note the 200. See the module docstring in app/routers/customers.py.
    assert response.status_code == 200
    assert response.json()["error"] == "not found"


def test_create_customer_succeeds(client):
    response = client.post(
        "/customers", json={"email": "new@example.com", "name": "New Person"}
    )
    body = response.json()
    assert body["email"] == "new@example.com"
    assert datetime.fromisoformat(body["created_at"]).utcoffset() == timedelta(0)


def test_create_duplicate_email_returns_error_body(client):
    response = client.post(
        "/customers", json={"email": "mona@example.com", "name": "Duplicate"}
    )
    assert response.json()["error"] == "email already registered"


def test_delete_customer(client):
    assert client.delete("/customers/cust-001").json() == {"deleted": "cust-001"}
