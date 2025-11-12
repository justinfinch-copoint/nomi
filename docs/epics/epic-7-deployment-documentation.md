# Epic 7: Deployment & Documentation

**Epic Goal:** Production-ready deployment and comprehensive architectural knowledge capture, ensuring the template is deployable and well-documented for future reference and reuse.

**Value:** Makes the project truly useful as a reference template. Documentation captures architectural decisions and deployment patterns that are critical learning outcomes. Enables others to understand, deploy, and extend the project.

---

## Story 7.1: Create Deployment Documentation

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

## Story 7.2: Create Architecture Decision Records (ADRs)

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

## Story 7.3: Create Comprehensive README

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

## Story 7.4: Add API Documentation with Examples

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

## Story 7.5: Add Developer Setup Guide

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

## Story 7.6: Create Testing Documentation and Examples

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
