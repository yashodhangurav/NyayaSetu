<!-- BEGIN:nextjs-agent-rules -->

## This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->

## Project-specific guidance

This is the NyayaSetu frontend, not a generic Next.js starter. Read the
repository-level [`../AGENTS.md`](../AGENTS.md) and
[`../docs/FRONTEND.md`](../docs/FRONTEND.md) before changing pages or data.

### What this app is

A public India-focused legal platform: marketing pages, an advocate directory, a
representative matter ledger, legal guides, and intake forms. The dashboard combines live API clients with development fixtures in `src/data/`.

### Commands

```bash
npm install
npm run dev      # predev clears port 3000 / stale lock, then Next.js on :3000
npm run lint
npm run build
npm run start
```

### Rules

- Preserve the visual system: warm paper palette, serif display type, mono
  labels, thin square borders, restrained motion. Tokens are inline hex values
  and in `src/app/globals.css`.
- `scripts/predev.js` intentionally kills whatever listens on port 3000. Do not
  remove it without replacing the behavior.
- Prefer server components for content. Use `"use client"` only for state,
  effects, or browser APIs.
- Keep the `dynamic(() => import(...), { ssr: false })` boundary around the 3D
  scene. Do not make the whole hero client-side just for Three.js.
- For pages that still use static data, if you migrate a page to the API,
  keep the static array until the API path is verified, then remove it and all
  its imports.
- Add remote image hosts to `next.config.ts` `images.remotePatterns` rather than
  disabling optimization.
- Do not add a client-side data library for public content that can be fetched
  on the server.
- `next dev` regenerates the block at the top of this file. Keep that block in
  commits; append project guidance below it.

### Content and compliance

- Canonical identity: NyayaSetu (न्यायसेतु), India, established 2026.
- Do not add or extend Chicago/Illinois "Ellery Kowal LLP" copy.
- Never remove the "not legal advice", "no advocate-client relationship", or BCI
  non-solicitation notices.
- Do not invent advocates, bar enrollments, case results, offices, phone
  numbers, or fees.
- Fixed-fee data is currently USD legacy content. Do not present it as approved
  India pricing.
- Keep claim language factual and non-comparative.

### API integration

- Contract: [`../docs/API.md`](../docs/API.md).
- Use the configured server-side `BACKEND_API_URL` rewrite and the shared API client.
- Preserve established form-field mappings; normalize
  `upcoming-30d` → `standard-30d` and `none-yet` → `exploratory`.
- Treat `202` from newsletter as success and `201` from intake as created.
- Surface `error.details` for validation failures and `requestId` for support.
- Handle `429` explicitly.
- Never send privileged material before conflict clearance; keep the warning.

### Verification

```bash
npm run lint
npm run build
```

There is no test suite yet. If you add one, document the command here and in
`../docs/DEVELOPMENT.md`.
