#!/usr/bin/env python3
"""
Local validation helper for OMNIA-VALIDATION.

This helper prioritizes the canonical sibling OMNIA checkout and prevents
accidental package shadowing during cross-repository tests.
"""

import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKDIR = ROOT.parent
OMNIA_DIR = WORKDIR / "OMNIA"
LIMIT_DIR = WORKDIR / "omnia-limit"


def run(cmd, env=None):
    print("$", " ".join(str(x) for x in cmd))
    return subprocess.run(cmd, cwd=str(ROOT), text=True, env=env).returncode


def main():
    env = os.environ.copy()
    env["OMNIA_SOURCE_DIR"] = str(OMNIA_DIR)

    priority = [
        str(OMNIA_DIR),
        str(LIMIT_DIR),
    ]

    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = os.pathsep.join([p for p in priority if Path(p).exists()] + ([existing] if existing else []))

    status = 0

    for dep in [OMNIA_DIR, LIMIT_DIR]:
        if dep.exists() and (dep / "pyproject.toml").exists():
            status |= run([sys.executable, "-m", "pip", "install", "-e", str(dep)], env=env)

    if (ROOT / "pyproject.toml").exists():
        status |= run([sys.executable, "-m", "pip", "install", "-e", "."], env=env)

    status |= run([sys.executable, "-m", "pytest", "-q"], env=env)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
