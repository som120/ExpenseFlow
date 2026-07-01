from datetime import date


def test_create_shared_transaction_and_summary(client, registered_user):
    headers = {"Authorization": f"Bearer {registered_user['token']}"}

    transaction_response = client.post(
        "/api/v1/transactions",
        headers=headers,
        json={
            "transaction_type": "shared",
            "category_name": "Food",
            "amount": "200.00",
            "my_share": "100.00",
            "description": "Dinner with Om",
            "payment_owner": "self",
            "transaction_date": date.today().isoformat(),
            "participants": [
                {
                    "participant_name": "Om",
                    "share_amount": "100.00",
                    "pending_amount": "100.00",
                    "status": "pending",
                }
            ],
        },
    )

    assert transaction_response.status_code == 201
    body = transaction_response.json()
    assert body["category_name"] == "Food"
    assert len(body["participants"]) == 1

    summary_response = client.get("/api/v1/summary", headers=headers)
    assert summary_response.status_code == 200
    summary = summary_response.json()
    assert summary["total_expenses"] == "100.00"
    assert summary["money_owed_to_you"] == "100.00"


def test_update_and_delete_transaction(client, registered_user):
    headers = {"Authorization": f"Bearer {registered_user['token']}"}

    create_response = client.post(
        "/api/v1/transactions",
        headers=headers,
        json={
            "transaction_type": "personal",
            "category_name": "Transport",
            "amount": "450.00",
            "my_share": "450.00",
            "description": "Cab",
            "payment_owner": "self",
            "transaction_date": date.today().isoformat(),
            "participants": [],
        },
    )

    assert create_response.status_code == 201
    transaction_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/v1/transactions/{transaction_id}",
        headers=headers,
        json={"description": "Airport cab", "amount": "500.00", "my_share": "500.00"},
    )

    assert update_response.status_code == 200
    assert update_response.json()["description"] == "Airport cab"
    assert update_response.json()["amount"] == "500.00"

    delete_response = client.delete(f"/api/v1/transactions/{transaction_id}", headers=headers)
    assert delete_response.status_code == 204

    list_response = client.get("/api/v1/transactions", headers=headers)
    assert list_response.status_code == 200
    assert list_response.json() == []


def test_income_transaction_rejects_participants(client, registered_user):
    headers = {"Authorization": f"Bearer {registered_user['token']}"}

    response = client.post(
        "/api/v1/transactions",
        headers=headers,
        json={
            "transaction_type": "income",
            "category_name": "Salary",
            "amount": "1000.00",
            "my_share": "1000.00",
            "description": "Salary credit",
            "payment_owner": "employer",
            "transaction_date": date.today().isoformat(),
            "participants": [
                {
                    "participant_name": "Om",
                    "share_amount": "100.00",
                    "pending_amount": "100.00",
                    "status": "pending",
                }
            ],
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Income transactions cannot have participants"


def test_borrowed_transaction_updates_money_you_owe(client, registered_user):
    headers = {"Authorization": f"Bearer {registered_user['token']}"}

    response = client.post(
        "/api/v1/transactions",
        headers=headers,
        json={
            "transaction_type": "borrowed",
            "category_name": "Food",
            "amount": "200.00",
            "my_share": "100.00",
            "description": "Dinner paid by Om",
            "payment_owner": "Om",
            "transaction_date": date.today().isoformat(),
            "participants": [
                {
                    "participant_name": "Om",
                    "share_amount": "100.00",
                    "pending_amount": "100.00",
                    "status": "pending",
                }
            ],
        },
    )

    assert response.status_code == 201

    summary_response = client.get("/api/v1/summary", headers=headers)
    assert summary_response.status_code == 200
    summary = summary_response.json()
    assert summary["total_expenses"] == "100.00"
    assert summary["money_you_owe"] == "100.00"
