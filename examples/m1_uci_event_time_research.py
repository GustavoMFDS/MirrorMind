"""Run the fixed UCI event-time protocol on an in-memory fictional workbook.

Example: ``python -m examples.m1_uci_event_time_research --split validation``
The generated rows and complete-date declaration are synthetic only.
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

from mirrormind.domains.retail.uci_event_time import (
    SOURCE_END,
    SOURCE_START,
    evaluate_uci_event_time,
)
from mirrormind.domains.retail.uci_transactions import (
    MAX_SUPPORTED_GROUPS,
    MAX_SUPPORTED_ROWS,
)
from mirrormind.domains.retail.uci_workbook import UCI_HEADER, read_uci_workbook

_FIXTURE_CREATED = datetime(2000, 1, 1)
_SYNTHETIC_PRODUCT_A = "SYNTHETIC-A"
_SYNTHETIC_PRODUCT_B = "SYNTHETIC-B"


def _canonical_xlsx(data: bytes) -> bytes:
    """Normalize generated archive metadata so its local digest is repeatable."""
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
                info, payload, compress_type=ZIP_DEFLATED, compresslevel=9
            )
    return output.getvalue()


def build_synthetic_workbook() -> bytes:
    """Construct fictional rows with missing product days and excluded fields."""
    workbook = Workbook()
    workbook.properties.creator = "MirrorMind synthetic fixture"
    workbook.properties.title = "Fictional UCI event-time research"
    workbook.properties.created = _FIXTURE_CREATED
    workbook.properties.modified = _FIXTURE_CREATED
    sheet = workbook.active
    sheet.title = "Online Retail"
    sheet.append(list(UCI_HEADER))

    day_count = (SOURCE_END - SOURCE_START).days + 1
    for index in range(day_count):
        event_day = SOURCE_START + timedelta(days=index)
        if event_day != date(2011, 9, 5):
            quantity = event_day.toordinal() % 11 + 1
            sheet.append([
                str(800_000 + index),
                _SYNTHETIC_PRODUCT_A,
                "SYNTHETIC-PRIVATE-DESCRIPTION",
                quantity,
                datetime(event_day.year, event_day.month, event_day.day, 12),
                1.25,
                987_650 + index,
                "Synthetic",
            ])
        if event_day == date(2011, 9, 1):
            sheet.append([
                "900001", _SYNTHETIC_PRODUCT_B,
                "Synthetic post-fit product", 5,
                datetime(event_day.year, event_day.month, event_day.day, 13),
                1.0, 123_456, "Synthetic",
            ])

    sheet.append([
        "C900002", "SYNTHETIC-CANCELLED", "Synthetic cancellation", -2,
        datetime(2011, 9, 2, 12), 1.0, 234_567, "Synthetic",
    ])
    sheet.append([
        "900003", "SYNTHETIC-ZERO", "Synthetic zero line", 0,
        datetime(2011, 9, 3, 12), 1.0, 345_678, "Synthetic",
    ])
    sheet.append([
        "900004", "SYNTHETIC-RETURN", "Synthetic negative return", -3,
        datetime(2011, 9, 4, 12), 1.0, 456_789, "Synthetic",
    ])
    stream = BytesIO()
    workbook.save(stream)
    workbook.close()
    return _canonical_xlsx(stream.getvalue())


def run_synthetic_evaluation(*, split: str = "validation") -> dict[str, object]:
    """Exercise workbook parsing, coverage declaration and fixed evaluation."""
    raw = build_synthetic_workbook()
    snapshot = read_uci_workbook(
        BytesIO(raw),
        expected_sha256=sha256(raw).hexdigest(),
        max_rows=MAX_SUPPORTED_ROWS,
        max_groups=MAX_SUPPORTED_GROUPS,
    )
    complete_dates = tuple(
        SOURCE_START + timedelta(days=index)
        for index in range((SOURCE_END - SOURCE_START).days + 1)
    )
    return evaluate_uci_event_time(
        snapshot,
        complete_event_dates=complete_dates,
        split=split,  # type: ignore[arg-type] - argparse validates at the CLI boundary
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate fixed baselines on a fictional UCI event-time fixture"
    )
    parser.add_argument("--split", choices=("validation", "holdout"), default="validation")
    args = parser.parse_args()
    try:
        result = run_synthetic_evaluation(split=args.split)
    except (OSError, TypeError, ValueError):
        parser.exit(2, "Invalid synthetic UCI event-time evaluation input.\n")
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
