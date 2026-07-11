from datetime import date


def seed_transactions(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    client.post(
        "/api/v1/transactions",
        headers=headers,
        json={
            "transaction_type": "income",
            "category_name": "Salary",
            "amount": "50000.00",
            "my_share": "50000.00",
            "description": "Salary",
            "payment_owner": "employer",
            "transaction_date": date.today().isoformat(),
            "participants": [],
        },
    )
    client.post(
        "/api/v1/transactions",
        headers=headers,
        json={
            "transaction_type": "shared",
            "category_name": "Food",
            "amount": "600.00",
            "my_share": "300.00",
            "description": "Dinner",
            "payment_owner": "self",
            "transaction_date": date.today().isoformat(),
            "participants": [
                {"participant_name": "Om", "share_amount": "300.00", "pending_amount": "300.00", "status": "pending"}
            ],
        },
    )


def test_analytics_endpoint(client, registered_user):
    seed_transactions(client, registered_user["token"])
    headers = {"Authorization": f"Bearer {registered_user['token']}"}

    response = client.get("/api/v1/analytics", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["top_spending_category"] == "Food"
    assert len(body["monthly_trends"]) >= 1


def test_reports_and_exports(client, registered_user):
    seed_transactions(client, registered_user["token"])
    headers = {"Authorization": f"Bearer {registered_user['token']}"}

    report_response = client.get("/api/v1/reports", headers=headers)
    assert report_response.status_code == 200
    assert report_response.json()["report_type"] == "monthly"

    csv_response = client.get("/api/v1/reports/export/csv", headers=headers)
    assert csv_response.status_code == 200
    assert "title,value" in csv_response.json()["content"]
