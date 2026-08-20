from fastapi.testclient import TestClient


# Health / Root 


def test_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "running" in response.json()["message"]


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "ok"


#  Register 


def test_register_success(client: TestClient) -> None:
    response = client.post(
        "/register",
        json={"email": "new@example.com", "password": "securepass123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert "id" in data


def test_register_duplicate_email(client: TestClient, registered_user: dict) -> None:
    response = client.post(
        "/register",
        json={"email": registered_user["email"], "password": "anotherpass123"},
    )
    assert response.status_code == 400


def test_register_weak_password(client: TestClient) -> None:
    response = client.post(
        "/register",
        json={"email": "weak@example.com", "password": "short"},
    )
    assert response.status_code == 422


# ── Login 


def test_login_success(client: TestClient, registered_user: dict) -> None:
    response = client.post(
        "/login",
        data={"username": registered_user["email"], "password": registered_user["password"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, registered_user: dict) -> None:
    response = client.post(
        "/login",
        data={"username": registered_user["email"], "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client: TestClient) -> None:
    response = client.post(
        "/login",
        data={"username": "nobody@example.com", "password": "securepass123"},
    )
    assert response.status_code == 401


#  Transactions CRUD 


def test_create_transaction(client: TestClient, auth_headers: dict) -> None:
    response = client.post(
        "/transactions",
        json={"amount": 50.0, "description": "Coffee", "type": "expense"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 50.0
    assert data["description"] == "Coffee"
    assert data["type"] == "expense"


def test_create_transaction_requires_auth(client: TestClient) -> None:
    response = client.post(
        "/transactions",
        json={"amount": 50.0, "description": "Coffee", "type": "expense"},
    )
    assert response.status_code == 401


def test_get_transactions_empty(client: TestClient, auth_headers: dict) -> None:
    response = client.get("/transactions", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["transactions"] == []
    assert data["total"] == 0


def test_get_transactions_with_data(client: TestClient, auth_headers: dict) -> None:
    client.post(
        "/transactions",
        json={"amount": 10.0, "description": "Item 1", "type": "expense"},
        headers=auth_headers,
    )
    client.post(
        "/transactions",
        json={"amount": 20.0, "description": "Item 2", "type": "income"},
        headers=auth_headers,
    )
    response = client.get("/transactions", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["transactions"]) == 2


def test_get_transactions_pagination(client: TestClient, auth_headers: dict) -> None:
    for i in range(5):
        client.post(
            "/transactions",
            json={"amount": float(i + 1), "description": f"Item {i}", "type": "expense"},
            headers=auth_headers,
        )
    response = client.get("/transactions?page=1&page_size=2", headers=auth_headers)
    data = response.json()
    assert len(data["transactions"]) == 2
    assert data["total"] == 5
    assert data["page"] == 1
    assert data["page_size"] == 2


def test_get_single_transaction(client: TestClient, auth_headers: dict) -> None:
    create_resp = client.post(
        "/transactions",
        json={"amount": 100.0, "description": "Big purchase", "type": "expense"},
        headers=auth_headers,
    )
    tx_id = create_resp.json()["id"]
    response = client.get(f"/transactions/{tx_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == tx_id


def test_get_single_transaction_not_found(client: TestClient, auth_headers: dict) -> None:
    response = client.get("/transactions/99999", headers=auth_headers)
    assert response.status_code == 404


def test_update_transaction(client: TestClient, auth_headers: dict) -> None:
    create_resp = client.post(
        "/transactions",
        json={"amount": 50.0, "description": "Old desc", "type": "expense"},
        headers=auth_headers,
    )
    tx_id = create_resp.json()["id"]
    response = client.put(
        f"/transactions/{tx_id}",
        json={"description": "New desc", "amount": 75.0},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["description"] == "New desc"
    assert response.json()["amount"] == 75.0


def test_update_transaction_not_found(client: TestClient, auth_headers: dict) -> None:
    response = client.put(
        "/transactions/99999",
        json={"description": "Nope"},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_delete_transaction(client: TestClient, auth_headers: dict) -> None:
    create_resp = client.post(
        "/transactions",
        json={"amount": 30.0, "description": "To delete", "type": "expense"},
        headers=auth_headers,
    )
    tx_id = create_resp.json()["id"]
    response = client.delete(f"/transactions/{tx_id}", headers=auth_headers)
    assert response.status_code == 204

    get_resp = client.get(f"/transactions/{tx_id}", headers=auth_headers)
    assert get_resp.status_code == 404


def test_delete_transaction_not_found(client: TestClient, auth_headers: dict) -> None:
    response = client.delete("/transactions/99999", headers=auth_headers)
    assert response.status_code == 404


# ── User isolation ────────────────────────────────────────────────────────────


def test_users_cannot_see_each_others_transactions(client: TestClient) -> None:
    client.post(
        "/register",
        json={"email": "alice@example.com", "password": "securepass123"},
    )
    client.post(
        "/register",
        json={"email": "bob@example.com", "password": "securepass123"},
    )

    login_alice = client.post(
        "/login",
        data={"username": "alice@example.com", "password": "securepass123"},
    )
    token_alice = login_alice.json()["access_token"]
    headers_alice = {"Authorization": f"Bearer {token_alice}"}

    login_bob = client.post(
        "/login",
        data={"username": "bob@example.com", "password": "securepass123"},
    )
    token_bob = login_bob.json()["access_token"]
    headers_bob = {"Authorization": f"Bearer {token_bob}"}

    client.post(
        "/transactions",
        json={"amount": 10.0, "description": "Alice's item", "type": "expense"},
        headers=headers_alice,
    )
    client.post(
        "/transactions",
        json={"amount": 20.0, "description": "Bob's item", "type": "income"},
        headers=headers_bob,
    )

    resp_alice = client.get("/transactions", headers=headers_alice)
    assert resp_alice.json()["total"] == 1
    assert resp_alice.json()["transactions"][0]["description"] == "Alice's item"

    resp_bob = client.get("/transactions", headers=headers_bob)
    assert resp_bob.json()["total"] == 1
    assert resp_bob.json()["transactions"][0]["description"] == "Bob's item"


# ── Summary ───────────────────────────────────────────────────────────────────


def test_summary(client: TestClient, auth_headers: dict) -> None:
    client.post(
        "/transactions",
        json={"amount": 1000.0, "description": "Salary", "type": "income"},
        headers=auth_headers,
    )
    client.post(
        "/transactions",
        json={"amount": 300.0, "description": "Rent", "type": "expense"},
        headers=auth_headers,
    )
    client.post(
        "/transactions",
        json={"amount": 50.0, "description": "Food", "type": "expense"},
        headers=auth_headers,
    )

    response = client.get("/summary", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_income"] == 1000.0
    assert data["total_expense"] == 350.0
    assert data["balance"] == 650.0


def test_summary_empty(client: TestClient, auth_headers: dict) -> None:
    response = client.get("/summary", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_income"] == 0.0
    assert data["total_expense"] == 0.0
    assert data["balance"] == 0.0


def test_summary_requires_auth(client: TestClient) -> None:
    response = client.get("/summary")
    assert response.status_code == 401
