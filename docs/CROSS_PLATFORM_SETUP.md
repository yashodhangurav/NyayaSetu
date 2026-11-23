# Cross-Platform Setup (macOS, Linux, Windows)

This is the canonical local-development command reference. The backend and
frontend run on macOS/Linux and Windows with the same application code; only
shell commands, virtualenv activation paths and process-kill commands differ.

> [!IMPORTANT]
> The root `venv/` directory is **generated locally per operating system** and
> is git-ignored. Never commit a virtualenv: it contains absolute interpreter
> paths and platform-specific binaries. An old macOS-only `venv/` was removed
> from the repository for this reason.

## 1. Prerequisites

| Tool | macOS / Linux | Windows |
| :--- | :--- | :--- |
| Python | 3.12 (`python3.12`) | 3.12 (`py -3.12`) |
| Node.js | 22+ | 22+ |
| PostgreSQL | 16 + `postgis`, `vector`, `uuid-ossp` | 16 + `postgis`, `vector`, `uuid-ossp` (or a Supabase project) |

Python 3.12 is the tested target. Python 3.13 can be selected with
`--python` in the bootstrap script but is not the pinned runtime.

## 2. One-command bootstrap (either OS)

From the repository root, with any Python 3.12+ interpreter:

```bash
python backend/scripts/bootstrap_env.py
```

This creates `venv/` at the repository root, installs
`backend/requirements.txt`, and copies `backend/.env.example` to
`backend/.env` when absent. Useful overrides:

```bash
python backend/scripts/bootstrap_env.py --python /path/to/python3.12
python backend/scripts/bootstrap_env.py --venv /custom/venv/path
python backend/scripts/bootstrap_env.py --skip-install
```

Afterwards, edit `backend/.env` (at minimum `DATABASE_URL`) and run the
migrations and server as shown below.

## 3. Manual setup

Commands are shown from the repository root unless a step says otherwise.

### macOS / Linux

```bash
# Create and activate the shared virtualenv
python3.12 -m venv venv
source venv/bin/activate

cd backend
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env          # then edit DATABASE_URL if needed
alembic upgrade head          # requires a reachable PostgreSQL instance
python run.py                 # http://localhost:8000
```

### Windows (PowerShell)

```powershell
# Create and activate the shared virtualenv
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1

cd backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env    # then edit DATABASE_URL if needed
alembic upgrade head           # requires a reachable PostgreSQL instance
python run.py                  # http://localhost:8000
```

If PowerShell blocks script activation, run
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use the
bootstrap script instead (it does not need activation).

### Running from the repository root

`run.py` now adds `backend/` to `sys.path`, so these work without `cd backend`:

```bash
python backend/run.py                                      # macOS / Linux
python backend\run.py                                      # Windows PowerShell
```

## 4. Dev launcher scripts

| Platform | Command |
| :--- | :--- |
| macOS / Linux | `bash backend/scripts/run_dev.sh` |
| Windows PowerShell | `powershell -ExecutionPolicy Bypass -File backend\scripts\run_dev.ps1` |

Both scripts activate an available virtualenv and then run `python run.py`
from `backend/`.

## 5. Verification

```bash
# macOS / Linux
cd backend && python scripts/verify_health.py

# Windows PowerShell
cd backend
python scripts\verify_health.py
```

`verify_health.py` first probes an already-running server on port 8000; it only
starts its own temporary uvicorn process when nothing is listening, so it will
not collide with a running dev server.

Useful endpoints:

* <http://127.0.0.1:8000/api/v1/health>
* <http://127.0.0.1:8000/docs>

Backend tests use in-memory SQLite and need no PostgreSQL service:

```bash
cd backend && pytest -v
```

## 6. Frontend (same commands on both platforms)

```bash
cd frontend
npm install
npm run dev        # predev.js clears port 3000 / stale Next.js lock
```

`npm run dev` proxies `/api/v1/:path*` to `http://localhost:8000`, so start the
backend first.

## 7. Troubleshooting

### Port 8000 already in use

```bash
# macOS / Linux
lsof -ti:8000 | xargs kill -9
```

```powershell
# Windows PowerShell
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue |
  Select-Object -ExpandProperty OwningProcess |
  ForEach-Object { Stop-Process -Id $_ -Force }
```

### Stale or cross-platform virtualenv

If the bootstrap script reports that `venv/` is missing its Python executable,
delete that directory and re-run the bootstrap. Do not copy a virtualenv
between macOS and Windows.

### Missing PostGIS / pgvector

Enable the extensions in PostgreSQL (`uuid-ossp`, `postgis`, `vector`) or use a
Supabase project where they are preinstalled, then re-run
`alembic upgrade head`.

## 8. Related documents

* [`../README.md`](../README.md) — project overview and quick start
* [`API.md`](API.md) — backend API reference
* [`DEVELOPMENT.md`](DEVELOPMENT.md) — operations and verification gates
* [`../AGENTS.md`](../AGENTS.md) — repository conventions
