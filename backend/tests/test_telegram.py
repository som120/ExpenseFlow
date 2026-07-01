def test_telegram_help_command(client):
    response = client.post(
        "/api/v1/telegram/webhook",
        json={"chat_id": 1, "text": "/help", "telegram_user_id": 99},
    )

    assert response.status_code == 200
    assert "Supported commands" in response.json()["message"]


def test_telegram_natural_language_preview(client):
    response = client.post(
        "/api/v1/telegram/webhook",
        json={"chat_id": 1, "text": "Dinner 200 with Om", "telegram_user_id": 99},
    )

    assert response.status_code == 200
    body = response.json()
    assert "Detected shared" in body["message"]
    assert body["parsed"]["transaction_type"] == "shared"
