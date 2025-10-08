import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_success():
    # Use a unique email for testing
    email = "testuser1@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Check participant added
    get_resp = client.get("/activities")
    assert email in get_resp.json()[activity]["participants"]


def test_signup_for_activity_already_signed_up():
    email = "testuser2@mergington.edu"
    activity = "Programming Class"
    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Try to sign up again for another activity
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_for_activity_not_found():
    email = "testuser3@mergington.edu"
    response = client.post(f"/activities/Nonexistent/signup?email={email}")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
