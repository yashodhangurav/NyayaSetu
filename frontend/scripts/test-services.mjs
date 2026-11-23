import assert from "node:assert/strict";

// NEXT_PUBLIC_ variables are eligible for inclusion in the browser bundle.
for (const name of ["NEXT_PUBLIC_JWT_SECRET", "NEXT_PUBLIC_DATABASE_URL"]) {
  assert(!process.env[name], `Remove ${name} from the frontend environment`);
}
console.log("Frontend environment checks passed.");
