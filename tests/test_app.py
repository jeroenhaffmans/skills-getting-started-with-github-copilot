from fastapi.testclient import TestClient
import pytest

from src import app

client = TestClient(app.app)


def test_get_activities_initial_state():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    # should be a dict with at least one activity
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_success_and_duplicate():
    # sign up a dummy email for Chess Club
    email = "test@example.com"
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # signing up again should return 400
    response2 = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant():
    email = "removeme@example.com"
    # first add participant so removal can be tested
    client.post(f"/activities/Chess%20Club/signup?email={email}")

    # now remove
    response = client.delete(f"/activities/Chess%20Club/participants?email={email}")
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]

    # removing again should 404
    response2 = client.delete(f"/activities/Chess%20Club/participants?email={email}")
    assert response2.status_code == 404
    assert response2.json()["detail"] == "Participant not found"


def test_remove_from_nonexistent_activity():
    resp = client.delete("/activities/Fake%20Club/participants?email=foo@bar.com")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"
