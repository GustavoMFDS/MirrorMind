"""Local fictional experiment metadata journal; not an independent authority."""
from __future__ import annotations

import hmac
import re
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Literal

from mirrormind.domains.retail.census_experiment import (
    CensusExperimentSpec,
    census_experiment_sha256,
    prepare_census_experiment,
    verify_census_experiment_receipt,
)
from mirrormind.domains.retail.census_split import CensusOriginSchedule
from mirrormind.domains.retail.census_vintages import CensusVintageRecord

MAX_CENSUS_JOURNAL_EXPERIMENTS = 1000
_SCHEMA_VERSION = 1
_APPLICATION_ID = 0x4D4D434A
_SHA256 = re.compile(r"[0-9a-f]{64}")
_EXPERIMENTS_SQL = (
    "CREATE TABLE experiments (id TEXT NOT NULL PRIMARY KEY, "
    "schedule TEXT NOT NULL, manifest TEXT NOT NULL, revision TEXT NOT NULL)"
)
_RECEIPTS_SQL = (
    "CREATE TABLE receipts (experiment_id TEXT NOT NULL REFERENCES experiments(id), "
    "split TEXT NOT NULL CHECK(split IN ('validation','holdout')), "
    "digest TEXT NOT NULL, PRIMARY KEY(experiment_id,split))"
)
_EXPECTED_OBJECTS = (
    ("table", "experiments", _EXPERIMENTS_SQL),
    ("table", "receipts", _RECEIPTS_SQL),
)


def _checked_sha(value: object) -> str:
    if type(value) is not str or not _SHA256.fullmatch(value):
        raise ValueError("invalid digest")
    return value


def _objects(db: sqlite3.Connection) -> tuple[tuple[object, ...], ...]:
    return tuple(db.execute(
        "SELECT type,name,sql FROM sqlite_master WHERE name NOT GLOB 'sqlite_*' "
        "ORDER BY name LIMIT 3"
    ))


def _check_schema(db: sqlite3.Connection) -> None:
    if (
        db.execute("PRAGMA application_id").fetchone()[0] != _APPLICATION_ID
        or db.execute("PRAGMA user_version").fetchone()[0] != _SCHEMA_VERSION
        or _objects(db) != _EXPECTED_OBJECTS
    ):
        raise ValueError("incompatible journal schema")
    if db.execute("PRAGMA foreign_key_check").fetchone() is not None:
        raise ValueError("journal foreign key violation")


class CensusExperimentJournal:
    """Metadata-only journal on a caller-controlled local filesystem."""

    def __init__(self, path: Path) -> None:
        if type(path) is not type(Path()) or not path.is_absolute():
            raise ValueError("explicit absolute journal path required")
        self._path = path
        with self._transaction(initialize=True):
            pass

    @contextmanager
    def _transaction(self, *, initialize: bool = False) -> Iterator[sqlite3.Connection]:
        db = sqlite3.connect(self._path, timeout=3, isolation_level=None)
        try:
            db.execute("PRAGMA foreign_keys=ON")
            db.execute("PRAGMA trusted_schema=OFF")
            db.execute("BEGIN IMMEDIATE")
            if initialize and (
                db.execute("PRAGMA application_id").fetchone()[0] == 0
                and db.execute("PRAGMA user_version").fetchone()[0] == 0
                and not _objects(db)
            ):
                db.execute(_EXPERIMENTS_SQL)
                db.execute(_RECEIPTS_SQL)
                db.execute(f"PRAGMA application_id={_APPLICATION_ID}")
                db.execute(f"PRAGMA user_version={_SCHEMA_VERSION}")
            _check_schema(db)
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def _read_spec(db: sqlite3.Connection, experiment_id: str) -> CensusExperimentSpec:
        row = db.execute(
            "SELECT schedule,manifest,revision FROM experiments WHERE id=?", (experiment_id,)
        ).fetchone()
        if row is None:
            raise ValueError("experiment not registered")
        spec = CensusExperimentSpec(*row)
        if census_experiment_sha256(spec) != experiment_id:
            raise ValueError("stored commitment mismatch")
        return spec

    def register(
        self,
        records: tuple[CensusVintageRecord, ...],
        *,
        plan: CensusOriginSchedule,
        spec: CensusExperimentSpec,
        expected_experiment_sha256: str,
        declared_code_revision: str,
    ) -> str:
        eid = census_experiment_sha256(spec)
        if not hmac.compare_digest(eid, _checked_sha(expected_experiment_sha256)):
            raise ValueError("experiment fingerprint mismatch")
        if prepare_census_experiment(
            records, plan=plan, declared_code_revision=declared_code_revision
        ) != spec:
            raise ValueError("experiment inputs differ from commitment")
        with self._transaction() as db:
            if db.execute("SELECT 1 FROM experiments WHERE id=?", (eid,)).fetchone():
                if self._read_spec(db, eid) != spec:
                    raise ValueError("commitment conflict")
            else:
                if db.execute("SELECT count(*) FROM experiments").fetchone()[0] >= MAX_CENSUS_JOURNAL_EXPERIMENTS:
                    raise ValueError("journal capacity reached")
                db.execute(
                    "INSERT INTO experiments VALUES(?,?,?,?)",
                    (eid, spec.schedule_sha256, spec.input_manifest_sha256, spec.declared_code_revision),
                )
        return eid

    def _replay(
        self,
        experiment_id: str,
        records: tuple[CensusVintageRecord, ...],
        *,
        plan: CensusOriginSchedule,
        split: Literal["validation", "holdout"],
        declared_code_revision: str,
        submitted: bytes,
    ) -> tuple[CensusExperimentSpec, str]:
        _checked_sha(experiment_id)
        with self._transaction() as db:
            spec = self._read_spec(db, experiment_id)
        digest = verify_census_experiment_receipt(
            records, plan=plan, spec=spec, expected_experiment_sha256=experiment_id,
            split=split, declared_code_revision=declared_code_revision, submitted=submitted,
        )
        return spec, _checked_sha(digest)

    def admit(
        self,
        experiment_id: str,
        records: tuple[CensusVintageRecord, ...],
        *,
        plan: CensusOriginSchedule,
        split: Literal["validation", "holdout"],
        declared_code_revision: str,
        submitted: bytes,
    ) -> str:
        spec, digest = self._replay(
            experiment_id, records, plan=plan, split=split,
            declared_code_revision=declared_code_revision, submitted=submitted,
        )
        with self._transaction() as db:
            if self._read_spec(db, experiment_id) != spec:
                raise ValueError("commitment changed during replay")
            row = db.execute(
                "SELECT digest FROM receipts WHERE experiment_id=? AND split=?", (experiment_id, split)
            ).fetchone()
            if row is not None:
                if _checked_sha(row[0]) != digest:
                    raise ValueError("receipt conflict")
            else:
                db.execute("INSERT INTO receipts VALUES(?,?,?)", (experiment_id, split, digest))
        return digest

    def verify_stored(
        self,
        experiment_id: str,
        records: tuple[CensusVintageRecord, ...],
        *,
        plan: CensusOriginSchedule,
        split: Literal["validation", "holdout"],
        declared_code_revision: str,
        submitted: bytes,
    ) -> str:
        spec, digest = self._replay(
            experiment_id, records, plan=plan, split=split,
            declared_code_revision=declared_code_revision, submitted=submitted,
        )
        with self._transaction() as db:
            if self._read_spec(db, experiment_id) != spec:
                raise ValueError("commitment changed during replay")
            row = db.execute(
                "SELECT digest FROM receipts WHERE experiment_id=? AND split=?", (experiment_id, split)
            ).fetchone()
            if row is None or _checked_sha(row[0]) != digest:
                raise ValueError("stored receipt does not match local replay")
        return digest

    def read(self, experiment_id: str) -> dict[str, object]:
        """Read unverified metadata; use verify_stored for explicit local replay."""
        _checked_sha(experiment_id)
        with self._transaction() as db:
            spec = self._read_spec(db, experiment_id)
            rows = db.execute(
                "SELECT split,digest FROM receipts WHERE experiment_id=? ORDER BY split",
                (experiment_id,),
            ).fetchall()
            if any(split not in ("validation", "holdout") for split, _ in rows):
                raise ValueError("stored split invalid")
            return {
                "experiment_sha256": experiment_id,
                "schedule_sha256": spec.schedule_sha256,
                "input_manifest_sha256": spec.input_manifest_sha256,
                "declared_code_revision": spec.declared_code_revision,
                "receipts": {split: _checked_sha(digest) for split, digest in rows},
                "stored_receipts_verified_on_read": False,
                "registration_verified": False,
                "holdout_lock_verified": False,
                "runtime_code_attested": False,
                "action_authorized": False,
                "ingestion_authorized": False,
                "forecast_eligible": False,
                "inference_status": "abstained",
            }
