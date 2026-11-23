"""Bootstrap a portable local development environment for the NyayaSetu backend.

The script works on macOS, Linux and Windows. It creates a fresh virtual
environment at the repository root (``venv/``), installs the pinned backend
requirements, and creates ``backend/.env`` from the template when missing.

Run it from any directory (the repository root is discovered automatically):

    python backend/scripts/bootstrap_env.py
    python backend/scripts/bootstrap_env.py --python /path/to/python3.12
    python backend/scripts/bootstrap_env.py --skip-install
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

BACKEND_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_DIR.parent
DEFAULT_VENV = REPO_ROOT / "venv"
IS_WINDOWS = os.name == "nt"


def python_version(executable: List[str]) -> Tuple[int, int]:
    """Return ``(major, minor)`` for an interpreter or launcher command."""
    code = "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')"
    result = subprocess.run(
        [*executable, "-c", code],
        capture_output=True,
        text=True,
        check=True,
    )
    major, minor = result.stdout.strip().split(".", 1)
    return int(major), int(minor)


def resolve_python(explicit: str | None) -> List[str]:
    """Find a suitable Python 3.12+ interpreter for the current platform."""
    candidates: List[List[str]] = []

    if explicit:
        candidates.append([explicit])
    if IS_WINDOWS:
        candidates.append(["py", "-3.12"])
    elif shutil.which("python3.12"):
        candidates.append(["python3.12"])
    if shutil.which("python3"):
        candidates.append(["python3"])
    candidates.append([sys.executable])

    for candidate in candidates:
        try:
            version = python_version(candidate)
        except (OSError, subprocess.CalledProcessError, ValueError):
            continue
        if version >= (3, 12):
            if version != (3, 12):
                print(
                    f"Note: using Python {version[0]}.{version[1]}; "
                    "Python 3.12 is the recommended runtime."
                )
            return candidate

    raise SystemExit(
        "Python 3.12 or newer is required. Install Python 3.12 and re-run, "
        "or pass an explicit interpreter with --python PATH."
    )


def venv_python(venv: Path) -> Path:
    """Return the interpreter path inside a virtualenv on the current OS."""
    return venv / ("Scripts/python.exe" if IS_WINDOWS else "bin/python")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--venv",
        type=Path,
        default=DEFAULT_VENV,
        help=f"Virtual environment location (default: {DEFAULT_VENV})",
    )
    parser.add_argument(
        "--python",
        default=None,
        help="Explicit Python interpreter to use (default: auto-detect 3.12)",
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Create the virtualenv but do not install requirements",
    )
    parser.add_argument(
        "--no-env",
        action="store_true",
        help="Do not create backend/.env from backend/.env.example",
    )
    args = parser.parse_args()

    venv = args.venv.expanduser().resolve()
    interpreter = venv_python(venv)

    if venv.exists() and not interpreter.exists():
        raise SystemExit(
            f"{venv} exists but is not a usable virtualenv for this OS "
            f"(missing {interpreter}). Remove that directory or use --venv PATH."
        )

    if interpreter.exists():
        print(f"Reusing existing virtual environment: {venv}")
    else:
        base_python = resolve_python(args.python)
        print(f"Creating virtual environment at {venv} with {' '.join(base_python)}")
        subprocess.check_call([*base_python, "-m", "venv", str(venv)])

    if not args.skip_install:
        print("Installing pinned backend requirements...")
        subprocess.check_call([str(interpreter), "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call(
            [
                str(interpreter),
                "-m",
                "pip",
                "install",
                "-r",
                str(BACKEND_DIR / "requirements.txt"),
            ]
        )

    if not args.no_env:
        env_file = BACKEND_DIR / ".env"
        if env_file.exists():
            print("backend/.env already exists; leaving it unchanged.")
        else:
            shutil.copyfile(BACKEND_DIR / ".env.example", env_file)
            print("Created backend/.env from backend/.env.example.")

    scripts_dir = venv / ("Scripts" if IS_WINDOWS else "bin")
    activate = scripts_dir / ("Activate.ps1" if IS_WINDOWS else "activate")
    print("\nSetup complete. Next steps:")
    if IS_WINDOWS:
        print(f"  & '{activate}'")
    else:
        print(f"  source {activate}")
    print(f"  cd {BACKEND_DIR}")
    print("  alembic upgrade head   # once PostgreSQL is reachable")
    print("  python run.py          # starts http://localhost:8000")


if __name__ == "__main__":
    main()
