def test_generate_and_consume_telegram_link_code(client, registered_user):
    headers = {"Authorization": f"Bearer {registered_user['token']}"}

    client.post(
        "/api/v1/transactions",
        headers=headers,
        json={
            "transaction_type": "personal",
            "category_name": "Food",
            "amount": "410.00",
            "my_share": "410.00",
            "description": "Website expense",
            "payment_owner": "self",
            "transaction_date": "2026-07-06",
            "participants": [],
        },
    )

    code_response = client.post("/api/v1/auth/telegram/link-code", headers=headers)
    assert code_response.status_code == 200
    code = code_response.json()["code"]

    telegram_response = client.post(
        "/api/v1/telegram/webhook",
        json={
            "update_id": 99,
            "message": {
                "message_id": 50,
                "date": 1710000005,
                "text": f"/link {code}",
                "chat": {"id": 501, "type": "private"},
                "from": {"id": 501, "is_bot": False, "first_name": "Somnath", "username": "som120"},
            },
        },
    )

    assert telegram_response.status_code == 200
    assert "Telegram linked successfully" in telegram_response.json()["message"]

    balance_response = client.post(
        "/api/v1/telegram/webhook",
        json={
            "update_id": 100,
            "message": {
                "message_id": 51,
                "date": 1710000006,
                "text": "/balance",
                "chat": {"id": 501, "type": "private"},
                "from": {"id": 501, "is_bot": False, "first_name": "Somnath", "username": "som120"},
            },
        },
    )
    assert balance_response.status_code == 200
    assert "Expenses: 410.00" in balance_response.json()["message"]
