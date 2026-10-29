import pytest
from fastapi.testclient import TestClient

from app import main


@pytest.fixture(autouse=True)
def clean_state():
    main._habits.clear()
    main._next_id = 1
    yield


@pytest.fixture
def client():
    return TestClient(main.app)


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_habit(client):
    response = client.post("/habits", json={"name": "Morning run"})
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["name"] == "Morning run"
    assert body["check_ins"] == []


def test_create_habit_rejects_empty_name(client):
    response = client.post("/habits", json={"name": ""})
    assert response.status_code == 422


def test_streak_after_check_ins(client):
    client.post("/habits", json={"name": "Reading"})
    for done in [True, False, True, True]:
        client.post("/habits/1/checkins", json={"done": done})
    response = client.get("/habits/1/streak")
    assert response.status_code == 200
    assert response.json() == {"habit_id": 1, "streak": 2}


def test_unknown_habit_returns_404(client):
    assert client.get("/habits/999/streak").status_code == 404
    assert client.post("/habits/999/checkins", json={"done": True}).status_code == 404


def test_list_habits(client):
    client.post("/habits", json={"name": "A"})
    client.post("/habits", json={"name": "B"})
    response = client.get("/habits")
    assert [h["name"] for h in response.json()] == ["A", "B"]

