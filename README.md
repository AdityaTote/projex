# Projex

> Talk to your Zoho Projects in natural language.

Projex is a conversational AI assistant for Zoho Projects. Instead of navigating the Zoho UI, users interact with their projects and tasks through a chat interface — listing tasks, creating them, updating assignees, or checking who has the most work this month, all through plain English.

Every user authenticates with their own Zoho account. No shared credentials, no admin tokens.

---

## Features

- **Natural language chat** — ask questions or give instructions in plain English
- **Read operations** — list projects, view tasks, check members, get utilisation reports
- **Write operations** — create, update, and delete tasks with human confirmation before every action
- **Per-user OAuth** — each user logs in with their own Zoho account
- **Session memory** — agent remembers context within a session ("show tasks for the first one")
- **Persistent memory** — picks up where you left off on next login

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js |
| Backend | FastAPI |
| Agent | LangGraph + LangChain |
| LLM | Gemini 3.1 Flash Lite |
| Database | PostgreSQL 15 |
| Auth | Zoho OAuth 2.0 + JWT |
| Migrations | migrate/migrate |
| Infra | Docker + Docker Compose |

---

## Quick Start

```bash
git clone https://github.com/your-username/projex.git
cd projex

cp backend/.env.example backend/.env
# fill in ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, GOOGLE_API_KEY

docker compose up --build
```

Backend runs at `http://localhost:8080`. Frontend runs separately — see [docs/local-setup.md](docs/local-setup.md).

---

## Project Structure

```
projex/
├── backend/               ← FastAPI + LangGraph agents
├── frontend/              ← Next.js chat UI
├── migrations/            ← SQL migrations
├── docker/                ← Dockerfiles
├── docker-compose.yml
├── docs/
│   ├── local-setup.md         ← setup guide
│   ├── architecture-overview.md
│   └── how-it-works.md
└── README.md
```

---

## How It Works

User sends a message → LangGraph classifies it as a read or write → routes to the appropriate agent → agent calls Zoho API tools → returns response.

Write operations always pause for explicit user confirmation before executing.

See [docs/how-it-works.md](docs/how-it-works.md) for the full flow.

---

## Architecture

```
Next.js
   ↓ HTTP + JWT
FastAPI
   ↓
LangGraph Graph
   load_context → load_project → router → query_agent / action_agent
   ↓
Zoho Projects REST API + PostgreSQL
```

See [docs/architecture-overview.md](docs/architecture-overview.md) for the full breakdown.

---

## Documentation

| Doc | Description |
|-----|-------------|
| [local-setup.md](docs/local-setup.md) | Prerequisites, Docker setup, Zoho OAuth config |
| [architecture-overview.md](docs/architecture-overview.md) | System design, agent graph, DB schema |
| [how-it-works.md](docs/how-it-works.md) | End-to-end flow, sample conversations |

---

## Known Limitations

- Only the first Zoho portal is used per account
- Bulk operations are not supported
- Write operations always require confirmation — HIL cannot be skipped
- Frontend Docker container is not yet wired into Docker Compose

---

## License

MIT