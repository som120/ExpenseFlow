def test_create_list_update_delete_friend(client, registered_user):
    headers = {"Authorization": f"Bearer {registered_user['token']}"}

    create_response = client.post(
        "/api/v1/friends",
        headers=headers,
        json={"name": "Om", "telegram_username": "om_friend", "phone": "1234567890", "notes": "School friend"},
    )
    assert create_response.status_code == 201
    friend_id = create_response.json()["id"]

    list_response = client.get("/api/v1/friends", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.put(
        f"/api/v1/friends/{friend_id}",
        headers=headers,
        json={"notes": "Best friend"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["notes"] == "Best friend"

    delete_response = client.delete(f"/api/v1/friends/{friend_id}", headers=headers)
    assert delete_response.status_code == 204


def test_create_budget_and_compute_remaining_amount(client, registered_user):
    headers = {"Authorization": f"Bearer {registered_user['token']}"}

    transaction_response = client.post(
        "/api/v1/transactions",
        headers=headers,
        json={
            "transaction_type": "personal",
            "category_name": "Food",
            "amount": "400.00",
            "my_share": "400.00",
            "description": "Groceries and meals",
            "payment_owner": "self",
            "transaction_date": "2026-07-05",
            "participants": [],
        },
    )
    assert transaction_response.status_code == 201

    budget_response = client.post(
        "/api/v1/budgets",
        headers=headers,
        json={
            "name": "Food Budget",
            "amount": "1000.00",
            "period": "monthly",
            "category_name": "Food",
            "is_active": True,
        },
    )
    assert budget_response.status_code == 201
    body = budget_response.json()
    assert body["spent_amount"] == "400.00"
    assert body["remaining_amount"] == "600.00"

    list_response = client.get("/api/v1/budgets", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
