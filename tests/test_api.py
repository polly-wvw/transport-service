from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_and_get():
    payload = {
        "vehicle_number": "А123ВС77",
        "maintenance_type": "TO-1",
        "desired_date": "2026-01-15",
        "description": "Стук в подвеске",
    }
    r = client.post("/api/v1/routes/", json=payload)
    assert r.status_code == 201
    rid = r.json()["id"]

    r = client.get(f"/api/v1/routes/{rid}")
    assert r.status_code == 200
    assert r.json()["vehicle_number"] == "А123ВС77"


def test_get_404():
    assert client.get("/api/v1/routes/99999").status_code == 404


def test_delete():
    r = client.post("/api/v1/routes/", json={
        "vehicle_number": "B1",
        "maintenance_type": "TO-2",
        "desired_date": "2026-02-01",
    })
    rid = r.json()["id"]
    assert client.delete(f"/api/v1/routes/{rid}").status_code == 204
    assert client.get(f"/api/v1/routes/{rid}").status_code == 404