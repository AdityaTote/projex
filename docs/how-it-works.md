# How Projex Works

## What is Projex?

Projex is a conversational AI assistant for Zoho Projects. Instead of navigating the Zoho UI, users interact with their projects and tasks through a natural language chat interface. Every user logs in with their own Zoho account — there are no shared credentials.

---

## End-to-End Flow

### 1. Login

The user opens Projex and clicks **Login with Zoho**.

- They are redirected to Zoho's login page
- After granting permission, Zoho sends an authorization code to Projex
- Projex exchanges that code for an `access_token` and `refresh_token`
- User info and portal ID are fetched from Zoho and saved to the database
- A JWT is issued and stored as an HTTP-only cookie
- The user lands on the chat page

From this point on, every request to `/chat` is authenticated via the JWT cookie.

---

### 2. Session Start — Project Selection

When the user sends their first message, the graph runs `load_context` first:

- Loads the user's `access_token`, `portal_id`, and any saved session context from PostgreSQL
- If a `current_project_id` exists (returning user), it is injected into state and the session continues immediately
- If no project is selected (new user or new session), the `load_project` node fetches all projects from Zoho and **pauses** via `interrupt()`, asking the user to select one

```
Bot: "Please select a project to get started:"
     1. Backend API
     2. Mobile App
     3. Marketing Site

User: "1"

Bot: "You're now working on Backend API. What would you like to do?"
```

The selected project is saved to the database and persists on the next login.

---

### 3. Normal Chat Turn

Once a project is selected, every message goes through this flow:

```
User message
     ↓
router (LLM classifies as "query" or "action")
     ↓                    ↓
query_agent          action_agent
     ↓                    ↓
Zoho API call     HIL confirmation
     ↓                    ↓
response          execute or cancel
```

#### Router

A single LLM call classifies the message:
- **query** — anything that reads data (show, list, fetch, who, how many)
- **action** — anything that writes data (create, update, delete, assign)

The router returns only `<route>query</route>` or `<route>action</route>`. Nothing else.

#### Query Agent

Handles all read operations. Uses a ReAct loop — the LLM decides which tool to call, calls it, reads the result, and either calls another tool or returns a final answer.

Example:
```
User: "Who has the most tasks this month?"

query_agent → calls get_task_utilisation
           → formats result
           → responds with summary
```

The agent remembers context within the session. If the user says "show tasks for the first one", the agent uses the project mentioned earlier in the conversation.

#### Action Agent

Handles all write operations. Same ReAct loop, but every tool call pauses for user confirmation before executing.

Example:
```
User: "Create a task called Fix Login Bug"

action_agent → prepares create_task call
             → interrupt() fires
             → graph pauses

Bot: "I'm about to create:
      Task: Fix Login Bug
      Project: Backend API
      Confirm?"

User: "yes"

→ graph resumes → task created in Zoho → confirmation sent
```

If the user says **no**, the operation is cancelled with no side effects.

---

### 4. Human-in-the-Loop (HIL) in Detail

HIL is not a separate node — it lives inside each action tool. When an action tool is called:

1. Tool calls `interrupt()` with a payload describing what is about to happen
2. LangGraph pauses the graph and returns the interrupt payload to the API
3. FastAPI sends it to the frontend as a confirmation prompt
4. User clicks Confirm or Cancel
5. Frontend sends `POST /chat` with `{ confirmed: true }` or `{ confirmed: false }`
6. Backend calls `graph.invoke(Command(resume={"approved": True/False}))`
7. Graph resumes — tool either executes or raises `RuntimeError("Action not approved")`
8. Action agent catches the error and returns a clean cancel message

This applies to all three action tools: `create_task`, `update_task`, `delete_task`.

---

### 5. Memory

Projex maintains two types of memory:

#### Short-term (within session)

The full conversation history is carried in `AgentState.messages`. LangGraph's `MemorySaver` checkpointer uses `session_id` as the thread key — state is automatically restored between turns within the same session.

This is what allows the agent to understand follow-up messages:
```
User: "Show me my projects"
Bot:  "Here are 3 projects: Backend API, Mobile App, Marketing Site"

User: "Show tasks for the second one"   ← agent knows "second one" = Mobile App
```

#### Long-term (across sessions)

After each turn, `save_memory` writes the current project and session messages to PostgreSQL. On next login, `load_context` reads this back into state — the user continues exactly where they left off without re-selecting a project.

---

### 6. Token Refresh

Zoho access tokens expire after 1 hour. Before every Zoho API call, Projex checks `expires_at` in the `user_tokens` table. If the token is expired, it silently fetches a new one using the stored `refresh_token`. The user never sees this happen.

---

## Sample Conversations

### Read operation
```
User: "What projects do I have?"
Bot:  Lists all projects for the authenticated user

User: "Show tasks for the first one"
Bot:  Remembers which project, lists tasks with status and assignees
```

### Write operation with confirmation
```
User: "Create a task called API Integration in Backend API"
Bot:  "About to create:
       Task: API Integration
       Project: Backend API
       Confirm?"

User: "yes"
Bot:  "Task created successfully."
```

### Write operation declined
```
User: "Delete task Fix Login Bug"
Bot:  "About to delete task: Fix Login Bug. This cannot be undone. Confirm?"

User: "no"
Bot:  "Action cancelled."
```

### Utilisation report
```
User: "Who has the most tasks this month?"
Bot:  Calls get_task_utilisation, returns a summary per member
```

---

## What Projex Cannot Do

- It cannot switch between multiple Zoho portals in one session — it uses the first portal on login
- It does not support bulk operations (delete all tasks, etc.)
- Write operations always require confirmation — there is no way to skip HIL
- It does not support Zoho modules outside of Projects and Tasks (no CRM, no Books, etc.)