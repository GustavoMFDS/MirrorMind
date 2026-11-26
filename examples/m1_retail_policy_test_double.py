"""Run a fictional 28-day retail replenishment comparison locally.

Usage: python -m examples.m1_retail_policy_test_double

All demand and inventory inputs are illustrative assumptions. This example
does not load a dataset, call a forecast model, or invoke WorldKernel.
"""
from __future__ import annotations

import json

from mirrormind.domains.retail.policy_simulation import (
    RetailPolicyAssumptions,
    RetailPolicyComparisonRequest,
    compare_synthetic_retail_policies,
)


def run_synthetic_policy_demo() -> dict[str, object]:
    """Run the same fictional fixture used by the documented CLI example."""
    request = RetailPolicyComparisonRequest(
        demand_profile_units=tuple(10 + day % 7 for day in range(28)),
        assumptions=RetailPolicyAssumptions(
            initial_stock_units=65,
            lead_time_days=2,
            fixed_order_quantity_units=70,
            reorder_point_units=55,
            review_period_days=7,
            safety_stock_units=15,
            procurement_cost_per_unit=2,
            holding_cost_per_unit_day=1,
            fixed_order_cost=12,
            unmet_demand_penalty_per_unit=8,
        ),
        replications=12,
        seed=317,
    )
    return {
        **compare_synthetic_retail_policies(request),
        "fixture_label": "fictional_demo",
    }


def main() -> int:
    try:
        result = run_synthetic_policy_demo()
    except (TypeError, ValueError):
        print("Invalid synthetic retail policy comparison configuration.")
        return 2
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
