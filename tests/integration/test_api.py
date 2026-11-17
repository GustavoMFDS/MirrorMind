from fastapi.testclient import TestClient

from mirrormind.api import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_capabilities_do_not_overstate_implementation():
    payload = client.get("/v1/capabilities").json()
    assert payload["status"] == "scaffold"
    assert "worldkernel_adapter" in payload["planned"]


def test_scenario_validation_only():
    spec = {
        "world_type": "retail.inventory",
        "world_version": "0.1",
        "horizon_days": 28,
        "runs": 10,
        "budget": {"max_simulation_runs": 10}
    }
    response = client.post("/v1/scenarios/validate", json=spec)
    assert response.status_code == 200
    assert response.json()["status"] == "validated_not_executed"


def test_runs_cannot_exceed_budget():
    spec = {
        "world_type": "retail.inventory",
        "world_version": "0.1",
        "horizon_days": 28,
        "runs": 20,
        "budget": {"max_simulation_runs": 10}
    }
    assert client.post("/v1/scenarios/validate", json=spec).status_code == 422


def test_forecast_must_cover_scenario_horizon():
    spec = {
        "world_type": "retail.inventory",
        "world_version": "0.1",
        "horizon_days": 28,
        "runs": 1,
        "forecast": {
            "forecast_id": "example",
            "model_version": "v0",
            "horizon_days": 7
        }
    }
    assert client.post("/v1/scenarios/validate", json=spec).status_code == 422
