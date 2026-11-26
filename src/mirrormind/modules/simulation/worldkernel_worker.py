"""Pinned one-shot worker for the optional local WorldKernel runtime.

The parent sends one JSON exchange request on stdin. This worker verifies the
installed VCS commit, registers WorldKernel's trusted built-ins plus one fixed
MirrorMind handler, requires the registered world revision and writes only the
versioned result to stdout.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from importlib import metadata
from urllib.parse import urlsplit

_EXPECTED_REPOSITORY = "github.com/gustavomfds/worldkernel"
_EXPECTED_PACKAGE_VERSION = "0.0.1"


class _RuntimeMissing(Exception):
    pass


class _RuntimePinMismatch(Exception):
    pass


def _verify_installed_runtime(expected_commit: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", expected_commit):
        raise _RuntimePinMismatch
    try:
        distribution = metadata.distribution("worldkernel")
    except metadata.PackageNotFoundError as exc:
        raise _RuntimeMissing from exc
    if distribution.version != _EXPECTED_PACKAGE_VERSION:
        raise _RuntimePinMismatch
    direct_url_text = distribution.read_text("direct_url.json")
    if direct_url_text is None:
        raise _RuntimePinMismatch
    try:
        direct_url = json.loads(direct_url_text)
    except (json.JSONDecodeError, TypeError) as exc:
        raise _RuntimePinMismatch from exc
    url = direct_url.get("url") if isinstance(direct_url, dict) else None
    vcs_info = direct_url.get("vcs_info") if isinstance(direct_url, dict) else None
    if not isinstance(url, str) or not isinstance(vcs_info, dict):
        raise _RuntimePinMismatch
    parsed = urlsplit(url.removeprefix("git+"))
    repository = f"{parsed.netloc}/{parsed.path.strip('/').removesuffix('.git')}".lower()
    if (
        repository != _EXPECTED_REPOSITORY
        or vcs_info.get("vcs") != "git"
        or vcs_info.get("commit_id") != expected_commit
    ):
        raise _RuntimePinMismatch


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--expected-commit", required=True)
    args = parser.parse_args()
    try:
        _verify_installed_runtime(args.expected_commit)
        request = json.load(sys.stdin, parse_constant=lambda _value: (_ for _ in ()).throw(ValueError()))
        if not isinstance(request, dict):
            raise TypeError("request must be an object")
        from worldkernel.adapters.exchange import execute_exchange
        from worldkernel.core.registry import register_world
        from worldkernel.examples.bootstrap import register_builtin_worlds

        from mirrormind.domains.retail.worldkernel_policy_world import (
            register_mirrormind_policy_world,
        )

        register_builtin_worlds()
        register_mirrormind_policy_world(register_world)
        result = execute_exchange(request, require_registered_version=True)
        sys.stdout.write(json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False))
        return 0
    except _RuntimeMissing:
        sys.stderr.write("WORLDKERNEL_NOT_INSTALLED\n")
    except _RuntimePinMismatch:
        sys.stderr.write("WORLDKERNEL_PIN_MISMATCH\n")
    except Exception:  # noqa: BLE001 - keep third-party tracebacks and input out of stderr
        sys.stderr.write("WORLDKERNEL_EXECUTION_FAILED\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
