"""Run a deterministic fictional UCI-shaped evidence-to-evaluation example.

Usage: python -m examples.m1_retail_synthetic_evaluation --holdout-days 7

The workbook is created in memory. It contains no source data and the
declared release dates are invented fixture values, not publisher evidence.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, timedelta
from hashlib import sha256
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from openpyxl import Workbook

from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.evaluation_flow import evaluate_retail_evidence_flow
from mirrormind.domains.retail.evidence_flow import (
    RetailUciEvidenceFlow,
    prepare_retail_uci_evidence_flow,
)
from mirrormind.domains.retail.uci_workbook import UCI_HEADER
from mirrormind.modules.evidence.intake_review import SourceReviewDeclaration

START = date(2011, 1, 1)
SYNTHETIC_STOCK_CODE = "SYNTHETIC-SKU"
EVALUATION_ON = START + timedelta(days=34)
INSPECTED_ON = date(2026, 11, 23)
CAPTURED_ON = date(2026, 11, 22)
FIXTURE_CREATED = datetime(2000, 1, 1)


def _fixture_day(index: int) -> date:
    return START + timedelta(days=index - 1)


def _canonical_xlsx(data: bytes) -> bytes:
    """Normalize ZIP order, timestamps and compression for a stable fixture digest."""
    output = BytesIO()
    with ZipFile(BytesIO(data), "r") as source, ZipFile(
        output, "w", compression=ZIP_DEFLATED, compresslevel=9
    ) as target:
        for filename in sorted(source.namelist()):
            info = ZipInfo(filename, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o600 << 16
            info.flag_bits = 0
            payload = source.read(filename)
            if filename == "docProps/core.xml":
                payload, replacements = re.subn(
                    rb'(<dcterms:modified[^>]*>).*?(</dcterms:modified>)',
                    rb"\g<1>2000-01-01T00:00:00Z\g<2>",
                    payload,
                )
                if replacements != 1:
                    raise ValueError("unexpected synthetic workbook metadata")
            target.writestr(
                info,
                payload,
                compress_type=ZIP_DEFLATED,
                compresslevel=9,
            )
    return output.getvalue()


def _synthetic_workbook(*, future_units: int) -> bytes:
    workbook = Workbook()
    workbook.properties.creator = "MirrorMind synthetic fixture"
    workbook.properties.title = "Fictional retail release evaluation"
    workbook.properties.created = FIXTURE_CREATED
    workbook.properties.modified = FIXTURE_CREATED
    sheet = workbook.active
    sheet.title = "Online Retail"
    sheet.append(list(UCI_HEADER))
    for index in range(1, 36):
        if index == 33:
            continue
        observed_on = _fixture_day(index)
        units = future_units if index == 35 else index % 7 + 1
        sheet.append([
            str(500_000 + index),
            SYNTHETIC_STOCK_CODE,
            "Fictional product description",
            units,
            datetime(observed_on.year, observed_on.month, observed_on.day, 12),
            1.5,
            1_234_500 + index,
            "Fictional",
        ])
    stream = BytesIO()
    workbook.save(stream)
    workbook.close()
    return _canonical_xlsx(stream.getvalue())


def build_synthetic_evidence_flow(
    *, future_units: int = 9, all_unpublished: bool = False
) -> RetailUciEvidenceFlow:
    """Build a bounded, deterministic, in-memory fictional evidence flow."""
    if type(future_units) is not int or not 1 <= future_units <= 10_000:
        raise ValueError("future_units must be an exact integer in 1..10000")
    if type(all_unpublished) is not bool:
        raise ValueError("all_unpublished must be an exact boolean")
    raw = _synthetic_workbook(future_units=future_units)
    digest = sha256(raw).hexdigest()
    releases = []
    for index in range(1, 36):
        if index == 33:
            continue
        observed_on = _fixture_day(index)
        if all_unpublished:
            available_on = _fixture_day(36)
        elif index == 27:
            available_on = _fixture_day(30)
        elif index == 35:
            available_on = _fixture_day(36)
        else:
            available_on = observed_on
        releases.append(DeclaredProductRelease(
            SYNTHETIC_STOCK_CODE, observed_on, available_on
        ))
    declaration = SourceReviewDeclaration(
        source_kind="uci_xlsx",
        source_record_ref="SYNTHETIC-SOURCE-01",
        snapshot_sha256=digest,
        license_evidence_ref="SYNTHETIC-LICENSE-01",
        permission_evidence_ref="SYNTHETIC-PERMISSION-01",
        privacy_review_ref="SYNTHETIC-PRIVACY-01",
        intended_use="research_evaluation",
        retention_days=30,
        captured_on=CAPTURED_ON,
        availability_evidence_ref="SYNTHETIC-AVAILABILITY-01",
    )
    return prepare_retail_uci_evidence_flow(
        BytesIO(raw),
        expected_sha256=digest,
        declaration=declaration,
        inspected_on=INSPECTED_ON,
        declared_calendar=tuple(_fixture_day(i) for i in range(1, 36)),
        declared_releases=tuple(releases),
        origin_on=EVALUATION_ON,
    )


def run_synthetic_evaluation(
    *,
    holdout_days: int = 7,
    future_units: int = 9,
    all_unpublished: bool = False,
) -> dict[str, object]:
    """Build the fictional fixture and run the complete local evaluation path."""
    flow = build_synthetic_evidence_flow(
        future_units=future_units,
        all_unpublished=all_unpublished,
    )
    return evaluate_retail_evidence_flow(
        flow,
        stock_code=SYNTHETIC_STOCK_CODE,
        evaluation_on=EVALUATION_ON,
        holdout_days=holdout_days,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a fictional release-aware retail baseline evaluation"
    )
    parser.add_argument("--holdout-days", type=int, default=7)
    args = parser.parse_args()
    try:
        result = run_synthetic_evaluation(holdout_days=args.holdout_days)
    except (OSError, TypeError, ValueError):
        parser.exit(2, "Invalid synthetic retail evaluation configuration.\n")
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
