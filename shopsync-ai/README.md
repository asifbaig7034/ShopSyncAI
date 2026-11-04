# ShopSync AI - UC-2 Owner-to-Orchestrator prototype

This repository implements **only UC-2, Send Request to Orchestrator**. The
Business Owner types a natural-language request into a small React chat.
FastAPI checks a local demo owner token, identifies relevant enabled handlers,
obtains sample data-backed results, and displays one combined answer. Owner
requests, responses, approval proposals, and agent events are recorded in the
shared data layer. Real account login, customer WhatsApp, order execution,
shipping, payments, social publishing, and the rest of UC-1/UC-3-UC-10 are not
implemented here.

The two working **demo** domains are Customer & Commerce (saved sample orders)
and Supply Chain & Operations (sample products and stock). The eventual architecture
has six specialist agents. A report from a demo agent is still based on stored
sample records; it is not a live external integration.

## Requirements

- Python 3.11+ and Node.js compatible with the installed Vite release.
- Docker is **optional**; it is used only if you want persistent local MongoDB.
- A Gemini key is **optional for the local rules demo**, but the final SRS UC-2
  requires a configured LLM Service in its normal flow.

## Run locally (Linux/macOS)

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
cp .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the generated token into the `SHOPSYNC_DEMO_OWNER_TOKEN` line of `.env`.
Do **not** commit `.env`. For the simplest demo leave `MONGODB_URI` empty; the
server automatically seeds an **in-memory** Mongo-compatible sample database,
whose contents disappear when the backend restarts. Then start FastAPI:

```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

Open `http://127.0.0.1:8000/docs` to inspect the API. In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal (typically `http://localhost:5173`).
Paste the **demo token** into the owner's local sign-in field. It is held only
in the open browser tab, not added to the frontend build or its environment.

## Run locally (Windows PowerShell)

From the project root:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
Copy-Item .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Put the generated value in `.env` as above. In the first terminal:

```powershell
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

In another terminal:

```powershell
cd frontend
npm install
npm run dev
```

If PowerShell blocks virtual-environment activation, use
`.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt` and
`.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload`
instead of changing your computer's script-execution policy.

## Try UC-2

Use **fictional** prompts with the seeded demo shop:

1. `Show products and stock` - routes to the available product and inventory
   handlers and combines results obtained from the sample database.
2. `Show recent orders` - reads the synthetic order sample.
3. `Show stock and orders` - returns two domain results in one reply.
4. `Show me` - requests clarification; your next reply uses the same
   conversation ID.
5. `Publish a social post` - tells you that the Social Media Agent belongs to a
   later use case; it must not claim a post was published.

To demonstrate FR-05 event coordination, open `http://127.0.0.1:8000/docs`,
choose **POST /api/owner/demo-events/low-stock**, click **Try it out**, and
enter `Bearer YOUR_TOKEN` in that operation's `authorization` header field.
The operation reads the fictional low-stock product and calls a read-only
Customer & Commerce event handler. **GET /api/owner/demo-events** shows the
stored event and agent response. Repeating the POST reuses its event ID, so
it does not create a second event or reprocess an acknowledged one. This is a
simulation: it does not notify a live customer or change stock.

The response identifies its mode. **Local rules demo** means no AI provider
answered the request; this is a runnable prototype, **not full SRS UC-2
completion**. No action that changes a price, issues a refund, or publishes a
post is executed from chat. Proposals remain pending for an owner approval
flow to be completed in the relevant later use case.

## Optional free-tier LLM for fictional demo prompts

Google currently lists free input/output usage for
[`gemini-3.5-flash-lite`](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite),
subject to your project and usage limits; check the
[official pricing](https://ai.google.dev/gemini-api/docs/pricing) and your AI
Studio quota. To test the adapter, create a Gemini API key in Google AI
Studio, then set these **server-side** values in `.env`:

```dotenv
GEMINI_API_KEY=your-own-key
GEMINI_MODEL=gemini-3.5-flash-lite
GEMINI_SYNTHETIC_DEMO=true
```

Restart FastAPI after changing `.env`. Never put the key in `frontend/.env`,
`VITE_` variables, the chat box, or Git. The adapter classifies intent; product
facts and agent outcomes still come from the shared database.

**Free Gemini usage is restricted to fictional/synthetic owner prompts.**
[Google's unpaid-service terms](https://ai.google.dev/gemini-api/terms)
explicitly prohibit submitting sensitive, confidential, or personal content
and say submitted content may be used to improve products or reviewed by
people. The adapter rejects some obvious personal-data patterns, but that
filter cannot guarantee privacy. Do not submit real customer conversations,
phone numbers, addresses, order details or confidential business information
through the free-tier demo. A real deployment requires an appropriate provider
plan and a separate privacy review.

## Optional durable MongoDB history

The zero-setup in-memory demo resets on backend restart. To persist data locally
if Docker is installed:

```bash
docker compose up -d mongo
```

Set `MONGODB_URI=mongodb://localhost:27017` in `.env`, restart the backend, and
seed **synthetic** examples with:

```bash
python -m backend.scripts.seed_demo
```

The application does not silently switch to an in-memory database if your
configured MongoDB server is unavailable; fix the connection or return to an
explicit demo configuration instead. This development Compose service binds
MongoDB to localhost only and does not provide production authentication.

## Verify the backend

```bash
python -m pytest -q backend/tests
```

See [UC-2 SRS mapping](docs/uc2-srs-mapping.md) for which requirement is met
by each module and which requirements remain for later implementation.

## Complete team file structure

This repository includes every file in the approved project layout. Only **UC-2 is implemented**; the other use-case source, test, frontend, Docker and future documentation files are intentionally **empty (0 bytes)** for your teammates to implement. Empty routes/pages are **not registered** in the FastAPI or React entry points, so the existing UC-2 demo continues to run. Keep `backend/requirements.txt`: the blank `backend/pyproject.toml` is a placeholder, not an installation file. Add approved SRS and diagrams to `docs/srs/` and `docs/diagrams/` yourself after deciding repository visibility. Never commit `.env`, real credentials, `.venv` or `node_modules`.
