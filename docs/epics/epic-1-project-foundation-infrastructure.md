# Epic 1: Project Foundation & Infrastructure

**Epic Goal:** Establish the complete technical foundation that enables all subsequent development, including project structure, build systems, database infrastructure, and basic deployment pipeline.

**Value:** Without this foundation, no features can be built. This epic creates the scaffolding for the entire "Goldilocks" architectural template.

---

## Story 1.1: Initialize Project Structure and Build System

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

## Story 1.2: Set Up PostgreSQL Database and SQLAlchemy ORM

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

## Story 1.3: Create Basic Health Check and API Documentation Endpoints

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

## Story 1.4: Configure Session Storage Infrastructure

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

## Story 1.5: Create Basic Frontend Layout and Routing

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

## Story 1.6: Set Up Basic Deployment Configuration

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
