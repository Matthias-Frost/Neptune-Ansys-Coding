"""
Verify that this machine is set up to run the group's PyFluent scripts.

Usage (from the repo folder, with the .venv activated):
    python scripts/check_setup.py            # quick checks, does not start Fluent
    python scripts/check_setup.py --launch   # also starts Fluent, connects, and shuts it down

Paste the full output into your Setup checklist issue on GitHub.
"""

from __future__ import annotations

import argparse
import os
import platform
import re
import sys
import time
from importlib import metadata
from pathlib import Path

# ---- Our standard environment (keep in sync with README.md) -----------------
REQUIRED_PYTHON = (3, 10)
ANSYS_VERSION_CODE = "231"  # Ansys 2023 R1 -> AWP_ROOT231
PACKAGE = "ansys-fluent-core"
# -----------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
results: list[tuple[str, str, str]] = []  # (status, check name, detail)


def record(status: str, name: str, detail: str = "") -> None:
    results.append((status, name, detail))
    print(f"  [{status:<4}] {name}" + (f" -> {detail}" if detail else ""))


def pinned_version() -> str | None:
    """Read the ansys-fluent-core version pinned in requirements.txt."""
    req = REPO_ROOT / "requirements.txt"
    if not req.exists():
        return None
    for line in req.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        m = re.match(r"ansys[-_]fluent[-_]core\s*==\s*(\S+)", line, re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def check_system() -> None:
    print("\nSystem")
    if platform.system() == "Windows":
        record("PASS", "Operating system", platform.platform())
    else:
        record("WARN", "Operating system", f"{platform.platform()} (guide assumes Windows)")


def check_python() -> None:
    print("\nPython")
    ver = sys.version_info
    ver_str = f"{ver.major}.{ver.minor}.{ver.micro}"
    if (ver.major, ver.minor) == REQUIRED_PYTHON:
        record("PASS", "Python version", ver_str)
    else:
        want = ".".join(map(str, REQUIRED_PYTHON))
        record("FAIL", "Python version", f"{ver_str}, expected {want}.x (see SETUP.md Step 1/5)")

    bits = "64-bit" if sys.maxsize > 2**32 else "32-bit"
    record("PASS" if bits == "64-bit" else "FAIL", "Python build", bits)

    in_venv = sys.prefix != sys.base_prefix
    expected_venv = (REPO_ROOT / ".venv").resolve()
    if in_venv and Path(sys.prefix).resolve() == expected_venv:
        record("PASS", "Virtual environment", str(expected_venv))
    elif in_venv:
        record("WARN", "Virtual environment", f"active, but not this repo's .venv: {sys.prefix}")
    else:
        record("FAIL", "Virtual environment", "not active (SETUP.md Step 5: Activate.ps1)")


def check_pyfluent() -> bool:
    print("\nPyFluent")
    try:
        installed = metadata.version(PACKAGE)
    except metadata.PackageNotFoundError:
        record("FAIL", f"{PACKAGE} installed", "not found (SETUP.md Step 6)")
        return False

    pin = pinned_version()
    if pin is None:
        record("WARN", f"{PACKAGE} installed", f"{installed} (no pin found in requirements.txt)")
    elif "REPLACE" in pin.upper():
        record("WARN", f"{PACKAGE} installed", f"{installed} (repo lead hasn't pinned a version yet)")
    elif installed == pin:
        record("PASS", f"{PACKAGE} installed", f"{installed} (matches requirements.txt)")
    else:
        record("FAIL", f"{PACKAGE} installed", f"{installed}, but requirements.txt pins {pin}")

    try:
        import ansys.fluent.core  # noqa: F401
        record("PASS", "Import ansys.fluent.core")
        return True
    except Exception as exc:  # report any import problem, not just ImportError
        record("FAIL", "Import ansys.fluent.core", f"{type(exc).__name__}: {exc}")
        return False


def check_ansys() -> bool:
    print("\nAnsys install")
    found = sorted(k for k in os.environ if re.fullmatch(r"AWP_ROOT\d{3}", k))
    record("PASS" if found else "FAIL", "AWP_ROOT variables", ", ".join(found) or "none set")

    var = f"AWP_ROOT{ANSYS_VERSION_CODE}"
    root = os.environ.get(var)
    if not root:
        record("FAIL", var, "not set (SETUP.md Troubleshooting)")
        return False
    fluent_dir = Path(root) / "fluent"
    if fluent_dir.is_dir():
        record("PASS", var, root)
        return True
    record("FAIL", var, f"{root} has no 'fluent' folder (is Fluent installed?)")
    return False


def _server_healthy(session) -> bool:
    """Health check that works across PyFluent versions (the API was renamed over time)."""
    if hasattr(session, "is_server_healthy"):
        return bool(session.is_server_healthy())
    for attr in ("health_check", "health_check_service"):
        svc = getattr(session, attr, None)
        if svc is not None:
            serving = svc.is_serving
            return bool(serving() if callable(serving) else serving)
    raise RuntimeError("could not find a health-check method on this PyFluent session")


def check_launch() -> None:
    print("\nLaunch test (starting Fluent in the background; first launch can take 1-2 min)")
    import ansys.fluent.core as pyfluent

    session = None
    t0 = time.perf_counter()
    try:
        session = pyfluent.launch_fluent(mode="solver", processor_count=2)
        elapsed = time.perf_counter() - t0
        record("PASS", "Launch Fluent solver", f"{elapsed:.0f} s")
        healthy = _server_healthy(session)
        record("PASS" if healthy else "FAIL", "Fluent server responding", str(healthy))
    except Exception as exc:
        record("FAIL", "Launch Fluent solver", f"{type(exc).__name__}: {exc}")
    finally:
        if session is not None:
            try:
                session.exit()
                record("PASS", "Shut down Fluent")
            except Exception as exc:
                record("WARN", "Shut down Fluent", f"{type(exc).__name__}: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--launch", action="store_true", help="also start and stop Fluent")
    args = parser.parse_args()

    print("=" * 64)
    print("Ansys Automation - setup check")
    print(f"Repo: {REPO_ROOT}")
    print(f"Python executable: {sys.executable}")
    print("=" * 64)

    check_system()
    check_python()
    pyfluent_ok = check_pyfluent()
    ansys_ok = check_ansys()

    if args.launch:
        if pyfluent_ok and ansys_ok:
            check_launch()
        else:
            print("\nLaunch test skipped: fix the FAIL items above first.")
            record("FAIL", "Launch test", "skipped")

    fails = sum(1 for s, _, _ in results if s == "FAIL")
    warns = sum(1 for s, _, _ in results if s == "WARN")
    print("\n" + "=" * 64)
    if fails:
        print(f"{fails} FAILED, {warns} warning(s). Fix FAIL items and run again.")
    elif not args.launch:
        print(f"Quick checks passed ({warns} warning(s)). Now run with --launch.")
    else:
        print(f"ALL CHECKS PASSED ({warns} warning(s)).")
    print("=" * 64)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
