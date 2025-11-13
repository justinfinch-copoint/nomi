# Epic Technical Specification: Project Foundation & Infrastructure

Date: 2025-11-13
Author: Justin
Epic ID: 1
Status: Draft

---

## Overview

Epic 1 establishes the complete technical foundation for Nomi - a learning-focused architectural reference project demonstrating production-grade patterns (server-side OAuth2, BFF architecture, vertical slice organization, REPR pattern) at manageable scale. This epic creates the scaffolding for a React + FastAPI application with proper separation of concerns, hot-reload development environment, PostgreSQL database infrastructure, session storage, and single-server deployment configuration. Without this foundation, no subsequent features can be built. This epic directly supports the PRD's primary goal: creating a "Goldilocks" architectural template that's complex enough to prove real-world patterns but simple enough to understand and reuse in future projects.

## Objectives and Scope

**In Scope:**
- ✅ React 19 + TypeScript 5.9 + Vite 7.1 frontend with HMR and Tailwind CSS 4.0
- ✅ FastAPI 0.121 backend with Uvicorn auto-reload
- ✅ Project structure following vertical slice architecture + REPR pattern (features/, core/)
- ✅ PostgreSQL 16+ database with SQLAlchemy 2.0 async ORM and Alembic migrations
- ✅ Users table schema (id, email, name, entraid_user_id, created_at, updated_at)
- ✅ Session storage infrastructure (Redis for production, in-memory for development)
- ✅ Basic React Router setup with placeholder routes (/, /login, /tasks, /inspirations, /profile)
- ✅ Health check endpoint (/health) and auto-generated API documentation (/docs, /redoc)
- ✅ Single-server deployment configuration (FastAPI serves React build + API endpoints)
- ✅ Development tooling (ESLint, Prettier, Black, Ruff)
- ✅ Environment configuration (.env.example files)

**Out of Scope (Deferred to Later Epics):**
- ❌ EntraID OAuth2 authentication implementation (Epic 2)
- ❌ Session validation middleware and protected route guards (Epic 2)
- ❌ Task and Inspiration database schemas and API endpoints (Epics 3-4)
- ❌ Actual user data or real authentication flows (Epic 2)
- ❌ UI styling beyond basic layout structure (incremental across epics)
- ❌ Production deployment to hosting provider (Epic 7)

## System Architecture Alignment

This epic implements the foundational architectural decisions documented in the Architecture document:

**Vertical Slice Architecture (ADR-005):** Backend organized by features (`app/features/auth/`, `app/features/tasks/`) with shared infrastructure in `app/core/`. Each feature slice will be self-contained with its own models, services, and endpoint files.

**REPR Pattern (ADR-006):** Each API endpoint will be a separate file containing Request/Response Pydantic schemas and endpoint handler (e.g., `create_task.py`, `list_tasks.py`). This epic creates the structure; actual endpoint files will be added in subsequent epics.

**Single-Server Deployment (ADR-002):** FastAPI serves both React static files and API endpoints from the same origin, eliminating CORS complexity. Vite proxy in development mirrors this architecture.

**Technology Stack Alignment:**
- Frontend: React 19.2.0, Vite 7.1.9, TypeScript 5.9.x, Tailwind CSS 4.0, React Router 7.9.x, Zustand 5.0.8
- Backend: FastAPI 0.121.1, SQLAlchemy 2.0.44 (Async), PostgreSQL 16+, MSAL Python 1.34.0
- Session Storage: Redis 7.x (production) / In-memory dict (development)

**Constraints Honored:**
- Maximum security pattern: Session-based authentication with HTTP-only cookies (foundation for Epic 2)
- PostgreSQL with UUID primary keys and async SQLAlchemy (ADR-004)
- Zustand for frontend state management (ADR-003)
- Naming conventions: snake_case (backend), camelCase (frontend), SCREAMING_SNAKE_CASE (env vars)

## Detailed Design

### Services and Modules

| Module/Service | Responsibility | Inputs | Outputs | Owner |
|---------------|----------------|---------|---------|-------|
| **Frontend - Vite Dev Server** | HMR, proxy /api/* to backend, serve React app | Source files, vite.config.ts | http://localhost:5173 | Story 1.1, 1.5 |
| **Frontend - React App** | SPA shell with routing, layout components | Routes, components | Rendered UI | Story 1.5 |
| **Backend - FastAPI App** | API server, static file serving, auto-reload | main.py, feature routers | http://localhost:8000 | Story 1.1 |
| **Backend - core/database.py** | Database connection, session factory | DATABASE_URL env var | AsyncSession instances | Story 1.2 |
| **Backend - core/session_store.py** | Session CRUD operations | SESSION_BACKEND env var | Session manager interface | Story 1.4 |
| **Backend - core/config.py** | Centralized settings | Environment variables | Settings instance | Story 1.1 |
| **Backend - Health Check Endpoint** | System health status | None | {"status": "healthy"} | Story 1.3 |
| **Backend - API Docs** | Auto-generated OpenAPI docs | FastAPI route definitions | Swagger UI (/docs), ReDoc (/redoc) | Story 1.3 |
| **Database - PostgreSQL** | Persistent data storage | SQL queries via SQLAlchemy | Query results | Story 1.2 |
| **Database - Alembic** | Schema migrations | Migration scripts | Database schema changes | Story 1.2 |
| **Session Store - Redis** | Production session storage | Session data, TTL | Session retrieval | Story 1.4 |
| **Session Store - In-Memory** | Development session storage | Session data, TTL | Session retrieval | Story 1.4 |

### Data Models and Contracts

**Users Table (Story 1.2)**

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    entraid_user_id VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_entraid_user_id ON users(entraid_user_id);
CREATE INDEX idx_users_email ON users(email);
```

**SQLAlchemy Model (app/features/users/model.py)**

```python
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    entraid_user_id = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**Session Data Model (In-Memory/Redis)**

```python
# Session structure (JSON/dict)
{
    "session_id": "uuid-v4",
    "user_id": "uuid",
    "email": "user@example.com",
    "name": "User Name",
    "created_at": "2025-11-13T10:00:00Z",
    "expires_at": "2025-11-14T10:00:00Z"  # 24 hour TTL
}
```

**Session Manager Interface (app/core/session_store.py)**

```python
class SessionManager:
    async def create_session(self, user_id: str, data: dict) -> str:
        """Create new session, return session_id"""
        pass

    async def get_session(self, session_id: str) -> dict | None:
        """Retrieve session data or None if expired/not found"""
        pass

    async def delete_session(self, session_id: str) -> bool:
        """Delete session, return success status"""
        pass
```

### APIs and Interfaces

**Health Check Endpoint (Story 1.3)**

```
GET /health
Response: 200 OK
Content-Type: application/json

{
  "status": "healthy"
}
```

**API Documentation Endpoints (Story 1.3)**

```
GET /docs
Response: 200 OK
Content-Type: text/html
Returns: Interactive Swagger UI for API exploration

GET /redoc
Response: 200 OK
Content-Type: text/html
Returns: Alternative ReDoc documentation interface

GET /openapi.json
Response: 200 OK
Content-Type: application/json
Returns: OpenAPI 3.0 specification (auto-generated by FastAPI)
```

**Frontend Routing (Story 1.5)**

```typescript
// React Router Routes (client-side)
/ (Home)                  → Public landing page
/login                    → Placeholder login page
/tasks                    → Protected route (placeholder)
/inspirations             → Protected route (placeholder)
/profile                  → Protected route (placeholder)
```

**Development Proxy (Story 1.1)**

```typescript
// vite.config.ts proxy configuration
'/api/*' → 'http://localhost:8000/api/*'
// Forwards all /api requests to backend during development
```

**Production Static File Serving (Story 1.6)**

```python
# FastAPI configuration
app.mount("/", StaticFiles(directory="../nomi-frontend/dist", html=True), name="static")

# Routes priority:
1. /api/* → API endpoints (registered first, take precedence)
2. /static/assets/* → React build assets
3. /* → index.html (SPA fallback for client-side routing)
```

### Workflows and Sequencing

**Development Environment Startup Flow**

```
1. Developer → Terminal: Start PostgreSQL (docker or local service)
2. Developer → Terminal: cd nomi-backend && alembic upgrade head
3. Alembic → PostgreSQL: Apply migration (create users table)
4. Developer → Terminal: uvicorn app.main:app --reload
5. FastAPI → PostgreSQL: Test database connection
6. FastAPI → Console: "Server started at http://localhost:8000"
7. Developer → Terminal: cd nomi-frontend && npm run dev
8. Vite → Console: "Server started at http://localhost:5173"
9. Vite → Vite Config: Configure proxy (/api/* → localhost:8000)
10. Developer → Browser: Navigate to http://localhost:5173
11. Browser → Vite: Request / (root)
12. Vite → Browser: Serve React app with HMR
13. React App → Browser: Render Home page
```

**Database Migration Flow (Story 1.2)**

```
1. Developer → Terminal: alembic revision --autogenerate -m "Create users table"
2. Alembic → app/features/users/model.py: Read SQLAlchemy models
3. Alembic → PostgreSQL: Read current schema
4. Alembic → alembic/versions/xxx.py: Generate migration script (diff)
5. Developer → Terminal: alembic upgrade head
6. Alembic → PostgreSQL: Execute SQL from migration script
7. PostgreSQL → Alembic: Confirm schema updated
8. Alembic → alembic_version table: Record migration version
```

**API Request Flow (Development)**

```
1. Browser → Vite (localhost:5173): Fetch /api/health
2. Vite Proxy → FastAPI (localhost:8000): Forward /api/health
3. FastAPI → Health Endpoint: Route to handler
4. Health Endpoint → FastAPI: Return {"status": "healthy"}
5. FastAPI → Vite Proxy: 200 OK + JSON
6. Vite Proxy → Browser: Forward response
```

**Production Build and Deployment Flow (Story 1.6)**

```
1. Developer → Terminal: cd nomi-frontend && npm run build
2. Vite → nomi-frontend/dist/: Compile React app (static files)
3. Developer → Terminal: cd nomi-backend && uvicorn app.main:app
4. FastAPI → main.py: Load app configuration
5. FastAPI → StaticFiles: Mount nomi-frontend/dist/ at root
6. FastAPI → Uvicorn: Start server on port 8000
7. User → Browser: Navigate to http://server:8000/
8. Browser → FastAPI: GET /
9. FastAPI → StaticFiles: Serve index.html
10. Browser → FastAPI: GET /static/assets/index-abc123.js
11. FastAPI → StaticFiles: Serve JS bundle
12. Browser: Render React app
13. React App → Browser: GET /api/health
14. Browser → FastAPI: /api/health
15. FastAPI → Health Endpoint: {"status": "healthy"}
```

**Session Storage Initialization (Story 1.4)**

```
1. FastAPI → core/config.py: Read SESSION_BACKEND env var
2. Config → main.py: SESSION_BACKEND = "redis" or "memory"
3. IF "redis":
   4a. FastAPI → core/session_store.py: Initialize RedisSessionManager
   5a. RedisSessionManager → Redis: Test connection (PING)
   6a. Redis → RedisSessionManager: PONG (connection confirmed)
4. ELSE "memory":
   4b. FastAPI → core/session_store.py: Initialize InMemorySessionManager
   5b. InMemorySessionManager: Create empty dict + cleanup task
5. FastAPI → Dependency Injection: Register session_manager
```

## Non-Functional Requirements

### Performance

**Source:** PRD NFR-PERF-001, NFR-PERF-002, NFR-PERF-003

**Development Environment:**
- Vite HMR: < 100ms update latency after file save
- FastAPI auto-reload: < 2s server restart after code change
- Health check endpoint: < 50ms response time

**Database Connection:**
- PostgreSQL connection pool: Min 5, Max 20 connections
- Query timeout: 30 seconds
- Connection acquisition: < 100ms under normal load

**Session Storage:**
- Redis operations: < 10ms for get/set/delete
- In-memory operations: < 1ms for get/set/delete
- Session TTL: 24 hours (configurable)

**Frontend Build (Production):**
- Initial bundle size: Target < 500KB (gzipped)
- Build time: < 60 seconds for production build
- Static file serving: < 100ms for cached resources

**Note:** This epic establishes infrastructure only. Full performance requirements (API response times, frontend rendering) apply to feature epics (2-7).

### Security

**Source:** PRD NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005

**Environment Variables (Story 1.1):**
- Sensitive values (DATABASE_URL, session secrets, EntraID credentials) MUST be in .env files
- .env files MUST be in .gitignore (never committed)
- .env.example provided with placeholder values for documentation

**Database Security (Story 1.2):**
- PostgreSQL connection: SSL/TLS enabled in production
- Database credentials: Environment variables only (not hardcoded)
- Connection string format: `postgresql+asyncpg://user:pass@host:port/db?ssl=require`

**Session Storage Security (Story 1.4):**
- Session IDs: UUID v4 (cryptographically random)
- Redis connection: TLS enabled in production, authentication required
- In-memory: Development only, data wiped on server restart

**Development vs Production (Story 1.1, 1.6):**
- Development: HTTP allowed (localhost only)
- Production: HTTPS required (enforced at deployment, not in code)
- CORS: Not applicable (single-server deployment, same origin)

**Input Validation (Story 1.3):**
- Pydantic models validate all API request data (automatic with FastAPI)
- SQL injection prevention: SQLAlchemy ORM (parameterized queries)

**Dependency Security (Story 1.1):**
- Lock files: package-lock.json (frontend), requirements.txt (backend)
- Regular updates via dependabot or manual review
- Vulnerability scanning: `npm audit`, `pip-audit` (recommended in CI/CD)

**Note:** Full authentication and authorization security (OAuth2, session cookies, protected endpoints) implemented in Epic 2.

### Reliability/Availability

**Source:** PRD NFR-REL-001, NFR-REL-002

**Database Reliability (Story 1.2):**
- Connection pooling: Automatic reconnection on connection loss
- Migration rollback: Alembic supports `downgrade` for failed migrations
- Data integrity: PostgreSQL ACID guarantees, foreign key constraints (future epics)
- Backup strategy: Not implemented in this epic (deployment concern)

**Session Storage Reliability (Story 1.4):**
- Redis: Persistence enabled (RDB snapshots + AOF log)
- In-memory: Data loss on restart (acceptable for development)
- Session expiry: Automatic cleanup via TTL (24 hours)
- Graceful degradation: If session store unavailable, return 503 Service Unavailable (Epic 2)

**Error Handling (Story 1.1, 1.3):**
- FastAPI automatic validation errors: 422 Unprocessable Entity with detailed messages
- Uncaught exceptions: FastAPI exception handlers return 500 Internal Server Error
- Health check: Returns 503 if database connection fails (future enhancement)

**Development Environment Resilience:**
- Vite: Auto-reconnects on file watcher errors
- FastAPI: Auto-reload recovers from syntax errors with clear error messages
- PostgreSQL: Docker restart policy or system service auto-restart

**Degradation Behavior:**
- Database unavailable: API returns 503, frontend shows error message (Epic 2+)
- Redis unavailable: Fall back to in-memory sessions (production) or return 503 (configurable)
- Frontend build missing: FastAPI returns 404 for root path (deployment validation catches this)

### Observability

**Logging (Story 1.1, 1.3):**
- Backend: Python `logging` module with structured logs
  - Development: Console output with DEBUG level
  - Production: JSON format with INFO level (future: ship to external service)
- Frontend: Browser console.log for development, remove in production build
- Log format: `[timestamp] [level] [module] message {context}`
- Required log events:
  - Server startup/shutdown
  - Database connection success/failure
  - Session creation/destruction (Epic 2)
  - API request/response (Epic 2+)
  - Errors with stack traces

**Metrics (Story 1.3):**
- Health check endpoint: Basic liveness indicator
- Future metrics (not in Epic 1):
  - Request count by endpoint
  - Response time percentiles (p50, p95, p99)
  - Database connection pool utilization
  - Session count and TTL distribution

**Tracing:**
- Not implemented in Epic 1 (foundational infrastructure only)
- Future: OpenTelemetry integration for distributed tracing (if needed)

**Development Monitoring:**
- Vite: HMR status messages in browser console
- FastAPI: Auto-reload notifications in terminal
- PostgreSQL: Query logging in development (SQLAlchemy echo=True)

**Production Monitoring Hooks:**
- Health check endpoint: `/health` for load balancer probes
- OpenAPI docs: `/docs` for API exploration and validation
- Future: Prometheus metrics endpoint `/metrics` (Epic 7)

## Dependencies and Integrations

**Frontend Dependencies (package.json)**

```json
{
  "dependencies": {
    "react": "^19.2.0",
    "react-dom": "^19.2.0",
    "react-router-dom": "^7.9.0",
    "zustand": "^5.0.8"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "typescript": "^5.9.0",
    "vite": "^7.1.9",
    "@vitejs/plugin-react": "^4.3.4",
    "tailwindcss": "^4.0.0",
    "postcss": "^8.4.49",
    "autoprefixer": "^10.4.20",
    "eslint": "^9.18.0",
    "prettier": "^3.4.2"
  }
}
```

**Backend Dependencies (requirements.txt)**

```
# Core Framework
fastapi==0.121.1
uvicorn[standard]==0.34.0
pydantic==2.10.6
pydantic-settings==2.7.1

# Database
sqlalchemy==2.0.44
alembic==1.16.0
asyncpg==0.30.0
psycopg[binary,pool]==3.2.3

# Authentication (future Epic 2, but dependencies added now)
msal==1.34.0
python-jose[cryptography]==3.3.0
python-multipart==0.0.19

# Session Storage
redis==5.2.1
aioredis==2.0.1

# Development/Quality
black==24.10.0
ruff==0.9.1
pytest==8.3.4
pytest-asyncio==0.25.2
httpx==0.28.1  # For testing FastAPI
```

**External Services & Integration Points**

| Service | Purpose | Configuration | Epic |
|---------|---------|---------------|------|
| **PostgreSQL 16+** | Primary database | DATABASE_URL env var, connection pooling (min 5, max 20) | 1.2 |
| **Redis 7.x** | Production session storage | REDIS_URL env var, TLS in production | 1.4 |
| **Microsoft EntraID** | OAuth2 authentication provider | ENTRAID_CLIENT_ID, ENTRAID_CLIENT_SECRET, ENTRAID_TENANT_ID | Epic 2 |
| **Vite Dev Server** | Development proxy | Proxy /api/* to localhost:8000 | 1.1 |

**Environment Variables (Required)**

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/nomi

# Session Storage
SESSION_BACKEND=memory  # or "redis"
REDIS_URL=redis://localhost:6379/0  # if SESSION_BACKEND=redis
SESSION_SECRET_KEY=<random-secret-key>
SESSION_TTL_HOURS=24

# Application
ENV=development  # or "production"
LOG_LEVEL=DEBUG  # or "INFO"

# EntraID (Epic 2, added for completeness)
ENTRAID_CLIENT_ID=<azure-app-client-id>
ENTRAID_CLIENT_SECRET=<azure-app-client-secret>
ENTRAID_TENANT_ID=<azure-tenant-id>
ENTRAID_REDIRECT_URI=http://localhost:8000/api/auth/callback
```

**Development Tools**

- **Docker** (optional): PostgreSQL and Redis containers
- **Node.js 20+**: Frontend package management and build
- **Python 3.10+**: Backend runtime
- **Git**: Version control

**No External API Integrations in Epic 1** - EntraID integration deferred to Epic 2.

## Acceptance Criteria (Authoritative)

**AC-1.1: Working Development Environment**
- Frontend runs at `http://localhost:5173` with Vite HMR functional
- Backend runs at `http://localhost:8000` with FastAPI auto-reload functional
- Vite proxy forwards `/api/*` requests to backend
- Project structure follows vertical slice architecture (features/, core/)
- Package management configured (npm for frontend, pip for backend)
- Linting configured (ESLint + Prettier for frontend, Black + Ruff for backend)

**AC-1.2: Database Infrastructure Operational**
- PostgreSQL connection established successfully
- SQLAlchemy base model class configured
- Alembic initialized with migration support
- Users table exists with fields: id (UUID), email, name, entraid_user_id, created_at, updated_at
- `alembic upgrade head` applies migrations successfully
- Database settings loaded from `.env` file

**AC-1.3: API Documentation Accessible**
- `GET /health` returns `{"status": "healthy"}` with 200 OK
- `GET /docs` displays Swagger UI with API documentation
- `GET /redoc` displays ReDoc documentation interface
- OpenAPI metadata includes title, version, description

**AC-1.4: Session Storage Configured**
- Development mode uses in-memory session storage
- Production mode uses Redis session storage (configurable)
- Session manager provides `create_session()`, `get_session()`, `delete_session()` interface
- SESSION_BACKEND environment variable controls storage backend
- Session TTL set to 24 hours (configurable)

**AC-1.5: Frontend Routing Established**
- React app displays with header/navigation
- Routes configured: `/` (home), `/login`, `/tasks`, `/inspirations`, `/profile`
- Navigation links visible in header
- Protected route wrapper component exists (placeholder)
- Tailwind CSS configured and functional
- Responsive design considerations in place

**AC-1.6: Production Deployment Ready**
- `npm run build` compiles frontend to `frontend/dist`
- FastAPI serves static files from `frontend/dist` at root `/`
- API endpoints accessible at `/api/*`
- SPA routing supported (fallback to `index.html` for client-side routes)
- Deployment instructions documented in README

## Traceability Mapping

| AC | Story | Spec Section | Components/APIs | Test Idea |
|----|-------|--------------|-----------------|-----------|
| **AC-1.1** | Story 1.1 | Services and Modules: Vite Dev Server, FastAPI App | `vite.config.ts`, `app/main.py`, `package.json`, `requirements.txt` | Start both servers, verify HMR with file change, verify proxy with API call |
| **AC-1.2** | Story 1.2 | Data Models: Users Table, SQLAlchemy Model | `app/core/database.py`, `app/features/users/model.py`, `alembic/versions/` | Run migration, query users table schema, verify UUID primary key |
| **AC-1.3** | Story 1.3 | APIs and Interfaces: Health Check, API Docs | `app/main.py` (health endpoint), FastAPI auto-docs | `GET /health` returns 200, `/docs` loads Swagger UI |
| **AC-1.4** | Story 1.4 | Data Models: Session Manager Interface | `app/core/session_store.py`, `app/core/config.py` | Create/get/delete session, verify TTL, test both Redis and in-memory modes |
| **AC-1.5** | Story 1.5 | APIs and Interfaces: Frontend Routing | `src/App.tsx`, `src/pages/`, `src/components/layout/` | Navigate to each route, verify rendering, check navigation links |
| **AC-1.6** | Story 1.6 | APIs and Interfaces: Production Static File Serving | `app/main.py` (StaticFiles mount), `frontend/dist/` | Build frontend, start FastAPI in prod mode, verify static files and SPA routing |

## Risks, Assumptions, Open Questions

**RISK-1:** PostgreSQL installation and configuration may vary across development environments (macOS, Windows, Linux, Docker)
- **Mitigation:** Provide Docker Compose configuration for consistent PostgreSQL + Redis setup. Document both Docker and native installation paths.

**RISK-2:** Vite proxy configuration may not perfectly mirror production single-server deployment
- **Mitigation:** Test production build frequently. Document known differences (CORS headers, cookie behavior).

**RISK-3:** Session storage switching (memory ↔ Redis) may have edge cases
- **Mitigation:** Create integration tests for both backends. Document environment variable requirements clearly.

**RISK-4:** Python/Node version mismatches across team members
- **Mitigation:** Document required versions prominently (Python 3.10+, Node 20+). Consider `.python-version` and `.nvmrc` files.

**ASSUMPTION-1:** Developers have basic familiarity with React, Python, PostgreSQL, and Git
- **Validation:** Provide clear setup guide with links to external resources for unfamiliar concepts.

**ASSUMPTION-2:** Development environment has at least 8GB RAM for running PostgreSQL + Redis + dev servers
- **Validation:** Document minimum system requirements in README.

**ASSUMPTION-3:** EntraID authentication dependencies can be installed now even though feature is Epic 2
- **Validation:** Confirm MSAL Python and related libraries don't conflict with current implementation.

**ASSUMPTION-4:** Tailwind CSS 4.0 configuration is stable (it's relatively new)
- **Validation:** Follow Tailwind 4.0 migration guide. Fallback to Tailwind 3.x if blocking issues arise.

**QUESTION-1:** Should we use Poetry instead of pip + requirements.txt for backend dependency management?
- **Decision needed:** Requirements.txt is simpler for learning project. Poetry adds complexity but better dependency resolution. **Recommendation:** Start with requirements.txt, can migrate later.

**QUESTION-2:** Should we include Docker Compose configuration in Story 1.2 or defer to Epic 7?
- **Decision needed:** Docker Compose highly useful for development but adds scope. **Recommendation:** Include basic `docker-compose.yml` for PostgreSQL + Redis in Story 1.2.

**QUESTION-3:** What level of test coverage is expected for Epic 1 infrastructure code?
- **Decision needed:** See Test Strategy below. **Recommendation:** Focus on integration tests over unit tests for infrastructure.

## Test Strategy Summary

**Testing Philosophy for Epic 1:**
Infrastructure and setup code benefits more from **integration testing** than unit testing. Focus on "does it work end-to-end?" rather than isolated unit tests for configuration modules.

**Test Levels:**

1. **Manual Testing (Primary for Epic 1)**
   - Developer verification after each story completion
   - Checklist-based testing against acceptance criteria
   - Visual verification of frontend rendering and routing
   - API testing via Swagger UI (`/docs`)

2. **Integration Tests (Backend)**
   - Framework: pytest + pytest-asyncio + httpx (FastAPI TestClient)
   - Coverage:
     - Database connection and migration application
     - Health check endpoint returns correct response
     - Session storage create/get/delete operations (both Redis and in-memory)
     - Static file serving in production mode
   - Test file: `tests/test_infrastructure.py`

3. **End-to-End Tests (Optional for Epic 1)**
   - Framework: Playwright or Cypress (if time permits)
   - Coverage:
     - Frontend loads at localhost:5173
     - All routes render without errors
     - Vite proxy forwards API requests correctly

**Test Coverage Goals:**
- Epic 1: ~60% coverage (infrastructure focus, manual testing acceptable)
- Future epics: 80%+ coverage for business logic (feature code)

**Testing Approach by Story:**

| Story | Test Type | Test Description |
|-------|-----------|------------------|
| **1.1** | Manual | Start servers, verify HMR works, check file structure |
| **1.2** | Integration | `test_database_connection()`, `test_migration_creates_users_table()` |
| **1.3** | Integration | `test_health_endpoint()`, `test_docs_accessible()` |
| **1.4** | Integration | `test_session_manager_memory()`, `test_session_manager_redis()` |
| **1.5** | Manual | Navigate to all routes, verify rendering and navigation |
| **1.6** | Integration | `test_static_files_served()`, `test_spa_fallback_routing()` |

**Edge Cases to Test:**
- Database connection failure: Health check should handle gracefully
- Invalid DATABASE_URL: Application startup should fail with clear error
- Redis unavailable (production mode): Fallback or clear error message
- Missing .env file: Application should fail with helpful message
- Frontend build missing: FastAPI should return 404 (not crash)

**Test Execution:**
```bash
# Backend tests
cd nomi-backend
pytest tests/ -v --cov=app

# Frontend (if tests added)
cd nomi-frontend
npm test
```

**Definition of Done (Testing):**
- All acceptance criteria manually verified and documented
- Integration tests written for critical paths (database, session, health check)
- README includes setup and test instructions
- Known issues/limitations documented
