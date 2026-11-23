# Frontend

The Next.js 16 client uses React 19, TypeScript and Tailwind CSS. Run npm commands from `frontend/`. [Setup and commands](CROSS_PLATFORM_SETUP.md) cover local development. The predev hook clears the dev lock and frees port 3000.

## Where to make changes

| Area | Location |
| --- | --- |
| App Router pages and layouts | [src/app](../frontend/src/app/) |
| Authenticated dashboard shell and feature pages | [src/app/dashboard](../frontend/src/app/dashboard/) |
| Dashboard controls, dialogs and shared UI | [src/components/dashboard](../frontend/src/components/dashboard/) |
| Editorial content and development fixtures | [src/data](../frontend/src/data/) |
| Typed dashboard requests | [src/services/dashboard](../frontend/src/services/dashboard/) |
| Colors, typography and shared styles | [globals.css](../frontend/src/app/globals.css) |

The [Next.js rewrite](../frontend/next.config.ts) uses server-side `BACKEND_API_URL`, defaulting to `http://127.0.0.1:8000`. Use the [API client](../frontend/src/lib/api-client.ts) for live operations. Some workflows use local data or simulate a result. Check the specific service before relying on server persistence.

## Chat and public assets

The [chat page](../frontend/src/app/dashboard/chat/page.tsx) sends messages to the [legal assistant](AI_AND_RAG.md). Replies show the short answer, deadline when available, and numbered actions. The reader can expand cited explanations, documents and missing facts. Keep error recovery and short greetings available when changing the answer layout.

The [homepage canvas](../frontend/src/components/3d/lady-justice-canvas.tsx) loads `/models/lady-justice/model.glb` on the client. Legacy asset URLs are served through Next.js rewrites. Preserve existing public paths when moving assets.
