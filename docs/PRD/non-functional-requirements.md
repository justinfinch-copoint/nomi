# Non-Functional Requirements

Only documenting NFRs that matter for THIS project. Learning-focused architecture projects need different constraints than production systems - we focus on patterns that demonstrate good practices without over-engineering.

## Performance Requirements

**Why performance matters for Nomi:**
- User experience should feel snappy (validates efficient patterns)
- Demonstrates understanding of performance implications
- Proves state management doesn't cause unnecessary re-renders
- Shows proper database query optimization

### NFR-PERF-001: Page Load Performance
**Requirement:** Initial application load must complete within acceptable timeframes for modern web applications.

**Acceptance Criteria:**
- **Initial page load:** < 3 seconds (including auth redirect if needed)
- **Time to interactive:** < 2 seconds after HTML loaded
- **JavaScript bundle size:** < 500KB (gzipped)
- **Subsequent navigation:** < 500ms (client-side routing)

**Why these targets:**
- Achievable without complex optimization
- Good enough for internal tools
- Demonstrates awareness of performance concerns
- Won't frustrate users during development/testing

**Implementation Patterns:**
- Vite tree-shaking and code splitting
- Lazy load routes with React.lazy()
- Minimal dependencies (modern, well-maintained packages only)
- No large UI libraries (avoid Material-UI, use lightweight or custom components)

### NFR-PERF-002: API Response Time
**Requirement:** API endpoints must respond quickly for typical operations.

**Acceptance Criteria:**
- **CRUD operations:** < 500ms for individual operations
- **List operations:** < 1 second (assuming < 100 items)
- **Authentication flow:** < 2 seconds (excluding EntraID redirect time)

**Implementation Patterns:**
- Database indexes on user_id, created_at, updated_at
- Simple queries without complex joins
- Connection pooling for database
- Session caching to reduce session store lookups

### NFR-PERF-003: Frontend Rendering Efficiency
**Requirement:** UI updates must not cause unnecessary re-renders or performance degradation.

**Acceptance Criteria:**
- Task/inspiration list renders smoothly with 100+ items
- No visible lag when toggling task status
- Form inputs respond immediately to typing
- Zustand state updates don't trigger full app re-renders

**Implementation Patterns:**
- Zustand selectors for component-specific state subscriptions
- React.memo for expensive components
- Virtualized lists if item count grows beyond MVP (future)
- Debounce search/filter inputs if added

## Security Requirements

**Why security matters for Nomi:**
- **Primary learning goal:** Maximum-security authentication patterns
- Demonstrates defense-in-depth principles
- Proves understanding of OWASP top vulnerabilities
- Creates patterns safe for enterprise applications

### NFR-SEC-001: Authentication Security (Maximum Security Pattern)
**Requirement:** Authentication implementation must follow maximum-security best practices with zero token exposure to browser.

**Acceptance Criteria:**
- **Zero token exposure:** Access tokens and refresh tokens NEVER sent to browser
- **HTTP-only cookies:** Session cookie inaccessible to JavaScript (XSS protection)
- **Signed cookies:** Cookie signature prevents tampering
- **Secure flag:** Cookies only sent over HTTPS in production
- **SameSite protection:** SameSite=Lax prevents CSRF attacks
- **Server-side validation:** Every protected endpoint validates session
- **Session expiry:** Sessions expire after 24 hours inactivity
- **Logout invalidation:** Logout immediately destroys server-side session

**Why maximum security:**
- Learning goal: understand enterprise-grade patterns
- Complete immunity to XSS token theft
- Defense-in-depth approach
- Patterns reusable for high-security applications

**Implementation Patterns:**
- MSAL Python for OAuth2 token exchange (server-side only)
- Redis/in-memory session storage with signed session IDs
- FastAPI middleware for session validation
- No Authorization headers, no bearer tokens, no localStorage

### NFR-SEC-002: Data Access Control
**Requirement:** Users must only access their own data - complete isolation between users.

**Acceptance Criteria:**
- All database queries filter by user_id from session
- Backend validates user ownership before update/delete operations
- API returns 403 Forbidden if user attempts to access another user's resource
- No data leakage between users under any circumstances

**Implementation Patterns:**
- User context extracted from session in middleware
- All database queries include WHERE user_id = {session.user_id}
- Ownership validation in CRUD operations before any modification
- Integration tests verify isolation

### NFR-SEC-003: Input Validation & Injection Prevention
**Requirement:** All user input must be validated and sanitized to prevent injection attacks.

**Acceptance Criteria:**
- **SQL injection protection:** Parameterized queries (SQLAlchemy ORM)
- **XSS protection:** Input sanitization on backend, output encoding in frontend
- **Length validation:** Title (200 chars), Description (2000 chars) enforced
- **Type validation:** Pydantic models validate data types
- **No code execution:** User input never executed as code

**Implementation Patterns:**
- SQLAlchemy ORM (prevents SQL injection)
- Pydantic validation models for all API inputs
- Character limits enforced on frontend and backend
- HTML escaping in frontend (React default escaping)
- No eval(), no innerHTML, no dangerouslySetInnerHTML

### NFR-SEC-004: Error Handling & Information Disclosure
**Requirement:** Error messages must not leak sensitive information or system details.

**Acceptance Criteria:**
- Production errors show generic messages: "An error occurred. Please try again."
- Stack traces never returned to client (log server-side only)
- Database errors abstracted: "Could not complete operation"
- 404 vs 403 carefully chosen (don't reveal resource existence)

**Implementation Patterns:**
- FastAPI exception handlers return safe error messages
- Logging sensitive errors server-side
- Environment-based error verbosity (detailed in dev, generic in prod)

### NFR-SEC-005: Dependency Security
**Requirement:** Project dependencies must be kept up-to-date and free of known vulnerabilities.

**Acceptance Criteria:**
- Run `npm audit` and `pip audit` before deployment
- No high or critical vulnerabilities in production
- Document all dependencies with version constraints
- Regular dependency updates (monthly or when vulnerabilities announced)

**Implementation Patterns:**
- Lock files (package-lock.json, requirements.txt with versions)
- Dependabot or similar for vulnerability alerts
- Minimal dependencies (fewer attack surfaces)

## Reliability Requirements

**Why reliability matters for Nomi:**
- Demonstrates proper error handling patterns
- Shows graceful degradation
- Learning goal: understand failure modes and recovery

### NFR-REL-001: Error Handling & Recovery
**Requirement:** Application must handle errors gracefully without crashing or losing user data.

**Acceptance Criteria:**
- API failures show user-friendly error messages with retry options
- Failed form submissions don't lose user input
- Session expiry redirects to login without data loss
- Network errors handled gracefully (offline support not required, but error state shown)
- Unhandled errors caught by error boundary (React)

**Implementation Patterns:**
- React Error Boundaries for component crashes
- Try-catch blocks in API calls with user-friendly error messages
- Toast notifications for transient errors
- Form state preserved until successful submission
- Loading states and error states for all async operations

### NFR-REL-002: Database Integrity
**Requirement:** Database must maintain referential integrity and prevent data corruption.

**Acceptance Criteria:**
- Foreign key constraints enforced (tasks.user_id → users.id)
- Cascade deletes defined (if user deleted, delete tasks - not in MVP but structure for it)
- Transactions for multi-step operations
- Database migrations tracked with Alembic

**Implementation Patterns:**
- SQLAlchemy foreign key relationships
- Alembic migrations for schema changes
- Database constraints enforced at schema level

## Maintainability Requirements

**Why maintainability matters for Nomi:**
- **Core learning goal:** Create reusable, understandable code
- Pattern library must be easy to adapt for future projects
- Code should be self-documenting through clarity

### NFR-MAINT-001: Code Quality & Readability
**Requirement:** Code must be clean, well-organized, and easy to understand for future reference.

**Acceptance Criteria:**
- Consistent code style (linting: ESLint for JS, Black/Ruff for Python)
- Meaningful variable and function names
- Components < 200 lines (extract if larger)
- API endpoints have clear docstrings
- Complex logic has explanatory comments

**Implementation Patterns:**
- ESLint + Prettier for frontend
- Black + Ruff for backend formatting
- Pre-commit hooks for linting
- Code review checklist (even for solo project)

### NFR-MAINT-002: Project Structure & Organization
**Requirement:** Project structure must be logical and follow best practices for React + FastAPI projects.

**Acceptance Criteria:**
- **Frontend structure:**
  ```
  frontend/
    src/
      components/     (reusable UI components)
      pages/          (route components)
      stores/         (Zustand stores)
      services/       (API client functions)
      utils/          (helper functions)
      App.tsx
      main.tsx
  ```
- **Backend structure:**
  ```
  backend/
    app/
      api/            (route handlers)
      models/         (SQLAlchemy models)
      schemas/        (Pydantic schemas)
      services/       (business logic)
      core/           (config, security, dependencies)
      main.py
  ```

**Implementation Patterns:**
- Separation of concerns (routes, business logic, data access)
- Feature-based or layer-based organization (choose one, be consistent)
- No circular dependencies

### NFR-MAINT-003: Documentation
**Requirement:** Project must include documentation for setup, architecture decisions, and common patterns.

**Acceptance Criteria:**
- **README.md:** Project overview, setup instructions, tech stack
- **SETUP.md:** Detailed environment setup, EntraID configuration, local development
- **ARCHITECTURE.md:** Architectural decisions, patterns used, why choices were made
- **API documentation:** Auto-generated with FastAPI (OpenAPI/Swagger)
- **Code comments:** Complex logic explained inline

**Implementation Patterns:**
- Markdown documentation in project root
- ADRs (Architectural Decision Records) for key choices
- FastAPI automatic OpenAPI docs
- Inline comments for non-obvious code

## What We're NOT Including (And Why)

**Scalability:** Not needed for learning project. Single-server deployment sufficient. No load balancing, no horizontal scaling, no microservices.

**High Availability:** Not needed. Downtime acceptable for learning project. No redundancy, no failover.

**Advanced Accessibility:** Basic Level A covered in UX section. AA/AAA not required for learning goals.

**Internationalization:** English only. No i18n complexity for learning project.

**Analytics/Monitoring:** Basic logging only. No APM, no metrics dashboard. Can add later if desired.

**Backup/Disaster Recovery:** Not required for learning project. Database backups good practice but not mandated.

## NFR Summary

**Total NFRs:** 13 requirements across 4 categories

**Categories Included:**
- ✅ Performance (3 requirements) - Good UX and efficient patterns
- ✅ Security (5 requirements) - Core learning goal, maximum security patterns
- ✅ Reliability (2 requirements) - Proper error handling and data integrity
- ✅ Maintainability (3 requirements) - Code quality for reference implementation

**Categories Skipped:**
- ❌ Scalability - Not needed for single-user learning project
- ❌ High Availability - Downtime acceptable
- ❌ Advanced Accessibility - Basic covered in UX section
- ❌ Internationalization - Out of scope

**Every NFR supports the learning goals - security is prioritized (the auth patterns are the crown jewel), performance is reasonable, maintainability ensures the code remains a useful reference.**

---
