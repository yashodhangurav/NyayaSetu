"""Script to verify the live FastAPI server health endpoint."""

import sys
import time
from multiprocessing import Process
from pathlib import Path

import httpx

# Ensure backend directory is in sys.path (also needed by spawned Windows processes)
backend_dir = str(Path(__file__).resolve().parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

BASE_URL = "http://127.0.0.1:8000"


def run_server():
    # Make sure sys.path is set in child process
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    import uvicorn
    from app.main import app
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")


def probe(client: httpx.Client):
    """Return a health response, or None when no server is listening yet."""
    try:
        return client.get("/api/v1/health", timeout=5.0)
    except httpx.ConnectError:
        return None


def report(resp: httpx.Response) -> bool:
    """Print the probe result and return True when the API reports healthy."""
    print(f"Status Code: {resp.status_code}")
    print(f"Response JSON: {resp.json()}")

    healthy = resp.status_code == 200 and resp.json().get("status") == "healthy"
    if healthy:
        print(">>> VERIFICATION SUCCESSFUL: GET /api/v1/health returned 200 OK and healthy status!")
    else:
        print(">>> VERIFICATION FAILED: Unexpected response")
    return healthy


def main():
    with httpx.Client(base_url=BASE_URL, timeout=5.0) as client:
        resp = probe(client)
        if resp is not None:
            sys.exit(0 if report(resp) else 1)

        print("No server detected on port 8000; starting a temporary uvicorn process...")
        proc = Process(target=run_server, daemon=True)
        proc.start()
        try:
            for _ in range(20):
                time.sleep(0.5)
                resp = probe(client)
                if resp is not None:
                    sys.exit(0 if report(resp) else 1)
            print(">>> VERIFICATION FAILED: temporary server did not become ready")
            sys.exit(1)
        finally:
            proc.terminate()
            proc.join(timeout=2)


if __name__ == "__main__":
    main()
