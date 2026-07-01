def test_register_and_login(client):
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "founder@expenseflow.dev",
            "full_name": "Founder",
            "password": "supersecret",
        },
    )

    assert register_response.status_code == 201
    assert register_response.json()["email"] == "founder@expenseflow.dev"

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "founder@expenseflow.dev", "password": "supersecret"},
    )

    assert login_response.status_code == 200
    assert login_response.json()["token_type"] == "bearer"
    assert "access_token" in login_response.json()


def test_get_me_requires_auth(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_get_me_returns_current_user(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "me@expenseflow.dev",
            "full_name": "Current User",
            "password": "supersecret",
        },
    )
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "me@expenseflow.dev", "password": "supersecret"},
    )

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {login_response.json()['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "me@expenseflow.dev"
