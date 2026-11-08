#!/usr/bin/env node

/**
 * Pre-dev script: Automatically frees port 3000 and clears stale Next.js dev lockfiles
 * so `npm run dev` never throws "Port 3000 is in use" or "Another next dev server is already running".
 */

const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

function cleanup() {
  // 1. Remove stale Next.js lockfile if present
  const lockPath = path.join(process.cwd(), ".next", "dev", "lock");
  try {
    if (fs.existsSync(lockPath)) {
      fs.unlinkSync(lockPath);
    }
  } catch {
    // Ignore if file was already removed
  }

  // 2. Kill any lingering processes on port 3000
  try {
    let pids = [];
    if (process.platform === "win32") {
      const output = execSync("netstat -ano | findstr :3000", { encoding: "utf8" });
      pids = output
        .split("\n")
        .map((line) => line.trim().split(/\s+/).pop())
        .filter((pid) => pid && !isNaN(Number(pid)));
    } else {
      const output = execSync("lsof -ti:3000 2>/dev/null", { encoding: "utf8" });
      pids = output
        .split("\n")
        .map((p) => p.trim())
        .filter(Boolean);
    }

    const currentPid = String(process.pid);
    for (const pid of pids) {
      if (pid && pid !== currentPid) {
        try {
          process.kill(Number(pid), "SIGKILL");
        } catch {
          // Process already ended
        }
      }
    }
  } catch {
    // No process was using port 3000
  }
}

cleanup();

