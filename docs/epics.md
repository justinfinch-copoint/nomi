# Nomi - Epic Breakdown

**Author:** Justin
**Date:** 2025-11-12
**Project Level:** 2-3 (Medium Complexity)
**Target Scale:** Learning/Reference Project

---

## Overview

This document provides the complete epic and story breakdown for Nomi, decomposing the requirements from the [PRD](./PRD.md) into implementable stories.

### Epic Summary

Nomi's implementation is organized into **7 sequential epics** that progressively build the "Goldilocks" architectural template:

1. **Project Foundation & Infrastructure** - Establish technical foundation (build system, database, deployment pipeline)
2. **Authentication & Session Management** ⭐ - Implement maximum-security server-side OAuth2 with EntraID (THE crown jewel pattern)
3. **Task Management** - Deliver core CRUD functionality demonstrating REST API, data isolation, and Zustand state management
4. **Inspiration Management** - Validate patterns across multiple entity types with cross-entity operations
5. **Organization & Filtering** - Enhance UX with client-side filtering and sorting patterns
6. **User Profile & Settings** - Display user context from identity provider
7. **Deployment & Documentation** - Production-ready deployment and architectural knowledge capture

**Sequencing Philosophy:** Each epic builds on previous foundations, enabling incremental value delivery while progressively proving all architectural patterns. Epic 2 (Authentication) is the critical learning goal - everything else demonstrates how to build on secure foundations.

---

## Epic 1: Project Foundation & Infrastructure

**Epic Goal:** Establish the complete technical foundation that enables all subsequent development, including project structure, build systems, database infrastructure, and basic deployment pipeline.

**Value:** Without this foundation, no features can be built. This epic creates the scaffolding for the entire "Goldilocks" architectural template.

---

### Story 1.1: Initialize Project Structure and Build System

As a **developer**,
I want the complete project structure with React + Vite frontend and FastAPI backend initialized,
So that I have a working development environment with hot module reload and a clear separation of concerns.

**Acceptance Criteria:**

**Given** a greenfield project
**When** I run the initialization commands
**Then** I have a working frontend at `http://localhost:5173` with Vite HMR

**And** I have a working backend at `http://localhost:8000` with FastAPI auto-reload

**And** the frontend has a Vite proxy configured to forward `/api/*` requests to the backend

**And** the project structure follows best practices:
- `frontend/src/` (components, pages, stores, services, utils)
- `backend/app/` (api, models, schemas, services, core)

**And** I have package management configured (npm/pnpm for frontend, pip/poetry for backend)

**And** basic linting is configured (ESLint + Prettier for frontend, Black + Ruff for backend)

**Prerequisites:** None (first story)

**Technical Notes:**
- Use Vite's React + TypeScript template
- Configure Vite proxy in `vite.config.ts` to avoid CORS during development
- FastAPI with uvicorn for backend
- Python 3.10+
- Create `.gitignore` for both frontend and backend
- Add `.env.example` files for environment variables

---

### Story 1.2: Set Up PostgreSQL Database and SQLAlchemy ORM

As a **developer**,
I want PostgreSQL configured with SQLAlchemy ORM and Alembic migrations,
So that I have a production-grade relational database ready for user-specific data storage.

**Acceptance Criteria:**

**Given** the backend project structure exists
**When** I configure the database connection
**Then** I can connect to PostgreSQL (local or Docker)

**And** SQLAlchemy is configured with a base model class

**And** Alembic is initialized for database migrations

**And** I have a `users` table schema defined with fields: id (UUID), email, name, entraid_user_id, created_at, updated_at

**And** I can run `alembic upgrade head` to apply migrations

**And** Database connection settings are environment-based (`.env` file)

**Prerequisites:** Story 1.1

**Technical Notes:**
- Use SQLAlchemy 2.0+ with async support
- PostgreSQL connection string in environment variables
- Alembic for migrations
- UUID primary keys for users
- Timestamps (created_at, updated_at) on all tables
- Foreign key relationships will be added in later epics

---

### Story 1.3: Create Basic Health Check and API Documentation Endpoints

As a **developer**,
I want basic health check and API documentation endpoints,
So that I can verify the backend is running and explore API contracts via auto-generated docs.

**Acceptance Criteria:**

**Given** the FastAPI backend is running
**When** I navigate to `http://localhost:8000/health`
**Then** I receive a JSON response: `{"status": "healthy"}`

**And** when I navigate to `http://localhost:8000/docs`
**Then** I see the auto-generated Swagger UI with API documentation

**And** when I navigate to `http://localhost:8000/redoc`
**Then** I see the alternative ReDoc documentation interface

**Prerequisites:** Story 1.1

**Technical Notes:**
- FastAPI automatically generates OpenAPI docs
- Health check endpoint returns 200 status
- Document API metadata (title, version, description)

---

### Story 1.4: Configure Session Storage Infrastructure

As a **developer**,
I want session storage configured with Redis for production and in-memory for development,
So that I'm ready to implement server-side session management for authentication.

**Acceptance Criteria:**

**Given** the backend is configured
**When** I'm in development mode
**Then** sessions are stored in-memory (no external dependencies)

**And** when I'm in production mode
**Then** sessions are stored in Redis with configurable connection settings

**And** I have a session manager utility that abstracts storage (Redis or in-memory)

**And** environment variables control which session backend is used

**Prerequisites:** Story 1.2

**Technical Notes:**
- Use `aioredis` or `redis-py` for Redis connection
- In-memory: Python dictionary with TTL management (simple implementation for dev)
- Session manager interface: `create_session(user_id, data)`, `get_session(session_id)`, `delete_session(session_id)`
- Session TTL: 24 hours (configurable)
- Environment variable: `SESSION_BACKEND=redis|memory`

---

### Story 1.5: Create Basic Frontend Layout and Routing

As a **developer**,
I want a basic React app with routing and layout structure,
So that I have a foundation for building authenticated and public pages.

**Acceptance Criteria:**

**Given** the React frontend is initialized
**When** I run the development server
**Then** I see a basic app shell with header/navigation

**And** React Router is configured with routes for:
  - `/` (public landing/home)
  - `/login` (placeholder login page)
  - `/tasks` (protected route - placeholder)
  - `/inspirations` (protected route - placeholder)
  - `/profile` (protected route - placeholder)

**And** navigation links are visible in the header

**And** a placeholder "Protected Route" component wraps authenticated routes

**And** basic CSS/styling framework is configured (Tailwind CSS or CSS modules)

**Prerequisites:** Story 1.1

**Technical Notes:**
- React Router v6+
- Create layout components: Header, Main content area
- Protected route wrapper (will be implemented properly in Epic 2)
- Use Tailwind CSS for utility-first styling (or alternative)
- Responsive design considerations from the start

---

### Story 1.6: Set Up Basic Deployment Configuration

As a **developer**,
I want basic deployment configuration for the single-server pattern,
So that I can deploy the application with FastAPI serving both the React build and API endpoints.

**Acceptance Criteria:**

**Given** the frontend and backend are both working in development
**When** I build the frontend for production
**Then** the compiled static files are output to `frontend/dist`

**And** FastAPI is configured to serve static files from `frontend/dist` at the root path `/`

**And** API endpoints remain accessible at `/api/*`

**And** FastAPI has a fallback route that serves `index.html` for client-side routing (SPA routing support)

**And** I have a deployment script or instructions for building and running in production mode

**Prerequisites:** Stories 1.1, 1.5

**Technical Notes:**
- Use `StaticFiles` middleware in FastAPI to mount the React build
- API routes must be registered before static files to take precedence
- Catchall route returns `index.html` for React Router
- Production build script: `npm run build` in frontend, then start FastAPI
- Environment-based configuration (dev vs production)
- Document deployment steps in README

---

## Epic 2: Authentication & Session Management

**Epic Goal:** Implement maximum-security server-side OAuth2 authentication with EntraID, session-based API protection using HTTP-only signed cookies, and protected routes on both frontend and backend.

**Value:** This is THE crown jewel architectural pattern - demonstrating enterprise-grade authentication with zero token exposure to the browser. Complete immunity to XSS token theft.

---

### Story 2.1: Configure EntraID Application Registration

As a **developer**,
I want an EntraID (Azure AD) application registered and configured for OAuth2 authorization code flow,
So that I can authenticate users with Microsoft identity platform.

**Acceptance Criteria:**

**Given** I have access to Azure Portal
**When** I register a new application in EntraID
**Then** I have a client ID and client secret

**And** the redirect URI is set to `http://localhost:8000/api/auth/callback` (development)

**And** the application is configured for "Web" platform (not SPA)

**And** API permissions include: `openid`, `profile`, `email`

**And** I have documented the configuration steps for future deployments

**And** client ID and client secret are stored in environment variables (never committed to git)

**Prerequisites:** Story 1.1

**Technical Notes:**
- Azure Portal → App Registrations → New Registration
- Platform: Web (server-side OAuth2)
- Redirect URI will change for production deployment
- Client secret stored in `.env` file
- Document in `docs/SETUP.md` or similar
- Add production redirect URI when deploying

---

### Story 2.2: Implement OAuth2 Authorization Initiation (Login Redirect)

As a **user**,
I want to click "Sign in with Microsoft" and be redirected to EntraID login,
So that I can authenticate using my Microsoft account.

**Acceptance Criteria:**

**Given** I'm on the login page (unauthenticated)
**When** I click "Sign in with Microsoft" button
**Then** the frontend redirects to `/api/auth/login` endpoint

**And** the backend constructs an EntraID authorization URL with:
  - `client_id` (from environment)
  - `redirect_uri` (backend callback URL)
  - `scope` (openid, profile, email)
  - `state` (CSRF protection token - randomly generated and stored in session)
  - `response_type=code` (authorization code flow)

**And** the backend redirects my browser to the EntraID authorization URL

**And** I see the Microsoft login page

**Prerequisites:** Stories 1.1, 2.1

**Technical Notes:**
- Frontend: Button triggers `window.location.href = '/api/auth/login'`
- Backend: Use `authlib` or `msal` library to construct authorization URL
- Generate random `state` parameter and store in temporary session/cookie for CSRF validation
- EntraID authorization URL format: `https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?...`
- Use common tenant or specific tenant ID

---

### Story 2.3: Implement OAuth2 Token Exchange (Callback Handler)

As a **user returning from EntraID**,
I want the backend to exchange my authorization code for tokens,
So that my identity is verified and a session is created.

**Acceptance Criteria:**

**Given** I've authenticated with Microsoft
**When** EntraID redirects to `/api/auth/callback?code=...&state=...`
**Then** the backend validates the `state` parameter matches the stored CSRF token

**And** the backend uses MSAL Python to exchange the authorization code for tokens (access token + ID token)

**And** the backend validates the ID token signature using JWKS from Microsoft

**And** the backend extracts user profile from ID token claims:
  - `sub` (user ID)
  - `email`
  - `name`

**And** the ID token is successfully validated

**Prerequisites:** Story 2.2

**Technical Notes:**
- Use `msal.ConfidentialClientApplication` for token exchange
- Validate `state` parameter to prevent CSRF
- Verify ID token signature using Microsoft's JWKS endpoint
- Extract claims: `sub`, `email`, `name`, `preferred_username`
- Handle errors: invalid code, expired code, token validation failure
- Do NOT send tokens to frontend - keep them server-side only

---

### Story 2.4: Create Server-Side Session and Set HTTP-Only Cookie

As a **user with validated tokens**,
I want a server-side session created with an HTTP-only signed cookie,
So that I'm authenticated for subsequent API requests without exposing any tokens to the browser.

**Acceptance Criteria:**

**Given** the ID token is validated successfully
**When** the backend creates a session
**Then** a unique session ID is generated (UUID or secure random string)

**And** the session is stored in the session backend (Redis or in-memory) with:
  - session_id (key)
  - user_id (from ID token `sub` claim)
  - email, name (from ID token)
  - created_at, expires_at (24-hour TTL)

**And** an HTTP-only cookie is set with:
  - Name: `session_id`
  - Value: signed session ID (to prevent tampering)
  - HttpOnly: true (JavaScript cannot access)
  - Secure: true (HTTPS only in production)
  - SameSite: Lax (CSRF protection)
  - Max-Age: 86400 (24 hours)

**And** the backend redirects to the frontend home page (`/`)

**And** no tokens are ever sent to the browser

**Prerequisites:** Stories 1.4, 2.3

**Technical Notes:**
- Use session manager from Story 1.4
- Sign cookie value using secret key (prevents tampering)
- Use `itsdangerous` or FastAPI's built-in signing for cookie signature
- Session ID should be cryptographically random
- Store minimal data in session (user_id, email, name)
- Tokens remain server-side only (can be stored if needed for API calls, but not for MVP)

---

### Story 2.5: Create User Record in Database (First-Time Login)

As a **user logging in for the first time**,
I want a user record created in the database,
So that my tasks and inspirations can be associated with my account.

**Acceptance Criteria:**

**Given** the ID token is validated and session is being created
**When** the user_id (from `sub` claim) does not exist in the database
**Then** a new user record is created in the `users` table with:
  - `id` (UUID primary key)
  - `entraid_user_id` (from `sub` claim - unique index)
  - `email` (from ID token)
  - `name` (from ID token)
  - `created_at`, `updated_at` (timestamps)

**And** when the user_id already exists in the database
**Then** the existing user record is updated with latest email and name (in case they changed in EntraID)

**And** the database user ID is stored in the session for future requests

**Prerequisites:** Stories 1.2, 2.4

**Technical Notes:**
- Upsert logic: Check if `entraid_user_id` exists, create or update accordingly
- Use database user ID (not EntraID user ID) for foreign keys in tasks/inspirations
- Unique constraint on `entraid_user_id`
- Update `updated_at` timestamp on profile updates

---

### Story 2.6: Implement Session Validation Middleware for Protected API Endpoints

As a **backend service**,
I want all protected API endpoints to validate session cookies,
So that only authenticated users can access their data.

**Acceptance Criteria:**

**Given** a request is made to a protected endpoint (e.g., `/api/tasks`, `/api/inspirations`)
**When** the request includes a valid session cookie
**Then** the middleware validates the cookie signature

**And** the middleware retrieves the session from the session store using the session ID

**And** if the session is valid and not expired, the request proceeds with user context attached

**And** the user ID from the session is available to the endpoint handler

**And** if the session cookie is missing, invalid, or expired
**Then** the middleware returns 401 Unauthorized with JSON error: `{"detail": "Not authenticated"}`

**Prerequisites:** Story 2.4

**Technical Notes:**
- FastAPI dependency for session validation: `get_current_user()`
- Verify cookie signature to prevent tampering
- Check session expiry (TTL)
- Attach user object to request state for endpoint access
- Return 401 for missing/invalid/expired sessions
- Apply middleware to all `/api/*` routes except `/api/auth/*` and `/api/health`

---

### Story 2.7: Create /api/auth/me Endpoint to Retrieve User Profile

As a **frontend application**,
I want to call `/api/auth/me` to check authentication status and retrieve user profile,
So that I can display user information and determine if the user is logged in.

**Acceptance Criteria:**

**Given** I have a valid session cookie
**When** I call GET `/api/auth/me`
**Then** I receive a 200 OK response with JSON:
```json
{
  "authenticated": true,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

**And** if I don't have a valid session cookie
**Then** I receive a 401 Unauthorized response

**Prerequisites:** Story 2.6

**Technical Notes:**
- Protected endpoint using session validation middleware
- Returns user profile from session
- Frontend calls this on app initialization to check auth status
- Used by frontend to populate auth state in Zustand store

---

### Story 2.8: Implement Logout Functionality

As a **user**,
I want to log out and have my session destroyed,
So that I'm no longer authenticated and must log in again to access protected resources.

**Acceptance Criteria:**

**Given** I'm authenticated with a valid session
**When** I click the logout button
**Then** the frontend calls POST `/api/auth/logout`

**And** the backend deletes the session from the session store

**And** the backend clears the session cookie (sets empty value with immediate expiry)

**And** the backend returns 200 OK

**And** the frontend clears auth state from Zustand store

**And** the frontend redirects me to the landing page (`/`)

**And** I can no longer access protected API endpoints (401 Unauthorized)

**Prerequisites:** Stories 2.6, 2.7

**Technical Notes:**
- Backend deletes session from Redis/in-memory store
- Clear cookie: Set-Cookie with empty value, Max-Age=0
- Frontend clears Zustand auth store
- Redirect to landing page after logout

---

### Story 2.9: Implement Zustand Auth Store and Frontend Auth State Management

As a **frontend application**,
I want centralized auth state management with Zustand,
So that all components can access authentication status and user profile.

**Acceptance Criteria:**

**Given** the app initializes
**When** the React app loads
**Then** a Zustand auth store is initialized with state:
```typescript
{
  isAuthenticated: boolean,
  user: { id, email, name } | null,
  loading: boolean
}
```

**And** on app initialization, the store calls `/api/auth/me` to check auth status

**And** if the API returns user data, the store sets `isAuthenticated: true` and populates `user`

**And** if the API returns 401, the store sets `isAuthenticated: false` and `user: null`

**And** the store exposes actions: `login()`, `logout()`, `checkAuth()`

**And** components can access auth state using Zustand selectors

**Prerequisites:** Stories 1.5, 2.7

**Technical Notes:**
- Create `src/stores/authStore.ts`
- Use Zustand for state management
- Call `/api/auth/me` on app mount (in App.tsx or root component)
- Actions trigger API calls and update state
- Loading state for async operations

---

### Story 2.10: Implement Protected Route Guards in React Router

As a **frontend application**,
I want protected routes to redirect unauthenticated users to the login page,
So that authenticated-only pages are not accessible without login.

**Acceptance Criteria:**

**Given** I'm unauthenticated
**When** I attempt to navigate to a protected route (`/tasks`, `/inspirations`, `/profile`)
**Then** I'm redirected to `/login`

**And** given I'm authenticated
**When** I navigate to a protected route
**Then** I see the requested page

**And** given I'm on a protected page and my session expires
**When** the API returns 401 Unauthorized
**Then** the frontend clears auth state and redirects me to `/login`

**And** after logging in, I'm redirected to the originally requested route (or home if none)

**Prerequisites:** Stories 1.5, 2.9

**Technical Notes:**
- Create `ProtectedRoute` wrapper component
- Check `isAuthenticated` from Zustand auth store
- Redirect using React Router's `Navigate` component
- Store intended route in location state for post-login redirect
- API interceptor: Catch 401 responses globally, trigger logout + redirect

---

### Story 2.11: Implement Session Expiry Handling

As a **user with an expired session**,
I want to be gracefully logged out and redirected to login,
So that I understand my session has expired and can log in again.

**Acceptance Criteria:**

**Given** my session has expired (24 hours of inactivity)
**When** I make any API request
**Then** the backend returns 401 Unauthorized

**And** the frontend intercepts the 401 response

**And** the frontend displays a toast notification: "Your session has expired. Please log in again."

**And** the frontend clears auth state from Zustand store

**And** the frontend redirects me to `/login`

**And** I can log in again successfully

**Prerequisites:** Stories 2.6, 2.9, 2.10

**Technical Notes:**
- Session TTL enforced in session store (24 hours)
- Global API error interceptor in frontend
- Use toast notification library (react-hot-toast or similar)
- Clear auth state before redirect
- Store intended route for post-login redirect

---

## Epic 3: Task Management

**Epic Goal:** Deliver complete task CRUD functionality with user-specific data isolation, demonstrating REST API design, database relationships, Zustand state management, and optimistic UI updates.

**Value:** First full entity implementation proving the complete stack works end-to-end. High user value. Foundation for understanding all patterns.

---

### Story 3.1: Create Tasks Database Schema and Model

As a **developer**,
I want a tasks table with proper schema and SQLAlchemy model,
So that I can store user-specific tasks with all required properties.

**Acceptance Criteria:**

**Given** the database is initialized
**When** I run Alembic migrations
**Then** a `tasks` table is created with columns:
  - `id` (UUID, primary key)
  - `user_id` (UUID, foreign key to users.id, not null)
  - `title` (VARCHAR(200), not null)
  - `description` (TEXT, nullable)
  - `status` (VARCHAR(20), default 'todo', values: 'todo', 'done')
  - `created_at` (TIMESTAMP, not null)
  - `updated_at` (TIMESTAMP, not null)

**And** a foreign key constraint ensures `user_id` references `users.id`

**And** an index is created on `user_id` for efficient queries

**And** an index is created on `updated_at` for sorting

**And** an SQLAlchemy model class `Task` is defined with proper relationships

**Prerequisites:** Story 1.2, Story 2.5 (users table exists)

**Technical Notes:**
- Alembic migration: `alembic revision --autogenerate -m "Add tasks table"`
- Foreign key with cascade delete (if user deleted, delete tasks - for future)
- SQLAlchemy model in `backend/app/models/task.py`
- Relationship: `user = relationship("User", back_populates="tasks")`
- Use UUID for IDs

---

### Story 3.2: Create Task Pydantic Schemas for API Validation

As a **developer**,
I want Pydantic schemas for task creation, updates, and responses,
So that API requests and responses are validated and type-safe.

**Acceptance Criteria:**

**Given** I'm building the tasks API
**When** I define Pydantic schemas
**Then** I have the following schemas:
  - `TaskCreate`: title (required, max 200 chars), description (optional, max 2000 chars)
  - `TaskUpdate`: title (optional, max 200 chars), description (optional, max 2000 chars), status (optional, 'todo' or 'done')
  - `TaskResponse`: id, user_id, title, description, status, created_at, updated_at

**And** validation errors return 422 Unprocessable Entity with clear error messages

**And** character limits are enforced

**And** status field only accepts 'todo' or 'done'

**Prerequisites:** Story 3.1

**Technical Notes:**
- Pydantic schemas in `backend/app/schemas/task.py`
- Use Field validators for max length
- Enum for status field
- Response schema includes all fields for frontend consumption

---

### Story 3.3: Implement POST /api/tasks (Create Task)

As a **user**,
I want to create a new task,
So that I can track things I need to do.

**Acceptance Criteria:**

**Given** I'm authenticated
**When** I POST to `/api/tasks` with JSON body:
```json
{
  "title": "My new task",
  "description": "Task details"
}
```
**Then** a new task is created in the database with:
  - My user_id (from session)
  - Provided title and description
  - Default status: 'todo'
  - Generated id, created_at, updated_at

**And** the API returns 201 Created with the complete task object

**And** if title is missing or exceeds 200 chars, I receive 422 Unprocessable Entity

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 3.1, 3.2

**Technical Notes:**
- Protected endpoint requiring session validation
- Extract user_id from session
- Use TaskCreate schema for validation
- Return TaskResponse schema
- Handle database errors gracefully

---

### Story 3.4: Implement GET /api/tasks (List All User's Tasks)

As a **user**,
I want to retrieve all my tasks,
So that I can see what I need to do.

**Acceptance Criteria:**

**Given** I'm authenticated and have tasks in the database
**When** I GET `/api/tasks`
**Then** I receive 200 OK with JSON array of all my tasks

**And** tasks are filtered by my user_id (I only see my own tasks)

**And** tasks are sorted by `updated_at` descending (most recently updated first)

**And** each task includes: id, title, description, status, created_at, updated_at

**And** if I have no tasks, I receive an empty array `[]`

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 3.1, 3.2

**Technical Notes:**
- Protected endpoint
- Query: `SELECT * FROM tasks WHERE user_id = ? ORDER BY updated_at DESC`
- Return list of TaskResponse schemas
- SQLAlchemy query with filter and order_by

---

### Story 3.5: Implement GET /api/tasks/{id} (Read Single Task)

As a **user**,
I want to retrieve a specific task by ID,
So that I can view its details.

**Acceptance Criteria:**

**Given** I'm authenticated and a task with the given ID exists
**When** I GET `/api/tasks/{id}`
**Then** I receive 200 OK with the task object

**And** the task belongs to me (user_id matches my session)

**And** if the task ID doesn't exist, I receive 404 Not Found

**And** if the task exists but belongs to another user, I receive 403 Forbidden

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 3.1, 3.2

**Technical Notes:**
- Protected endpoint
- Validate ownership: task.user_id == session.user_id
- Return 403 if user doesn't own the task
- Use TaskResponse schema

---

### Story 3.6: Implement PUT /api/tasks/{id} (Update Task)

As a **user**,
I want to update a task's title, description, or status,
So that I can modify task details or mark it as done.

**Acceptance Criteria:**

**Given** I'm authenticated and own a task
**When** I PUT to `/api/tasks/{id}` with JSON body:
```json
{
  "title": "Updated title",
  "status": "done"
}
```
**Then** the task is updated with the provided fields

**And** the `updated_at` timestamp is set to the current time

**And** the API returns 200 OK with the updated task object

**And** if the task doesn't exist, I receive 404 Not Found

**And** if the task belongs to another user, I receive 403 Forbidden

**And** if validation fails (title too long, invalid status), I receive 422 Unprocessable Entity

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 3.1, 3.2

**Technical Notes:**
- Protected endpoint
- Validate ownership before update
- Use TaskUpdate schema (all fields optional)
- Only update provided fields (partial update)
- Update `updated_at` timestamp
- Return TaskResponse schema

---

### Story 3.7: Implement DELETE /api/tasks/{id} (Delete Task)

As a **user**,
I want to delete a task permanently,
So that I can remove tasks I no longer need.

**Acceptance Criteria:**

**Given** I'm authenticated and own a task
**When** I DELETE `/api/tasks/{id}`
**Then** the task is permanently deleted from the database

**And** the API returns 204 No Content

**And** if the task doesn't exist, I receive 404 Not Found

**And** if the task belongs to another user, I receive 403 Forbidden

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 3.1, 3.2

**Technical Notes:**
- Protected endpoint
- Validate ownership before deletion
- Hard delete (no soft delete for MVP)
- Return 204 No Content on success

---

### Story 3.8: Create Zustand Tasks Store for State Management

As a **frontend application**,
I want a Zustand store to manage tasks state,
So that task data is centralized and components stay in sync.

**Acceptance Criteria:**

**Given** the frontend needs to manage tasks
**When** the tasks store is initialized
**Then** it contains state:
```typescript
{
  tasks: Task[],
  loading: boolean,
  error: string | null
}
```

**And** it exposes actions:
  - `fetchTasks()` - calls GET /api/tasks and updates state
  - `createTask(data)` - calls POST /api/tasks and adds to state
  - `updateTask(id, data)` - calls PUT /api/tasks/{id} and updates state
  - `deleteTask(id)` - calls DELETE /api/tasks/{id} and removes from state

**And** actions handle loading and error states

**And** components can subscribe to tasks using selectors

**Prerequisites:** Story 1.5 (Zustand configured)

**Technical Notes:**
- Create `src/stores/tasksStore.ts`
- Use Zustand for state management
- Actions call API and update state optimistically (add before API confirms)
- Error handling with try/catch
- Loading state for async operations

---

### Story 3.9: Build Task List UI Component

As a **user**,
I want to see all my tasks in a list view,
So that I can quickly scan what I need to do.

**Acceptance Criteria:**

**Given** I'm on the `/tasks` page
**When** the page loads
**Then** tasks are fetched from the API and displayed in a list

**And** each task shows: title, status (todo/done indicator), created date

**And** if I have no tasks, I see an empty state: "No tasks yet - create your first one!"

**And** tasks are sorted by most recently updated first

**And** I see a loading indicator while tasks are being fetched

**And** if an error occurs, I see an error message

**Prerequisites:** Stories 3.4, 3.8

**Technical Notes:**
- React component: `TaskList.tsx`
- Use Zustand tasks store to access state
- Call `fetchTasks()` on component mount
- Map over tasks array to render task cards
- Visual differentiation for done tasks (strikethrough, faded, or checkmark)
- Loading skeleton or spinner

---

### Story 3.10: Build Task Creation Form

As a **user**,
I want to create a new task via a form,
So that I can add items to my task list.

**Acceptance Criteria:**

**Given** I'm on the `/tasks` page
**When** I click "Add Task" button
**Then** a task creation form appears (modal or inline)

**And** the form has fields:
  - Title (required, max 200 chars)
  - Description (optional, textarea, max 2000 chars)

**And** the form validates: Title is required, character limits enforced

**And** when I submit the form
**Then** the task is created via POST /api/tasks

**And** the new task appears in the list immediately (optimistic update)

**And** the form closes/resets

**And** I see a success toast notification: "Task created"

**And** if validation fails, I see inline error messages

**And** the submit button is disabled while submitting

**Prerequisites:** Stories 3.3, 3.8

**Technical Notes:**
- React component: `TaskCreateForm.tsx`
- Modal component or inline form
- Form validation (required fields, max length)
- Call `createTask()` from Zustand store
- Optimistic update: Add to list before API confirms
- Toast notification library (react-hot-toast or similar)
- Disable button during submission

---

### Story 3.11: Build Task Edit Form

As a **user**,
I want to edit a task's title, description, or status,
So that I can modify task details.

**Acceptance Criteria:**

**Given** I'm viewing a task in the list
**When** I click the task or an "Edit" button
**Then** an edit form appears with fields pre-populated:
  - Title (current value)
  - Description (current value)
  - Status (dropdown: todo/done)

**And** I can modify any field

**And** when I submit the form
**Then** the task is updated via PUT /api/tasks/{id}

**And** the task updates in the list immediately (optimistic update)

**And** the form closes

**And** I see a success toast: "Task updated"

**And** if validation fails, I see inline error messages

**And** I can cancel without saving

**Prerequisites:** Stories 3.6, 3.8

**Technical Notes:**
- React component: `TaskEditForm.tsx`
- Reuse or extend TaskCreateForm component
- Pre-populate form with current task values
- Call `updateTask(id, data)` from Zustand store
- Optimistic update
- Cancel button closes form without API call

---

### Story 3.12: Build Quick Status Toggle for Tasks

As a **user**,
I want to quickly mark tasks as done or todo without opening the edit form,
So that I can efficiently update task status.

**Acceptance Criteria:**

**Given** I'm viewing my task list
**When** I click a checkbox next to a task
**Then** the task status toggles between 'todo' and 'done'

**And** the task is updated via PUT /api/tasks/{id}

**And** the UI updates immediately (optimistic)

**And** done tasks are visually differentiated (strikethrough, faded, checkmark icon)

**And** no confirmation is required (quick action)

**Prerequisites:** Stories 3.6, 3.8, 3.9

**Technical Notes:**
- Checkbox or toggle button on each task card
- OnClick handler calls `updateTask(id, { status: newStatus })`
- Optimistic UI update
- Visual styles for done vs todo tasks
- No loading indicator for this quick action

---

### Story 3.13: Build Task Delete Functionality with Confirmation

As a **user**,
I want to delete tasks with a confirmation dialog,
So that I can remove tasks I no longer need without accidental deletion.

**Acceptance Criteria:**

**Given** I'm viewing a task in the list
**When** I click a "Delete" button (trash icon)
**Then** a confirmation dialog appears: "Delete this task? This cannot be undone."

**And** I can confirm or cancel

**And** when I confirm
**Then** the task is deleted via DELETE /api/tasks/{id}

**And** the task is removed from the list immediately (optimistic)

**And** I see a success toast: "Task deleted"

**And** when I cancel, the dialog closes with no action

**Prerequisites:** Stories 3.7, 3.8, 3.9

**Technical Notes:**
- Delete button (trash icon) on each task card
- Confirmation modal/dialog component
- Call `deleteTask(id)` from Zustand store
- Optimistic removal from list
- Toast notification on success

---

## Epic 4: Inspiration Management

**Epic Goal:** Validate architectural patterns across multiple entity types with cross-entity operations, demonstrating that the task management patterns are reusable and that entities can interact (inspiration → task conversion).

**Value:** Second full entity implementation proving pattern reusability. The cross-entity conversion (FR-INSP-005) demonstrates that the architecture supports complex operations between different data models. Lower user value than tasks, but critical for architectural validation.

---

### Story 4.1: Create Inspirations Database Schema and Model

As a **developer**,
I want an inspirations table with proper schema and SQLAlchemy model,
So that I can store user-specific inspirations with all required properties.

**Acceptance Criteria:**

**Given** the database is initialized
**When** I run Alembic migrations
**Then** an `inspirations` table is created with columns:
  - `id` (UUID, primary key)
  - `user_id` (UUID, foreign key to users.id, not null)
  - `title` (VARCHAR(200), not null)
  - `description` (TEXT, nullable)
  - `captured_date` (DATE, not null, default current date)
  - `created_at` (TIMESTAMP, not null)
  - `updated_at` (TIMESTAMP, not null)

**And** a foreign key constraint ensures `user_id` references `users.id`

**And** an index is created on `user_id` for efficient queries

**And** an index is created on `captured_date` for sorting

**And** an SQLAlchemy model class `Inspiration` is defined with proper relationships

**Prerequisites:** Story 1.2 (database infrastructure), Story 2.5 (users table exists)

**Technical Notes:**
- Alembic migration: `alembic revision --autogenerate -m "Add inspirations table"`
- Foreign key with cascade delete (if user deleted, delete inspirations)
- SQLAlchemy model in `backend/app/models/inspiration.py`
- Relationship: `user = relationship("User", back_populates="inspirations")`
- No status field (unlike tasks - inspirations don't have todo/done states)
- captured_date automatically set to current date on creation

---

### Story 4.2: Create Inspiration Pydantic Schemas for API Validation

As a **developer**,
I want Pydantic schemas for inspiration creation, updates, and responses,
So that API requests and responses are validated and type-safe.

**Acceptance Criteria:**

**Given** I'm building the inspirations API
**When** I define Pydantic schemas
**Then** I have the following schemas:
  - `InspirationCreate`: title (required, max 200 chars), description (optional, max 2000 chars)
  - `InspirationUpdate`: title (optional, max 200 chars), description (optional, max 2000 chars)
  - `InspirationResponse`: id, user_id, title, description, captured_date, created_at, updated_at

**And** validation errors return 422 Unprocessable Entity with clear error messages

**And** character limits are enforced

**Prerequisites:** Story 4.1

**Technical Notes:**
- Pydantic schemas in `backend/app/schemas/inspiration.py`
- Use Field validators for max length
- Response schema includes all fields for frontend consumption
- captured_date is read-only (auto-generated on backend)

---

### Story 4.3: Implement POST /api/inspirations (Create Inspiration)

As a **user**,
I want to capture a new inspiration,
So that I can save ideas and thoughts for later.

**Acceptance Criteria:**

**Given** I'm authenticated
**When** I POST to `/api/inspirations` with JSON body:
```json
{
  "title": "My brilliant idea",
  "description": "Details about the idea"
}
```
**Then** a new inspiration is created in the database with:
  - My user_id (from session)
  - Provided title and description
  - captured_date set to current date
  - Generated id, created_at, updated_at

**And** the API returns 201 Created with the complete inspiration object

**And** if title is missing or exceeds 200 chars, I receive 422 Unprocessable Entity

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6 (auth middleware), 4.1, 4.2

**Technical Notes:**
- Protected endpoint requiring session validation
- Extract user_id from session
- Use InspirationCreate schema for validation
- Return InspirationResponse schema
- Auto-set captured_date to current date
- Handle database errors gracefully

---

### Story 4.4: Implement GET /api/inspirations (List All User's Inspirations)

As a **user**,
I want to retrieve all my inspirations,
So that I can review my captured ideas.

**Acceptance Criteria:**

**Given** I'm authenticated and have inspirations in the database
**When** I GET `/api/inspirations`
**Then** I receive 200 OK with JSON array of all my inspirations

**And** inspirations are filtered by my user_id (I only see my own inspirations)

**And** inspirations are sorted by `captured_date` descending (most recently captured first)

**And** each inspiration includes: id, title, description, captured_date, created_at, updated_at

**And** if I have no inspirations, I receive an empty array `[]`

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 4.1, 4.2

**Technical Notes:**
- Protected endpoint
- Query: `SELECT * FROM inspirations WHERE user_id = ? ORDER BY captured_date DESC`
- Return list of InspirationResponse schemas
- SQLAlchemy query with filter and order_by

---

### Story 4.5: Implement GET /api/inspirations/{id} (Read Single Inspiration)

As a **user**,
I want to retrieve a specific inspiration by ID,
So that I can view its details.

**Acceptance Criteria:**

**Given** I'm authenticated and an inspiration with the given ID exists
**When** I GET `/api/inspirations/{id}`
**Then** I receive 200 OK with the inspiration object

**And** the inspiration belongs to me (user_id matches my session)

**And** if the inspiration ID doesn't exist, I receive 404 Not Found

**And** if the inspiration exists but belongs to another user, I receive 403 Forbidden

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 4.1, 4.2

**Technical Notes:**
- Protected endpoint
- Validate ownership: inspiration.user_id == session.user_id
- Return 403 if user doesn't own the inspiration
- Use InspirationResponse schema

---

### Story 4.6: Implement PUT /api/inspirations/{id} (Update Inspiration)

As a **user**,
I want to update an inspiration's title or description,
So that I can refine my captured ideas.

**Acceptance Criteria:**

**Given** I'm authenticated and own an inspiration
**When** I PUT to `/api/inspirations/{id}` with JSON body:
```json
{
  "title": "Updated idea",
  "description": "Refined details"
}
```
**Then** the inspiration is updated with the provided fields

**And** the `updated_at` timestamp is set to the current time

**And** the `captured_date` remains unchanged (not modifiable)

**And** the API returns 200 OK with the updated inspiration object

**And** if the inspiration doesn't exist, I receive 404 Not Found

**And** if the inspiration belongs to another user, I receive 403 Forbidden

**And** if validation fails (title too long), I receive 422 Unprocessable Entity

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 4.1, 4.2

**Technical Notes:**
- Protected endpoint
- Validate ownership before update
- Use InspirationUpdate schema (all fields optional)
- Only update provided fields (partial update)
- Update `updated_at` timestamp
- Do NOT allow updating captured_date
- Return InspirationResponse schema

---

### Story 4.7: Implement DELETE /api/inspirations/{id} (Delete Inspiration)

As a **user**,
I want to delete an inspiration permanently,
So that I can remove ideas I no longer need.

**Acceptance Criteria:**

**Given** I'm authenticated and own an inspiration
**When** I DELETE `/api/inspirations/{id}`
**Then** the inspiration is permanently deleted from the database

**And** the API returns 204 No Content

**And** if the inspiration doesn't exist, I receive 404 Not Found

**And** if the inspiration belongs to another user, I receive 403 Forbidden

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 4.1, 4.2

**Technical Notes:**
- Protected endpoint
- Validate ownership before deletion
- Hard delete (no soft delete for MVP)
- Return 204 No Content on success

---

### Story 4.8: Create Zustand Inspirations Store for State Management

As a **frontend application**,
I want a Zustand store to manage inspirations state,
So that inspiration data is centralized and components stay in sync.

**Acceptance Criteria:**

**Given** the frontend needs to manage inspirations
**When** the inspirations store is initialized
**Then** it contains state:
```typescript
{
  inspirations: Inspiration[],
  loading: boolean,
  error: string | null
}
```

**And** it exposes actions:
  - `fetchInspirations()` - calls GET /api/inspirations and updates state
  - `createInspiration(data)` - calls POST /api/inspirations and adds to state
  - `updateInspiration(id, data)` - calls PUT /api/inspirations/{id} and updates state
  - `deleteInspiration(id)` - calls DELETE /api/inspirations/{id} and removes from state

**And** actions handle loading and error states

**And** components can subscribe to inspirations using selectors

**Prerequisites:** Story 1.5 (Zustand configured)

**Technical Notes:**
- Create `src/stores/inspirationsStore.ts`
- Use Zustand for state management (pattern reuse from tasks store)
- Actions call API and update state optimistically
- Error handling with try/catch
- Loading state for async operations
- Separate store from tasks (different entity)

---

### Story 4.9: Build Inspiration List UI Component

As a **user**,
I want to see all my inspirations in a list view,
So that I can quickly browse my captured ideas.

**Acceptance Criteria:**

**Given** I'm on the `/inspirations` page
**When** the page loads
**Then** inspirations are fetched from the API and displayed in a list

**And** each inspiration shows: title, captured date

**And** if I have no inspirations, I see an empty state: "No inspirations yet - capture your first idea!"

**And** inspirations are sorted by most recently captured first

**And** I see a loading indicator while inspirations are being fetched

**And** if an error occurs, I see an error message

**Prerequisites:** Stories 4.4, 4.8

**Technical Notes:**
- React component: `InspirationList.tsx`
- Use Zustand inspirations store to access state
- Call `fetchInspirations()` on component mount
- Map over inspirations array to render inspiration cards
- Loading skeleton or spinner
- Empty state design

---

### Story 4.10: Build Inspiration Creation Form

As a **user**,
I want to create a new inspiration via a form,
So that I can capture ideas as they come to me.

**Acceptance Criteria:**

**Given** I'm on the `/inspirations` page
**When** I click "Capture Inspiration" button
**Then** an inspiration creation form appears (modal or inline)

**And** the form has fields:
  - Title (required, max 200 chars)
  - Description (optional, textarea, max 2000 chars)

**And** the form validates: Title is required, character limits enforced

**And** when I submit the form
**Then** the inspiration is created via POST /api/inspirations

**And** the new inspiration appears in the list immediately (optimistic update)

**And** the form closes/resets

**And** I see a success toast notification: "Inspiration captured"

**And** if validation fails, I see inline error messages

**And** the submit button is disabled while submitting

**Prerequisites:** Stories 4.3, 4.8

**Technical Notes:**
- React component: `InspirationCreateForm.tsx`
- Modal component or inline form
- Form validation (required fields, max length)
- Call `createInspiration()` from Zustand store
- Optimistic update: Add to list before API confirms
- Toast notification library (reuse from tasks)
- Disable button during submission
- captured_date is auto-generated on backend (not in form)

---

### Story 4.11: Build Inspiration Edit Form

As a **user**,
I want to edit an inspiration's title and description,
So that I can refine my captured ideas.

**Acceptance Criteria:**

**Given** I'm viewing an inspiration in the list
**When** I click the inspiration or an "Edit" button
**Then** an edit form appears with fields pre-populated:
  - Title (current value)
  - Description (current value)

**And** I can modify any field

**And** when I submit the form
**Then** the inspiration is updated via PUT /api/inspirations/{id}

**And** the inspiration updates in the list immediately (optimistic update)

**And** the form closes

**And** I see a success toast: "Inspiration updated"

**And** if validation fails, I see inline error messages

**And** I can cancel without saving

**Prerequisites:** Stories 4.6, 4.8

**Technical Notes:**
- React component: `InspirationEditForm.tsx`
- Reuse or extend InspirationCreateForm component
- Pre-populate form with current inspiration values
- Call `updateInspiration(id, data)` from Zustand store
- Optimistic update
- Cancel button closes form without API call
- captured_date is read-only (not editable)

---

### Story 4.12: Build Inspiration Delete Functionality with Confirmation

As a **user**,
I want to delete inspirations with a confirmation dialog,
So that I can remove ideas I no longer need without accidental deletion.

**Acceptance Criteria:**

**Given** I'm viewing an inspiration in the list
**When** I click a "Delete" button (trash icon)
**Then** a confirmation dialog appears: "Delete this inspiration? This cannot be undone."

**And** I can confirm or cancel

**And** when I confirm
**Then** the inspiration is deleted via DELETE /api/inspirations/{id}

**And** the inspiration is removed from the list immediately (optimistic)

**And** I see a success toast: "Inspiration deleted"

**And** when I cancel, the dialog closes with no action

**Prerequisites:** Stories 4.7, 4.8, 4.9

**Technical Notes:**
- Delete button (trash icon) on each inspiration card
- Confirmation modal/dialog component (reuse from tasks)
- Call `deleteInspiration(id)` from Zustand store
- Optimistic removal from list
- Toast notification on success

---

### Story 4.13: Implement POST /api/inspirations/{id}/convert (Convert Inspiration to Task)

As a **user**,
I want to convert an inspiration into a task,
So that I can act on my ideas by turning them into actionable work items.

**Acceptance Criteria:**

**Given** I'm authenticated and own an inspiration
**When** I POST to `/api/inspirations/{id}/convert`
**Then** the backend creates a new task with:
  - title copied from inspiration
  - description copied from inspiration
  - status set to 'todo'
  - user_id from session

**And** the backend deletes the original inspiration (decision: delete after conversion for MVP simplicity)

**And** the backend returns 201 Created with the created task object

**And** if the inspiration doesn't exist, I receive 404 Not Found

**And** if the inspiration belongs to another user, I receive 403 Forbidden

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 3.1 (tasks table), 4.1, 4.2

**Technical Notes:**
- Protected endpoint
- Validate ownership before conversion
- Create transaction: Create task → Delete inspiration (atomic operation)
- Copy title and description from inspiration to task
- Set default task status to 'todo'
- Return task object (TaskResponse schema)
- Rollback transaction if either operation fails
- MVP decision: Delete inspiration after conversion (simpler than marking as converted)

---

### Story 4.14: Build "Convert to Task" UI Feature

As a **user**,
I want a "Convert to Task" button on each inspiration,
So that I can easily turn ideas into actionable tasks.

**Acceptance Criteria:**

**Given** I'm viewing my inspirations list
**When** I see a "Convert to Task" button on each inspiration
**Then** clicking the button calls POST /api/inspirations/{id}/convert

**And** the inspiration is removed from the inspirations store

**And** the new task is added to the tasks store

**And** I see a success toast: "Inspiration converted to task"

**And** the inspiration disappears from the inspirations list

**And** optional: I'm offered a link to view the new task or navigate to tasks page

**Prerequisites:** Stories 3.8 (tasks store), 4.8 (inspirations store), 4.9, 4.13

**Technical Notes:**
- "Convert to Task" button on each inspiration card
- Call conversion endpoint
- Update both stores: Remove from inspirations, add to tasks
- Toast notification with optional link to tasks page
- Consider confirmation dialog: "Convert this inspiration to a task?"
- Handle errors gracefully (show error toast if conversion fails)
- Optimistic UI update

---

## Epic 5: Organization & Filtering

**Epic Goal:** Enhance UX with client-side filtering and sorting patterns, demonstrating how to manage UI state without additional API calls and how to provide responsive user experience through frontend-only operations.

**Value:** Improves usability significantly by helping users focus on what matters. Demonstrates client-side state management patterns (Zustand selectors, computed state) without backend complexity.

---

### Story 5.1: Implement Client-Side Task Status Filter

As a **user**,
I want to filter my tasks to show only active or completed items,
So that I can focus on what I need to do or review what I've accomplished.

**Acceptance Criteria:**

**Given** I'm on the `/tasks` page with tasks loaded
**When** I see filter options: "All", "Active", "Completed"
**Then** clicking "All" shows all tasks (both todo and done)

**And** clicking "Active" shows only tasks with status='todo'

**And** clicking "Completed" shows only tasks with status='done'

**And** the filter is applied client-side (no API call)

**And** the active filter is visually highlighted

**And** task count is displayed for each filter option (e.g., "Active (5)")

**And** the filter state persists while I navigate away and return to tasks page

**Prerequisites:** Stories 3.4, 3.8, 3.9 (tasks loaded in store)

**Technical Notes:**
- Add `statusFilter` to tasks Zustand store state: 'all' | 'active' | 'completed'
- Create selector that filters tasks based on statusFilter
- Filter buttons component above task list
- Computed counts: `tasks.filter(t => t.status === 'todo').length`
- No API calls - pure frontend filtering
- Default filter: 'all'

---

### Story 5.2: Implement Client-Side Sort for Tasks

As a **user**,
I want to sort my tasks by date,
So that I can see newest or oldest tasks first.

**Acceptance Criteria:**

**Given** I'm on the `/tasks` page with tasks loaded
**When** I see sort options: "Newest first", "Oldest first"
**Then** clicking "Newest first" sorts tasks by `updated_at` descending

**And** clicking "Oldest first" sorts tasks by `updated_at` ascending

**And** the sort is applied client-side (no API call)

**And** the active sort option is visually indicated

**And** the sort preference persists while I navigate away and return

**And** sort works in combination with status filter

**Prerequisites:** Stories 3.4, 3.8, 3.9, 5.1

**Technical Notes:**
- Add `sortOrder` to tasks Zustand store state: 'newest' | 'oldest'
- Create selector that sorts filtered tasks based on sortOrder
- Sort dropdown or toggle buttons
- Sort by `updated_at` field (could also support `created_at`)
- Chain filters: filter by status first, then sort
- Default sort: 'newest'

---

### Story 5.3: Implement Client-Side Sort for Inspirations

As a **user**,
I want to sort my inspirations by date,
So that I can see newest or oldest inspirations first.

**Acceptance Criteria:**

**Given** I'm on the `/inspirations` page with inspirations loaded
**When** I see sort options: "Newest first", "Oldest first"
**Then** clicking "Newest first" sorts inspirations by `captured_date` descending

**And** clicking "Oldest first" sorts inspirations by `captured_date` ascending

**And** the sort is applied client-side (no API call)

**And** the active sort option is visually indicated

**And** the sort preference persists while I navigate away and return

**Prerequisites:** Stories 4.4, 4.8, 4.9

**Technical Notes:**
- Add `sortOrder` to inspirations Zustand store state: 'newest' | 'oldest'
- Create selector that sorts inspirations based on sortOrder
- Sort dropdown or toggle buttons (reuse component from tasks if possible)
- Sort by `captured_date` field
- Default sort: 'newest'

---

### Story 5.4: Add Task and Inspiration Counts to Navigation

As a **user**,
I want to see how many tasks and inspirations I have in the navigation,
So that I have quick visibility into my content at a glance.

**Acceptance Criteria:**

**Given** I'm authenticated and viewing the app
**When** I look at the navigation menu
**Then** I see "Tasks (5)" showing my total task count

**And** I see "Inspirations (3)" showing my total inspiration count

**And** counts update in real-time when I create, delete, or convert items

**And** counts are computed from Zustand stores (no additional API calls)

**Prerequisites:** Stories 3.8, 4.8

**Technical Notes:**
- Read counts from Zustand stores: `tasks.length`, `inspirations.length`
- Use Zustand selectors to subscribe to count changes
- Display in navigation component
- Counts update automatically via store reactivity
- Consider showing active task count vs total: "Tasks (3/10 active)"

---

## Epic 6: User Profile & Settings

**Epic Goal:** Display user context from identity provider, demonstrating how to present read-only data sourced from external authentication systems and provide account management features.

**Value:** Gives users visibility into their account info and provides essential logout functionality. Demonstrates working with identity provider data (read-only profile from EntraID).

---

### Story 6.1: Create Profile Page UI

As a **user**,
I want to view my profile information,
So that I can see my account details and verify my identity.

**Acceptance Criteria:**

**Given** I'm authenticated
**When** I navigate to `/profile`
**Then** I see a profile page displaying:
  - My name (from EntraID)
  - My email address (from EntraID)
  - Account type indicator: "Microsoft Account"

**And** all fields are read-only (no edit functionality)

**And** a note is displayed: "Profile information is managed by your Microsoft account"

**And** a "Logout" button is prominently displayed

**And** the page has a clean, professional layout

**Prerequisites:** Stories 2.7 (auth/me endpoint), 2.9 (auth store)

**Technical Notes:**
- React component: `Profile.tsx`
- Read user data from Zustand auth store
- Display fields as read-only text (not form inputs)
- Professional styling with clear information hierarchy
- Logout button calls logout action from auth store
- Route: `/profile` (protected route)

---

### Story 6.2: Add Profile Link to Navigation

As a **user**,
I want quick access to my profile from the navigation,
So that I can easily view my account details or log out.

**Acceptance Criteria:**

**Given** I'm authenticated
**When** I look at the navigation header
**Then** I see a profile link or user menu

**And** clicking it navigates to `/profile` or opens a dropdown with:
  - "Profile" link → navigates to `/profile`
  - "Logout" button → logs me out

**And** my name or email is displayed in the user menu trigger

**And** the user menu is visually distinct from main navigation

**Prerequisites:** Stories 2.9, 6.1

**Technical Notes:**
- User menu component in header
- Display user name from auth store
- Dropdown menu or direct link to profile
- Include logout action in dropdown for quick access
- Consider user avatar/initials icon
- Responsive design (mobile: hamburger menu or bottom nav)

---

### Story 6.3: Add Activity Summary to Profile Page

As a **user**,
I want to see summary statistics on my profile page,
So that I can quickly understand my usage of the application.

**Acceptance Criteria:**

**Given** I'm on the `/profile` page
**When** the page loads
**Then** I see summary cards displaying:
  - Total tasks count
  - Active tasks count (status='todo')
  - Completed tasks count (status='done')
  - Total inspirations count

**And** counts are computed from Zustand stores (no additional API calls)

**And** counts update in real-time if I create/delete items in another tab

**Prerequisites:** Stories 3.8, 4.8, 6.1

**Technical Notes:**
- Read from tasks and inspirations Zustand stores
- Computed values: filter tasks by status for counts
- Display as summary cards or statistics grid
- Use Zustand selectors for reactivity
- Simple, clear visualization (numbers + labels)
- Optional: Add date joined (user.created_at from database)

---

## Epic 7: Deployment & Documentation

**Epic Goal:** Production-ready deployment and comprehensive architectural knowledge capture, ensuring the template is deployable and well-documented for future reference and reuse.

**Value:** Makes the project truly useful as a reference template. Documentation captures architectural decisions and deployment patterns that are critical learning outcomes. Enables others to understand, deploy, and extend the project.

---

### Story 7.1: Create Deployment Documentation

As a **developer**,
I want comprehensive deployment documentation,
So that I can deploy Nomi to production and understand the deployment architecture.

**Acceptance Criteria:**

**Given** the application is ready for deployment
**When** I read the deployment documentation
**Then** I have clear instructions for:
  - Environment variables configuration (EntraID credentials, database connection, session backend)
  - PostgreSQL database setup (local and production)
  - Redis setup for session storage (production)
  - Building the frontend for production (`npm run build`)
  - Running the backend in production mode (uvicorn with proper settings)
  - Single-server deployment pattern (FastAPI serving both API and static files)

**And** I have example configurations for common deployment targets:
  - Local production simulation
  - Cloud VM (Azure, AWS, GCP)
  - Container deployment (Docker/Docker Compose)

**And** security considerations are documented:
  - HTTPS requirement (Secure cookies)
  - Environment variable management (never commit secrets)
  - CORS configuration
  - Session security settings

**Prerequisites:** Story 1.6 (deployment configuration)

**Technical Notes:**
- Create `docs/DEPLOYMENT.md`
- Include `.env.example` with all required variables
- Document EntraID redirect URI setup for production
- Step-by-step deployment checklist
- Troubleshooting common issues
- Security best practices
- Optional: Docker Compose file for easy local production testing

---

### Story 7.2: Create Architecture Decision Records (ADRs)

As a **developer learning from this template**,
I want to understand WHY architectural decisions were made,
So that I can apply the same reasoning to my own projects.

**Acceptance Criteria:**

**Given** the project is complete
**When** I read the architecture documentation
**Then** I have ADRs documenting key decisions:
  1. Server-side OAuth2 with HTTP-only cookies (vs SPA OAuth with localStorage)
  2. Single-server deployment pattern (vs separate frontend/backend servers)
  3. PostgreSQL with SQLAlchemy (vs other databases/ORMs)
  4. Zustand for state management (vs Redux, Context API, etc.)
  5. Redis for session storage (vs database sessions)
  6. Separate entity stores (vs single unified store)

**And** each ADR follows standard format:
  - Context: What problem are we solving?
  - Decision: What did we choose?
  - Consequences: What are the tradeoffs?
  - Alternatives Considered: What else did we evaluate?

**And** ADRs explain the "Goldilocks" principle for each decision

**Prerequisites:** Project completion (Epic 1-6 stories)

**Technical Notes:**
- Create `docs/architecture/` directory
- ADR template: `docs/architecture/ADR-template.md`
- Individual ADRs: `ADR-001-oauth-pattern.md`, `ADR-002-deployment-pattern.md`, etc.
- Focus on learning value: WHY this choice for a reference template
- Link to relevant code examples
- Discuss when to deviate from these patterns

---

### Story 7.3: Create Comprehensive README

As a **developer discovering this project**,
I want a clear README that explains what Nomi is and how to use it,
So that I can quickly understand the project's purpose and get started.

**Acceptance Criteria:**

**Given** someone discovers the Nomi repository
**When** they read the README
**Then** they understand:
  - **What:** Nomi is a "Goldilocks" architectural template for learning
  - **Why:** Demonstrates enterprise patterns at reference-project scale
  - **Key Patterns:** OAuth2, session auth, REST APIs, React + FastAPI, single-server deployment
  - **Who it's for:** Developers learning full-stack patterns, teams building similar apps

**And** they have quick-start instructions:
  1. Prerequisites (Node.js, Python, PostgreSQL)
  2. Clone and install dependencies
  3. Configure environment variables
  4. Run database migrations
  5. Start development servers
  6. Access the app

**And** they have links to detailed documentation:
  - Architecture overview
  - Deployment guide
  - ADRs
  - API documentation

**And** the README includes badges (optional):
  - Build status
  - License
  - Tech stack icons

**Prerequisites:** Stories 7.1, 7.2

**Technical Notes:**
- Create `README.md` at project root
- Clear structure: Purpose → Features → Quick Start → Documentation → License
- Include architecture diagram (optional but valuable)
- Link to live demo (if deployed)
- Contributing guidelines (if accepting contributions)
- Emphasize learning goals and reference template purpose
- Keep it concise - link to detailed docs rather than embedding everything

---

### Story 7.4: Add API Documentation with Examples

As a **developer**,
I want comprehensive API documentation with examples,
So that I understand how to interact with all endpoints.

**Acceptance Criteria:**

**Given** the API is complete
**When** I access the API documentation
**Then** I can view documentation via:
  - FastAPI auto-generated Swagger UI (`/docs`)
  - FastAPI auto-generated ReDoc (`/redoc`)
  - Optional: Separate API documentation file

**And** for each endpoint, I see:
  - HTTP method and path
  - Description of purpose
  - Authentication requirements
  - Request body schema (if applicable)
  - Response schemas (success and error)
  - Example requests with curl or JavaScript fetch

**And** common response codes are documented:
  - 200 OK, 201 Created, 204 No Content
  - 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Unprocessable Entity

**Prerequisites:** Epic 2 (auth endpoints), Epic 3 (task endpoints), Epic 4 (inspiration endpoints)

**Technical Notes:**
- FastAPI auto-generates OpenAPI docs (already available at `/docs` and `/redoc`)
- Enhance with detailed descriptions in endpoint docstrings
- Pydantic schemas automatically generate request/response examples
- Optional: Create `docs/API.md` with curl examples and usage patterns
- Document authentication flow with sequence diagram
- Include example responses for common error scenarios

---

### Story 7.5: Add Developer Setup Guide

As a **new developer joining the project**,
I want a detailed setup guide,
So that I can get my development environment running quickly.

**Acceptance Criteria:**

**Given** I'm setting up the project for the first time
**When** I follow the developer setup guide
**Then** I have step-by-step instructions for:
  - Installing prerequisites (Node.js, Python, PostgreSQL, optional Redis)
  - Cloning the repository
  - Installing frontend dependencies (`npm install`)
  - Installing backend dependencies (`pip install` or `poetry install`)
  - Setting up PostgreSQL database
  - Configuring environment variables (`.env` files)
  - Registering EntraID application (with screenshots)
  - Running database migrations
  - Starting development servers
  - Verifying the setup works

**And** I have troubleshooting tips for common setup issues

**And** I understand the project structure and where to find things

**Prerequisites:** Project completion

**Technical Notes:**
- Create `docs/SETUP.md` or include in README
- Detailed EntraID setup with screenshots/links
- Environment variable explanation (what each var does)
- Database setup for different OSes (macOS, Linux, Windows)
- Common errors and solutions (port conflicts, dependency issues, database connection failures)
- Link to additional resources (EntraID docs, PostgreSQL docs, etc.)
- Project structure overview: frontend/, backend/, docs/

---

### Story 7.6: Create Testing Documentation and Examples

As a **developer maintaining this project**,
I want testing documentation and example tests,
So that I understand the testing strategy and can add tests confidently.

**Acceptance Criteria:**

**Given** the project is complete
**When** I read the testing documentation
**Then** I understand:
  - Testing philosophy for a reference template (prioritize learning value)
  - Testing stack: pytest (backend), Vitest or Jest (frontend)
  - What to test: Critical paths, authentication, data isolation
  - What not to test: Over-testing reduces template clarity

**And** I have example tests for:
  - Backend: API endpoint test (task CRUD)
  - Backend: Authentication middleware test
  - Backend: Database model test
  - Frontend: Component test (task list)
  - Frontend: Store test (Zustand)
  - Integration test: Auth flow (optional)

**And** I can run tests with simple commands:
  - Backend: `pytest` or `pytest -v`
  - Frontend: `npm test`

**And** tests are documented with comments explaining patterns

**Prerequisites:** Project completion (optional: implement example tests first)

**Technical Notes:**
- Create `docs/TESTING.md`
- Example tests in `backend/tests/` and `frontend/src/__tests__/`
- Focus on demonstrating testing patterns, not 100% coverage
- pytest fixtures for database, authenticated user
- Frontend: React Testing Library for components, Vitest for stores
- Document test database setup (separate test DB)
- CI/CD considerations (optional: GitHub Actions workflow)
- Balance: Enough tests to show patterns, not so many it obscures learning

---

---

_For implementation: Use the `create-story` workflow to generate individual story implementation plans from this epic breakdown._
