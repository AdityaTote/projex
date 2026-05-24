# Architecture Overview — Projex

## Overview

Projex is a conversational AI platform that connects users to their Zoho Projects workspace through natural language. Every user authenticates with their own Zoho account. The backend uses a multi-agent LangGraph system to classify and handle each message — one agent for read operations, another for write operations.

---

## System Layers

```
┌─────────────────────────────────────┐
│         Next.js Frontend            │
│   Login UI  ·  Chat Interface       │
└────────────────┬────────────────────┘
                 │ HTTP + JWT cookie
┌────────────────▼────────────────────┐
│         FastAPI Backend             │
│  /auth/login  ·  /auth/callback     │
│  /chat                              │
│  JWT middleware on every request    │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│       LangGraph Agent Graph         │
│                                     │
│  load_context → load_project        │
│       → router                      │
│       → query_agent / action_agent  │
│       → end                         │
└──────────┬──────────────┬───────────┘
           │              │
┌──────────▼──────┐  ┌────▼──────────┐
│  Zoho Projects  │  │  PostgreSQL   │
│  REST API       │  │  DB           │
└─────────────────┘  └───────────────┘
```

---

## Component Breakdown

### Frontend (Next.js)

- Login page triggers Zoho OAuth redirect
- Chat interface sends messages to `POST /chat`
- Handles two response types:
  - Normal response → render as bot message
  - HIL confirmation → render confirm/cancel buttons

---

### Backend (FastAPI)

Three endpoints:

| Endpoint | Purpose |
|----------|---------|
| `GET /auth/login` | Redirects user to Zoho OAuth page |
| `GET /auth/callback` | Receives auth code, exchanges for tokens, saves user to DB, sets JWT cookie |
| `POST /chat` | Receives user message, invokes LangGraph, returns response |

JWT middleware runs on every request to `/chat` — decodes the cookie and identifies the current user.

---

### LangGraph Agent Graph

The core of Projex. A stateful graph with 5 nodes:

```
START
  ↓
load_context      ← load user info, tokens, session, past messages from DB
  ↓
load_project      ← check if project selected; interrupt() to ask user if not
  ↓
router            ← LLM classifies message as "query" or "action"
  ↓           ↓
query_agent   action_agent
                  ↓
              HIL confirmation (interrupt inside tool)
  ↓           ↓
            END
```

#### Node Responsibilities

| Node | LLM | Tools | Job |
|------|-----|-------|-----|
| `load_context` | no | no | DB read → inject into state |
| `load_project` | no | list_projects | fetch projects, interrupt() if none selected |
| `router` | yes | no | classify message as query or action |
| `query_agent` | yes | yes (5 tools) | ReAct loop for read operations |
| `action_agent` | yes | yes (3 tools) | ReAct loop for write operations + HIL |

---

### Agent State

```python
class AgentState(TypedDict):
    user_id: str
    session_id: str
    access_token: str
    portal_id: str
    messages: Annotated[list, add_messages]
    route: Optional[Route]
    current_project_id: Optional[str]
    current_project_name: Optional[str]
    long_term_context: Optional[dict]
```

State persists across turns in a session via LangGraph's `MemorySaver` checkpointer using `session_id` as the `thread_id`.

---

### Tool Separation

Strict separation — agents never share tools.

| Agent | Tools |
|-------|-------|
| Query Agent | `list_projects`, `list_tasks`, `get_task_details`, `list_project_members`, `get_task_utilisation` |
| Action Agent | `create_task`, `update_task`, `delete_task` |

Tools are created via closures — `access_token` and `portal_id` are injected at build time and never passed as LLM arguments:

```python
def make_query_tools(access_token: str, portal_id: str) -> list:
    @tool
    def list_projects(page: int = 1, per_page: int = 20) -> dict:
        # access_token already in scope
        ...
    return [list_projects, ...]
```

---

### Human-in-the-Loop (HIL)

Write operations always require explicit user confirmation before executing. This is implemented via LangGraph's `interrupt()` inside the action tools — not in the agent node itself.

```
action_agent calls tool
      ↓
tool calls interrupt() → graph pauses → response returned to frontend
      ↓
frontend renders confirmation dialog
      ↓
user clicks Confirm → POST /chat with { confirmed: true }
user clicks Cancel  → POST /chat with { confirmed: false }
      ↓
graph resumes via Command(resume={"approved": True/False})
      ↓
executes or cancels cleanly
```

---

### Memory

| Type | Implementation | Scope |
|------|---------------|-------|
| Short-term | LangGraph `AgentState` + `MemorySaver` | Current session only |
| Long-term | PostgreSQL `user_memory` table | Persists across sessions |

- On session start: `load_context` reads DB and injects last project and preferences into state
- During session: checkpointer maintains state across turns using `session_id`
- On turn end: state is saved back to DB (current project, messages)

---

### Database Schema

```
users              ← zoho user id, email, name, portal_id
user_tokens        ← access_token, refresh_token, expires_at
user_memory        ← last_project_id, last_project_name, preferred_view
sessions           ← session_id, user_id, project_id, project_name
session_messages   ← session_id, role, content
```

---

### LLM

```
Model   : gemini-3.1-flash-lite
Provider: Google Gemini via langchain-google-genai
Config  : temperature=0, convert_system_message_to_human=True
```

All prompts use XML tags for structure and deterministic parsing:
- Router returns `<route>query</route>` or `<route>action</route>`
- Query Agent responds in `<response><message/><data/></response>`
- Action Agent responds in `<response><message/><action/><payload/></response>`

---

### OAuth Flow

```
1. User clicks Login with Zoho
2. Frontend redirects to GET /auth/login
3. Backend redirects to Zoho OAuth page
4. User logs in and grants permission
5. Zoho redirects to GET /auth/callback?code=xxx
6. Backend exchanges code for access + refresh tokens
7. Backend calls GET /api/v3/portals → extracts user info + portal_id
8. User, token, portal saved to PostgreSQL
9. JWT issued → set as HTTP-only cookie
10. Redirect to /chat
```

Token refresh happens silently before every Zoho API call by checking `expires_at` in `user_tokens`.