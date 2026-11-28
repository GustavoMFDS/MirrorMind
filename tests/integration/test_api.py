from fastapi.testclient import TestClient

from mirrormind.api import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_capabilities_do_not_overstate_implementation():
    payload = client.get("/v1/capabilities").json()
    assert payload["status"] == "scaffold"
    assert "worldkernel_adapter" in payload["experimental"]
    assert "worldkernel_adapter" not in payload["planned"]
    assert "local_retail_policy_test_double" in payload["experimental"]
    assert "synthetic_retail_decision_workflow" in payload["experimental"]
    assert "local_synthetic_tool_orchestration" in payload["experimental"]


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


def test_synthetic_retail_decision_route_returns_the_shared_service_result():
    import json
    from datetime import date

    from mirrormind.domains.retail.synthetic_decision_workflow import (
        SyntheticDecisionWorkflowRequest,
        run_synthetic_decision_workflow,
    )

    request = SyntheticDecisionWorkflowRequest(
        as_of=date(2011, 1, 26), replications=1, seed=17
    )
    response = client.post(
        "/v1/decision-workflows/retail/synthetic",
        json={"as_of": "2011-01-26", "replications": 1, "seed": 17},
    )

    assert response.status_code == 200
    expected = run_synthetic_decision_workflow(request)
    assert response.json() == json.loads(json.dumps(expected, allow_nan=False))
    assert response.json()["trace"]["human_review"]["status"] == "not_requested"
    assert response.json()["writes_performed"] is False


def test_synthetic_retail_decision_route_rejects_unbounded_request_fields():
    response = client.post(
        "/v1/decision-workflows/retail/synthetic",
        json={"as_of": "2011-01-26", "replications": 1, "seed": 17,
              "arbitrary_url": "https://invalid.example"},
    )
    assert response.status_code == 422


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


def test_live_api_claims_equal_reviewed_capability_ledger():
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    ledger = json.loads(
        (root / "docs/engineering/CAPABILITY_LEDGER.json").read_text(encoding="utf-8")
    )
    capabilities = ledger["capabilities"]
    response = client.get("/v1/capabilities")
    assert response.status_code == 200
    public = response.json()
    assert public["status"] == "scaffold"
    assert set(public["implemented"]) == {
        item["id"] for item in capabilities if item["status"] == "implemented"
    }
    assert set(public["planned"]) == {
        item["id"] for item in capabilities if item["status"] == "planned"
    }
    assert set(public["experimental"]) == {
        item["id"] for item in capabilities if item["status"] == "experimental"
    }
    assert not set(public["implemented"]) & set(public["planned"])
    assert all(item["status"] != "implemented" for item in capabilities
               if item["id"] == "simulation_gateway_protocol")


def test_openapi_version_matches_project_version():
    import re
    from pathlib import Path

    from mirrormind import __version__

    project = (Path(__file__).resolve().parents[2] / "pyproject.toml").read_text(
        encoding="utf-8"
    )
    version = re.search(r'^version = "([^"]+)"$', project, re.MULTILINE)
    assert version is not None
    assert version.group(1) == __version__
    assert client.get("/openapi.json").json()["info"]["version"] == __version__
