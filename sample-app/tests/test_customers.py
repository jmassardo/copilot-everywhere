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


def _assert_utc_timestamp(value):
    created_at = datetime.fromisoformat(value)
    assert created_at.tzinfo is not None
    assert created_at.utcoffset() == timedelta(0)


def test_list_customers_returns_seeded_customers(client):
    body = client.get("/customers").json()
    assert len(body["customers"]) == 2
    for customer in body["customers"]:
        _assert_utc_timestamp(customer["created_at"])


def test_reset_recreates_seeded_customers_with_utc_timestamps(client):
    for _ in range(3):
        store.reset()
        body = client.get("/customers").json()
        for customer in body["customers"]:
            _assert_utc_timestamp(customer["created_at"])


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
    _assert_utc_timestamp(body["created_at"])


def test_create_duplicate_email_returns_error_body(client):
    response = client.post(
        "/customers", json={"email": "mona@example.com", "name": "Duplicate"}
    )
    assert response.json()["error"] == "email already registered"


def test_delete_customer(client):
    assert client.delete("/customers/cust-001").json() == {"deleted": "cust-001"}
