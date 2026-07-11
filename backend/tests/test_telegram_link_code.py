def test_generate_and_consume_telegram_link_code(client, registered_user):
    headers = {"Authorization": f"Bearer {registered_user['token']}"}

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
