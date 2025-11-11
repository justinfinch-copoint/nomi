# Product Brief: Nomi

**Date:** 2025-11-11
**Author:** Justin
**Context:** Technical Architecture Proof-of-Concept

---

## Executive Summary

Nomi is a technical learning project designed to prove out a React + Python BFF (Backend for Frontend) architecture using a realistic but simplified todo list application domain. The project prioritizes clean architectural patterns, separation of concerns, and demonstrating modern full-stack development practices over feature complexity or market viability.

The application draws inspiration from reimagining traditional todo lists (task management + inspiration capture), but implements only core features necessary to validate the architectural approach.

---

## Core Vision

### Problem Statement

Building modern full-stack applications requires understanding how to properly structure a React frontend with a Python backend, particularly using the BFF pattern. Many tutorials and examples are either too trivial (hello world) or too complex (enterprise systems), making it difficult to learn architectural patterns in a realistic but manageable context.

### Proposed Solution

Nomi serves as a **realistic architectural reference implementation** - complex enough to demonstrate real-world patterns (authentication, CRUD operations, data relationships, API design) but simple enough to remain focused on architecture over feature bloat.

Using a todo list domain provides familiar, well-understood functionality that allows focus on the "how" (architecture) rather than the "what" (requirements discovery).

---

## Target Users

### Primary User

**Justin (Developer/Architect)** - Learning and validating React + Python BFF architectural patterns through hands-on implementation.

**Technical Goals:**
1. **Authentication & Authorization Flows** - Implement EntraID/MSAL authentication with session-based API security (HTTP-only cookies), protected routes, and user-specific data access patterns
2. **React State Management** - Learn and implement Zustand for client-side state management across the application
3. **Deployment Architecture** - Prove out single-server deployment pattern with FastAPI serving both React static files and API endpoints, with PostgreSQL and session storage

**Success Criteria:**
- Clean, maintainable code architecture
- Working EntraID authentication with session-based API security
- Protected routes with no tokens exposed to browser (HTTP-only cookies only)
- Demonstrable BFF patterns with REST API
- Successfully deployed and running application
- Reusable architectural patterns for future projects

---

## MVP Scope

### Core Features

**Minimal feature set designed to prove architectural patterns:**

1. **User Authentication & Authorization**
   - EntraID authentication with MSAL (Microsoft identity platform)
   - Session-based authentication with HTTP-only cookies
   - Protected routes (frontend)
   - User-specific data access (backend)
   - **Why:** Proves enterprise authentication flows, secure session management, protected API endpoints, and user context management without exposing tokens to browser

2. **Task Management (CRUD)**
   - Create, read, update, delete tasks
   - Tasks belong to authenticated users
   - Basic task properties: title, description, status (todo/done)
   - **Why:** Demonstrates REST API patterns, database relationships, and state management

3. **Inspiration Capture**
   - Separate "inspiration" items (distinct from tasks)
   - Simple CRUD operations for inspirations
   - Basic properties: title, description, date captured
   - Optional: Convert inspiration → task
   - **Why:** Demonstrates multiple related entities, data relationships, and state management across different types

4. **Basic Organization**
   - Filter by type (tasks vs inspirations)
   - Filter by status (for tasks: todo/done)
   - Simple list views
   - **Why:** Demonstrates client-side filtering and Zustand state patterns

**Feature Selection Criteria:**
- Simple enough to keep focus on architecture, not feature complexity
- Realistic enough to require proper REST API design, authentication, and state management
- Covers key technical patterns: CRUD, auth, relationships, filtering, state management

### Out of Scope for MVP

Advanced features from brainstorming session:
- AI-powered task complexity analysis
- Mood/energy-based scheduling algorithms
- Voice activation / "Hey Nomi" interface
- XP/skill progression systems
- Task delegation/outsourcing integrations
- AI-generated inspiration seeds
- Advanced scheduling logic
- Task mix/playlist features

**Why:** These add significant feature complexity without additional architectural learning value. The MVP feature set is sufficient to prove all key architectural patterns while remaining manageable in scope.

---

## Technical Preferences

### Confirmed Technology Stack

**Frontend:**
- **React 18+** with **Vite** (modern, fast dev server, HMR)
- **@azure/msal-react** and **@azure/msal-browser** for EntraID authentication flow
- **Zustand** for state management (modern, minimal boilerplate, performant)
- TypeScript (optional but recommended for type safety)
- React Router for client-side routing
- Styling: TBD (Tailwind CSS, CSS Modules, or styled-components)

**Backend:**
- **FastAPI** (Python 3.10+)
- **BFF Pattern** (Backend for Frontend) - API specifically tailored for React frontend needs
- **Pydantic** for data validation and type safety
- **SQLAlchemy** ORM for database interactions
- **MSAL Python** for EntraID/Azure AD integration
- **Session management** (Redis or in-memory for dev) with HTTP-only cookies
- **Alembic** for database migrations

**Database:**
- **PostgreSQL** (production-grade relational database)

**API Design:**
- **REST API** with clear resource-based endpoints
- OpenAPI/Swagger documentation (auto-generated by FastAPI)
- JSON request/response format

**Authentication:**
- **EntraID (Azure AD)** with **MSAL (Microsoft Authentication Library)** for identity provider
- **Session-based authentication** with HTTP-only cookies
- **Server-side token management** - access/refresh tokens never exposed to browser
- Backend exchanges MSAL tokens for server-managed sessions
- Protected API endpoints using session validation

### Key Architectural Patterns to Implement

1. **BFF Pattern**
   - Backend tailored specifically for frontend needs
   - Aggregation and transformation of data for optimal frontend consumption
   - Single API layer between React and database

2. **Authentication Flow (EntraID + Session-Based)**
   - Frontend initiates MSAL authentication with EntraID
   - User authenticates with Microsoft (redirect flow)
   - Backend receives MSAL token, validates with EntraID
   - Backend creates server-side session, returns HTTP-only cookie
   - All API requests use session cookie (credentials: 'include')
   - **No tokens stored in browser** - enhanced security against XSS attacks
   - Client-side auth state management with Zustand (user info only, no tokens)
   - Protected routes in React Router based on session state

3. **State Management Architecture**
   - Zustand stores for global app state (auth, user profile)
   - Local component state where appropriate
   - Separation of server state (API data) and client state (UI state)

4. **REST API Design**
   - Resource-based URL structure (`/api/tasks`, `/api/inspirations`, `/api/users`)
   - Proper HTTP methods (GET, POST, PUT, DELETE)
   - Consistent response formats
   - Error handling and validation

5. **Deployment Architecture**
   - **Single-server deployment** - FastAPI serves both API and React static files
   - Frontend built files served at root (`/`)
   - API endpoints at `/api/*`
   - **No CORS complexity** - same origin for frontend and backend
   - **Seamless cookie authentication** - same domain, no credentials configuration needed
   - Database hosting (managed PostgreSQL or containerized)
   - Session storage (Redis for production, in-memory for dev)
   - Environment configuration management

### Authentication Architecture Details

**Security-First Approach: No Tokens in Browser**

Traditional SPA authentication often stores JWT tokens in localStorage or sessionStorage, exposing them to XSS attacks. Nomi implements a more secure pattern:

**Flow:**
1. **Frontend (React + MSAL):** User clicks "Sign in with Microsoft"
2. **MSAL Redirect:** User redirected to Microsoft login page (EntraID)
3. **Microsoft Authentication:** User enters credentials, completes MFA if required
4. **MSAL Callback:** Microsoft redirects back with authorization code
5. **Token Exchange (Frontend):** MSAL exchanges code for access token (handled in browser memory, not persisted)
6. **Backend Session Exchange:** Frontend sends MSAL token to backend `/auth/session` endpoint
7. **Backend Validation:** Backend validates token with Microsoft Graph API
8. **Session Creation:** Backend creates server-side session (stored in Redis/memory)
9. **Cookie Response:** Backend returns HTTP-only, Secure, SameSite cookie with session ID
10. **Subsequent Requests:** All API calls include session cookie automatically (credentials: 'include')
11. **MSAL Token Discarded:** Frontend discards MSAL token after session exchange

**Security Benefits:**
- ✅ No access tokens stored in browser (immune to XSS token theft)
- ✅ HTTP-only cookies cannot be accessed by JavaScript
- ✅ SameSite protection against CSRF attacks
- ✅ Secure flag ensures cookies only sent over HTTPS
- ✅ Server-side session validation on every request
- ✅ Easy session revocation (delete server-side session)

**Trade-offs:**
- Requires session storage infrastructure (Redis recommended for production)
- Backend becomes stateful (sessions must be shared across instances)
- Slightly more complex than pure JWT approach

**Why This Matters for Learning:**
This architecture represents enterprise-grade security patterns used in production systems. It's more complex than tutorial-level JWT, but teaches real-world security considerations.

### Deployment Architecture Details

**Single-Server Pattern: Simplicity and Security**

Rather than deploying frontend and backend separately (which introduces CORS complexity), Nomi uses a single-server deployment where FastAPI serves both the API and the React application.

**Architecture:**
```
                     ┌─────────────────────────┐
                     │   Single Server         │
                     │   (FastAPI)             │
                     │                         │
  Browser ──────────►│  /            → React   │
                     │  /api/*       → FastAPI │
                     │  /auth/*      → Auth    │
                     │                         │
                     │  Same Origin            │
                     │  ✅ No CORS             │
                     │  ✅ Cookies work        │
                     └─────────────────────────┘
                               │
                               ▼
                     ┌─────────────────────────┐
                     │  PostgreSQL + Redis     │
                     └─────────────────────────┘
```

**Benefits:**
- ✅ **No CORS configuration needed** - frontend and backend are same origin
- ✅ **Cookies work seamlessly** - no `credentials: 'include'` complexity
- ✅ **Simpler deployment** - single server to manage, single domain/URL
- ✅ **Faster development** - no CORS debugging, no cross-origin issues
- ✅ **Production-ready pattern** - used by many enterprise internal applications
- ✅ **All architectural learning goals met** - BFF, auth, state management all still demonstrated

**Implementation:**
1. React (Vite) builds to `frontend/dist`
2. FastAPI mounts `/dist` as static files at root
3. API routes defined at `/api/*` prefix
4. Fallback to `index.html` for React Router (SPA routing)

**Development Workflow:**
- **Dev:** Vite dev server (port 5173) + FastAPI (port 8000)
  - Vite proxy configuration forwards `/api/*` requests to FastAPI
  - **No CORS issues** - browser sees requests as same-origin
  - **Full HMR support** - hot module reload works while proxying API calls
  - Configuration in `vite.config.ts`:
    ```typescript
    server: {
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
        },
      },
    }
    ```
- **Production:** Single FastAPI server serves both built React and API

**Why This Approach:**
Separate frontend/backend hosting is valuable for high-scale applications with CDN needs, but adds unnecessary complexity for a learning project. This single-server pattern focuses learning on architecture (BFF, auth, state) rather than deployment infrastructure complexity.

---

## Technical Constraints & Considerations

### Simplicity over Perfection
- Focus on clear, understandable architecture over premature optimization
- Document architectural decisions for future reference
- Prioritize learning and experimentation over production-grade hardening

### Development Approach
- Build features incrementally (auth → tasks → inspirations → filtering)
- Test each architectural pattern as it's implemented
- Keep deployment in mind from the start (avoid "works on my machine" issues)

### Development Environment
- **Frontend:** Vite dev server (port 5173) with HMR
- **Backend:** FastAPI with uvicorn (port 8000)
- **Proxy:** Vite proxy forwards `/api/*` to FastAPI (no CORS issues)
- **Database:** PostgreSQL (local or Docker)
- **Session Storage:** In-memory for dev (Redis for production)

**Key Benefit:** Vite proxy allows same-origin requests during development, avoiding CORS complexity while maintaining full HMR capabilities. This mirrors the production single-server architecture where frontend and API are served from the same origin.

### Known Learning Challenges
1. **First-time Zustand usage** - expect iteration on state management patterns
2. **EntraID/MSAL integration** - understanding redirect flows, token validation, and session exchange
3. **Session management** - implementing secure session storage (Redis or alternative) and HTTP-only cookie handling
4. **Vite proxy configuration** - setting up development proxy to avoid CORS while maintaining HMR
5. **Single-server deployment** - configuring FastAPI to serve both static files and API endpoints
6. **Build process integration** - automating React build and deployment to FastAPI static directory

---

## Success Metrics (Learning Goals)

**Technical Achievement Metrics:**
- ✅ Successfully deployed application accessible via URL
- ✅ Working EntraID authentication with MSAL
- ✅ Session-based API security with HTTP-only cookies (no tokens in browser)
- ✅ Protected routes on both frontend and backend
- ✅ CRUD operations working for tasks and inspirations
- ✅ Zustand state management implemented across app
- ✅ Clean separation of concerns (BFF pattern evident)

**Learning Outcome Metrics:**
- Understanding of EntraID/MSAL authentication flow (redirect, token exchange, session creation)
- Knowledge of session-based authentication and HTTP-only cookie security
- Proficiency with Zustand patterns (stores, actions, selectors)
- Knowledge of FastAPI project structure and best practices
- Experience with React + Vite modern development workflow
- Understanding of deployment architecture for full-stack apps with session management
- Reusable code patterns for future enterprise projects

**Documentation Goals:**
- Architectural decision records (why certain patterns were chosen)
- Setup/deployment documentation
- Code examples demonstrating key patterns

---

## Research & Stack Validation

**Stack choices validated through 2024-2025 industry research:**

**FastAPI:**
- Industry adoption: Uber, Microsoft, Netflix
- Performance: 3,000+ requests/sec (17ms response time)
- Explicitly recommended for BFF pattern implementations
- Auto-generates OpenAPI documentation
- Native async/await support

**Vite + React:**
- Create React App officially deprecated (2024)
- Vite now industry standard for React projects
- Millisecond startup vs 20-30 seconds (CRA)
- Native ES modules, modern tooling

**Zustand:**
- Modern state management standard for 2025
- Recommended for 90% of projects (MVPs, SaaS platforms)
- Minimal boilerplate compared to Redux
- High performance, simple API

**Sources:** Web research conducted 2025-01-11 covering current best practices and industry trends.

---

_This Product Brief captures the technical learning goals for Nomi as an architectural proof-of-concept project._

_The brainstorming session (docs/bmm-brainstorming-session-2025-11-10.md) explored the full product vision, but this brief intentionally scopes down to features that demonstrate architectural patterns without overwhelming complexity._

_Next: The PRD workflow will transform this brief into detailed epics and stories focused on implementing the architectural patterns._
