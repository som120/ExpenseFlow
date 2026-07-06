import hashlib
import hmac
import time

from app.core.config import settings


def build_payload(**overrides):
    payload = {
        "id": 123456,
        "first_name": "Somnath",
        "last_name": "Paul",
        "username": "som120",
        "photo_url": "https://t.me/i/userpic/320/test.jpg",
        "auth_date": int(time.time()),
    }
    payload.update(overrides)
    data = {key: value for key, value in payload.items() if value is not None}
    check_string = "\n".join(f"{key}={data[key]}" for key in sorted(data))
    secret = hashlib.sha256((settings.telegram_bot_token or "test-telegram-token").encode()).digest()
    payload["hash"] = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()
    return payload


def test_telegram_auth_creates_user(client, monkeypatch):
    monkeypatch.setattr(settings, "telegram_bot_token", "test-telegram-token")
    response = client.post("/api/v1/auth/telegram", json=build_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["user"]["full_name"] == "Somnath Paul"
    assert body["access_token"]


def test_telegram_link_links_existing_user(client, registered_user, monkeypatch):
    monkeypatch.setattr(settings, "telegram_bot_token", "test-telegram-token")
    response = client.post(
        "/api/v1/auth/telegram/link",
        headers={"Authorization": f"Bearer {registered_user['token']}"},
        json=build_payload(id=999001, username="linked_user"),
    )

    assert response.status_code == 200
    assert response.json()["full_name"] == "Somnath Paul"
