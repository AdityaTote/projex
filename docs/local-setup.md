# Local Setup — Projex

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) + [Docker Compose](https://docs.docker.com/compose/install/)
- [uv](https://docs.astral.sh/uv/) (Python package manager) — for local backend dev only
- [Bun](https://bun.sh/) — for local frontend dev only
- A [Zoho Developer Console](https://api-console.zoho.com/) account
- A [Google AI Studio](https://aistudio.google.com/) account for Gemini API key

---

## 1. Clone the Repository

```bash
git clone https://github.com/AdityaTote/projex.git
cd projex
```

---

## 2. Zoho OAuth Configuration

Before running anything, register your app on Zoho.

1. Go to [Zoho Developer Console](https://api-console.zoho.com/)
2. Click **Add Client** → choose **Web Based**
3. Fill in:
   - **Client Name**: Projex
   - **Homepage URL**: `http://localhost:3000`
   - **Authorized Redirect URIs**: `http://localhost:3000/auth/callback`
4. Click **Create**
5. Copy the **Client ID** and **Client Secret**

### Base URL by region

| Region | ZOHO_BASE_URL |
|--------|--------------|
| US | `https://accounts.zoho.com` |
| IN | `https://accounts.zoho.in` |
| EU | `https://accounts.zoho.eu` |
| AU | `https://accounts.zoho.com.au` |

---

## 3. Configure Environment

```bash
cp backend/.env.example backend/.env
```

Open `backend/.env` and fill in:

```env
# JWT
JWT_SECRET=your-random-secret-string
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=1440

# Zoho OAuth
ZOHO_CLIENT_ID=your-zoho-client-id
ZOHO_CLIENT_SECRET=your-zoho-client-secret
ZOHO_ACCESS_TYPE=offline
ZOHO_REDIRECT_URI=http://localhost:3000/auth/callback
ZOHO_BASE_URL=https://accounts.zoho.in
ZOHO_SCOPE=ZohoProjects.portals.READ,ZohoProjects.projects.ALL,ZohoProjects.tasks.ALL,ZohoProjects.users.READ,ZohoProjects.timesheets.READ

# Database — must match docker-compose.yml
DB_HOST=projex-postgres
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=projex

# CORS
CORS_ALLOW_ORIGINS=http://localhost:3000
CORS_ALLOW_METHODS=*
CORS_ALLOW_HEADERS=*
CORS_ALLOW_CREDENTIALS=true

# Gemini
GOOGLE_API_KEY=your-google-api-key
```

> **Note:** `DB_HOST` must be `projex-postgres` (the Docker container name), not `localhost`, when running via Docker.

---

## 4. Run with Docker

### Start all services

```bash
docker compose up --build
```

This starts three containers in order:

| Container | Role |
|-----------|------|
| `projex-postgres` | PostgreSQL 15 database |
| `projex-migrate` | Runs SQL migrations then exits |
| `projex-backend` | FastAPI backend on port 8080 |

### Stop all services

```bash
docker compose down
```

### Stop and remove volumes (wipes DB)

```bash
docker compose down -v
```

---

## 5. Backend Setup (local dev without Docker)

If you prefer to run the backend natively instead of using Docker, you can use `uv`:

```bash
cd backend
uv sync
uv run fastapi dev app/main.py --port 8080
```

---

## 6. Frontend Setup (local dev)

The frontend is not yet wired into Docker Compose. Run it locally:

```bash
cd frontend
cp .env.example .env
```

```env
NEXT_PUBLIC_API_URL=http://localhost:8080
```

```bash
bun install
bun dev
```

Frontend runs at `http://localhost:3000`.

---

## 7. Verify Everything is Running

| Service | URL |
|---------|-----|
| Backend API | `http://localhost:8080` |
| API Docs (Swagger) | `http://localhost:8080/docs` |
| Health check | `http://localhost:8080/ready` |
| Frontend | `http://localhost:3000` |

Open `http://localhost:3000`, click **Login with Zoho**, and complete the OAuth flow.

---

## Project Structure

```
projex/
├── backend/
│   ├── app/               ← FastAPI app + LangGraph agents
│   ├── main.py
│   ├── .env
│   ├── .env.example
│   └── pyproject.toml
├── docker/
│   ├── api.dockerfile
│   └── web.dockerfile
├── docker-compose.yml
├── frontend/
│   ├── src/
│   ├── .env
│   └── package.json
├── migrations/            ← Raw SQL migrations (migrate/migrate)
│   ├── *.up.sql
│   └── *.down.sql
└── scripts/
    └── start_script.sh
```

---

## Common Issues

**Backend not starting — `service_completed_successfully` wait**
The backend waits for migrations to finish. If migrations fail, check that `DB_*` values match the postgres container config.

**`invalid_redirect_uri` from Zoho**
`ZOHO_REDIRECT_URI` in `.env` must exactly match the redirect URI registered in Zoho Developer Console — including the port (`8080`).

**`DB_HOST=localhost` connection refused inside Docker**
Inside Docker, services talk to each other by container name. Use `DB_HOST=projex-postgres`, not `localhost`.

**Gemini API error**
Make sure `GOOGLE_API_KEY` is valid and the Generative Language API is enabled in your Google Cloud project.

**Port already in use**
Override default ports using environment variables before running compose:
```bash
POSTGRES_PORT=5433 AI_PORT=8081 docker compose up
```