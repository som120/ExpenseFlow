def test_telegram_help_command(client):
    response = client.post(
        "/api/v1/telegram/webhook",
        json={
            "update_id": 1,
            "message": {
                "message_id": 10,
                "date": 1710000000,
                "text": "/help",
                "chat": {"id": 1, "type": "private"},
                "from": {"id": 99, "is_bot": False, "first_name": "Test"},
            },
        },
    )

    assert response.status_code == 200
    assert "Supported commands" in response.json()["message"]


def test_telegram_natural_language_preview(client):
    response = client.post(
        "/api/v1/telegram/webhook",
        json={
            "update_id": 2,
            "message": {
                "message_id": 11,
                "date": 1710000001,
                "text": "Dinner 200 with Om",
                "chat": {"id": 1, "type": "private"},
                "from": {"id": 99, "is_bot": False, "first_name": "Test"},
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert "Saved transaction." in body["message"]
    assert "Detected shared" in body["message"]
    assert body["parsed"]["transaction_type"] == "shared"

    summary_response = client.post(
        "/api/v1/telegram/webhook",
        json={
            "update_id": 4,
            "message": {
                "message_id": 13,
                "date": 1710000003,
                "text": "/summary",
                "chat": {"id": 1, "type": "private"},
                "from": {"id": 99, "is_bot": False, "first_name": "Test"},
            },
        },
    )

    assert summary_response.status_code == 200
    assert "Expenses: 100.00" in summary_response.json()["message"]


def test_telegram_creates_user_and_saves_income(client):
    response = client.post(
        "/api/v1/telegram/webhook",
        json={
            "update_id": 5,
            "message": {
                "message_id": 14,
                "date": 1710000004,
                "text": "Received 45000 salary",
                "chat": {"id": 22, "type": "private"},
                "from": {"id": 501, "is_bot": False, "first_name": "Alex", "username": "alex_user"},
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert "Saved transaction." in body["message"]
    assert body["parsed"]["transaction_type"] == "income"


def test_telegram_ignores_non_text_updates(client):
    response = client.post(
        "/api/v1/telegram/webhook",
        json={
            "update_id": 3,
            "message": {
                "message_id": 12,
                "date": 1710000002,
                "chat": {"id": 1, "type": "private"},
                "from": {"id": 99, "is_bot": False, "first_name": "Test"},
                "photo": [{"file_id": "abc", "file_unique_id": "def", "width": 10, "height": 10}],
            },
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Ignored unsupported Telegram update type."
