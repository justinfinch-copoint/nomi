# Nomi - Product Requirements Document

**Author:** Justin
**Date:** 2025-11-12
**Version:** 1.0

---

## Executive Summary

Nomi is a technical learning project that provides a **reusable architectural template** for building modern full-stack applications with React and Python. The project demonstrates enterprise-grade patterns (server-side OAuth2, BFF architecture, session-based security, single-server deployment) in a realistic but manageable context - complex enough to prove real-world patterns, simple enough to understand and adapt for future projects.

The application uses a familiar todo list domain intentionally - not to compete with existing products, but to allow complete focus on architectural patterns without getting lost in complex requirements discovery. By the end, you'll have a reference implementation that answers "how do I properly structure this?" for authentication, state management, API design, and deployment in a React + Python stack.

### What Makes This Special

**The "Goldilocks" Architectural Template**

Most code examples are either:
- **Too trivial:** "Hello World" tutorials that don't demonstrate real authentication, state management, or deployment
- **Too complex:** Enterprise codebases with overwhelming abstractions, microservices, and infrastructure that obscure the core patterns

Nomi sits in the sweet spot - **just right complexity**:
- Real EntraID authentication with maximum security (server-side OAuth2, HTTP-only cookies, zero token exposure)
- Production-ready patterns (BFF architecture, proper state management, session handling)
- Single-server deployment that eliminates CORS complexity while remaining production-viable
- Clean separation of concerns without over-engineering
- Fully functional application that can be deployed, used, and shown to others

**The magic moment:** Opening the codebase 6 months from now when starting a new project and thinking "I know exactly how to structure this because I proved it in Nomi" - then copying architectural patterns with confidence instead of second-guessing or over-Googling.

---

## Project Classification

**Technical Type:** Web Application (React SPA + Python BFF)
**Domain:** General Purpose (Learning/Reference Project)
**Complexity:** Medium (Architectural focus, simplified features)

This is a **greenfield software project** on the **BMad Method track** - meaning comprehensive planning from vision through architecture before implementation. The project intentionally uses a simple domain (task/inspiration management) to maximize focus on architectural learning goals rather than feature complexity.

**Why Web App Classification:**
- Single-page application (SPA) with React + Vite
- Python FastAPI backend serving both static files and API
- Browser-based interface with modern responsive design
- Real-time client-server interaction via REST API
- Session-based authentication with HTTP-only cookies

**Why General Domain:**
- No complex regulatory requirements (healthcare, fintech, government)
- No specialized domain knowledge needed
- Familiar problem space (task management) allows architecture focus
- Patterns are transferable to any domain

### Domain Context

**Learning-Focused Architecture Project**

Unlike production applications with market validation requirements, Nomi optimizes for **learning outcomes and pattern reusability**:

- **Primary metric:** Code clarity and architectural cleanliness
- **Success definition:** Patterns are understandable and transferable to other projects
- **Constraints:** Keep features simple enough to maintain architecture focus
- **Trade-offs:** Favor educational value over feature completeness

This context shapes every requirement: features exist to demonstrate architectural patterns, not to achieve market fit.

---

## Success Criteria

Success for Nomi is measured by **learning outcomes and architectural clarity**, not user adoption or revenue metrics. The project succeeds when it becomes a trusted reference implementation that accelerates future development.

### Technical Achievement Metrics

**Architecture Proof Points:**
- ✅ Successfully deployed application accessible via public URL
- ✅ EntraID authentication working with MSAL Python (OAuth2 authorization code flow)
- ✅ Session-based API security with HTTP-only signed cookies
- ✅ Zero tokens exposed to browser (complete XSS immunity for auth)
- ✅ Protected routes on both frontend (React Router) and backend (FastAPI)
- ✅ CRUD operations working for all entities (tasks, inspirations)
- ✅ Zustand state management implemented consistently across application
- ✅ Clean BFF pattern evident in code structure
- ✅ Single-server deployment serving both React and API from same origin

**Code Quality Indicators:**
- Code is readable and well-commented (explaining architectural decisions)
- Clear separation of concerns (frontend/backend, auth/business logic, state/UI)
- Patterns are consistent throughout codebase
- No "works on my machine" issues - reproducible setup

### Learning Outcome Metrics

**Knowledge Gained:**
- Deep understanding of server-side OAuth2 authorization code flow with EntraID
- Practical knowledge of MSAL Python for token exchange and validation
- Expertise in session-based authentication with signed HTTP-only cookies
- Understanding when to use server-side vs client-side auth patterns
- Proficiency with Zustand patterns (stores, actions, selectors)
- Knowledge of FastAPI project structure and best practices
- Experience with React + Vite modern development workflow
- Understanding of single-server deployment architecture
- Reusable authentication patterns for maximum-security enterprise applications

**Pattern Library Created:**
- Authentication flow (OAuth2 → session → protected routes)
- State management structure (Zustand stores organization)
- API design patterns (BFF-style endpoints)
- Frontend/backend project structure
- Development environment configuration (Vite proxy, FastAPI static serving)
- Deployment configuration for single-server pattern

### Documentation Goals

**Architectural Decision Records (ADRs):**
- Why server-side OAuth2 instead of client-side MSAL?
- Why HTTP-only cookies instead of JWT in localStorage?
- Why single-server deployment instead of separate hosting?
- Why Zustand instead of Redux or Context API?
- Why FastAPI instead of Flask or Django?

**Setup Documentation:**
- EntraID application configuration steps
- Local development environment setup
- Deployment process and infrastructure requirements
- Environment variable configuration

**Code Examples Demonstrating Key Patterns:**
- Protected route implementation (frontend + backend)
- Zustand store creation and usage
- FastAPI endpoint with session validation
- OAuth2 callback handling
- Error handling patterns

**The Success Test:**
Six months from now, when starting a new React + Python project, you can:
1. Reference Nomi's auth implementation without hesitation
2. Copy and adapt architectural patterns confidently
3. Explain trade-offs to other developers clearly
4. Avoid common pitfalls you already solved in Nomi

---

## Product Scope

Scope is driven by **architectural learning value** - features exist to demonstrate patterns, not to build a competitive product. The MVP contains exactly what's needed to prove all key architectural patterns without overwhelming complexity.

### MVP - Minimum Viable Product

**Core principle:** Just enough features to demonstrate all critical architectural patterns in a realistic context.

#### 1. Authentication & Authorization (EntraID + Session-Based)
**What:**
- EntraID authentication with MSAL Python
- OAuth2 authorization code flow (fully server-side)
- Session-based authentication with HTTP-only signed cookies
- User profile management
- Protected routes (frontend React Router guards)
- Protected API endpoints (backend session validation)
- Logout functionality

**Why this is in MVP:**
- **Primary architectural pattern** to master
- Demonstrates complete OAuth2 flow from redirect through callback
- Proves server-side session management with Redis/in-memory storage
- Shows protected route patterns on both frontend and backend
- Maximum security pattern (zero token exposure) worth learning deeply

**Architectural value:** 10/10 - This is the crown jewel pattern.

#### 2. Task Management (CRUD Operations)
**What:**
- Create new tasks (title, description, status)
- Read/list all user's tasks
- Update task properties and status (todo → done)
- Delete tasks
- Tasks are user-specific (isolated by authenticated user)

**Why this is in MVP:**
- Demonstrates REST API design (resource-based endpoints)
- Shows database relationships (user → tasks)
- Proves Zustand state management for entity collections
- BFF pattern: backend shapes data for frontend needs
- CRUD is foundational - must be solid

**Architectural value:** 9/10 - Core full-stack pattern.

#### 3. Inspiration Capture (Secondary Entity)
**What:**
- Create inspirations (title, description, date captured)
- Read/list all user's inspirations
- Update inspiration properties
- Delete inspirations
- Optional: Convert inspiration → task (demonstrates entity relationships)

**Why this is in MVP:**
- Proves patterns work for multiple entity types
- Demonstrates managing related but distinct data models
- Shows state management across different entity types
- Tests API design consistency across resources
- Conversion feature shows cross-entity operations

**Architectural value:** 7/10 - Validates patterns aren't one-off, adds entity relationship complexity.

#### 4. Basic Organization & Filtering
**What:**
- Filter by entity type (tasks vs inspirations)
- Filter tasks by status (todo vs done)
- Simple list views for each entity type
- Basic sorting (by date created/updated)

**Why this is in MVP:**
- Demonstrates client-side filtering patterns in Zustand
- Shows UI state management (filter state separate from data)
- Tests query parameter handling if filters are URL-based
- Lightweight feature that proves state management patterns

**Architectural value:** 6/10 - Validates state management patterns for UI concerns.

### MVP Feature Selection Criteria

**Include if:**
- ✅ Demonstrates a new architectural pattern not yet proven
- ✅ Required to make other features realistic (auth required for user-specific data)
- ✅ Simple to implement but high learning value
- ✅ Common pattern you'll reuse in other projects

**Exclude if:**
- ❌ Adds feature complexity without new architectural patterns
- ❌ Requires significant infrastructure (AI, third-party APIs, complex algorithms)
- ❌ Distracts from core learning goals
- ❌ Can be added later without architectural refactoring

### Growth Features (Post-MVP)

**When MVP is complete and patterns are proven**, these features could be added to deepen specific pattern knowledge:

#### Enhanced Organization
- Tags/categories for tasks and inspirations
- Search functionality (full-text search patterns)
- Bulk operations (select multiple, batch actions)

**Learning value:** Advanced state management, search patterns, batch operation handling.

#### Collaboration Features (If exploring multi-user patterns)
- Share tasks/inspirations with other users
- Team workspaces
- Real-time updates (WebSocket patterns)

**Learning value:** Multi-tenant data isolation, real-time communication, WebSocket integration.

#### Rich Content
- Markdown support for descriptions
- File attachments
- Image uploads

**Learning value:** File upload patterns, storage integration (S3), content sanitization.

#### Enhanced UX
- Drag-and-drop reordering
- Keyboard shortcuts
- Dark mode toggle
- Mobile-responsive improvements

**Learning value:** Advanced UI patterns, responsive design, accessibility.

### Vision (Future Exploration)

**Features from brainstorming session** that are out of scope for architectural learning but interesting for product exploration:

- AI-powered task complexity analysis
- Mood/energy-based scheduling algorithms
- Voice activation / "Hey Nomi" interface
- XP/skill progression systems
- Task delegation/outsourcing integrations
- AI-generated inspiration seeds
- Advanced scheduling logic
- Task mix/playlist features

**Why deferred:** These add significant complexity and third-party dependencies without teaching new fundamental architectural patterns. They're product innovations, not architectural learning goals.

**Could be valuable if:** You specifically want to learn AI integration patterns, voice interface development, or gamification systems - but that would be a different project focus.

### Scope Rationale

The MVP feature set achieves the core goal: **a reusable architectural template that's not trivial but not overwhelming.**

- **Not trivial:** Real auth, multiple entities, state management, deployment - all production patterns
- **Not overwhelming:** 4 focused feature areas, familiar domain, no complex algorithms or infrastructure
- **Just right:** Proves all key patterns, remains understandable, stays manageable

Every feature in MVP demonstrates a pattern you'll reuse. Every feature excluded simplifies focus without losing architectural value.

---

## Web Application Specific Requirements

Nomi is a **Single-Page Application (SPA)** built with React + Vite, following modern web app patterns. These requirements shape the technical implementation and architectural decisions.

### Application Architecture Pattern

**SPA (Single-Page Application)**
- Client-side routing with React Router
- Dynamic content loading via API calls
- Single initial HTML load, subsequent navigation handled by JavaScript
- State managed client-side with Zustand
- Backend serves compiled static files + API endpoints

**Why SPA (not MPA):**
- Better demonstrates React patterns and Zustand state management
- Smoother user experience without full page reloads
- Clear separation between frontend state and backend API
- Modern standard for dashboard/tool applications
- Aligns with learning goals (client-side state management)

**Why not SSR/SSG:**
- Adds deployment complexity (Node.js server or build-time generation)
- Not required for authenticated application (no SEO needs)
- Focus remains on React + Python, not Next.js/Remix patterns
- Simpler mental model for learning

### Browser Support Matrix

**Target Browsers:**
- **Chrome/Edge:** Latest 2 versions (primary development browser)
- **Firefox:** Latest 2 versions
- **Safari:** Latest 2 versions

**Why modern browsers only:**
- Leverages modern JavaScript (ES6+) without transpilation complexity
- Supports modern CSS features (Grid, Flexbox, CSS variables)
- No legacy browser baggage (IE11, older Safari)
- Development efficiency - focus on patterns, not polyfills
- Realistic for internal tools / modern web apps

**Browser Features Required:**
- ES6+ JavaScript support
- Fetch API for HTTP requests
- LocalStorage for any client-side preferences
- Session cookies with secure, httpOnly, sameSite support
- Modern CSS (Grid, Flexbox, CSS Custom Properties)

### Responsive Design Requirements

**Design Approach:**
- **Desktop-first** with mobile responsive layouts
- Breakpoints: Desktop (1024px+), Tablet (768px-1023px), Mobile (320px-767px)
- Touch-friendly targets for mobile (min 44x44px touch areas)
- Responsive typography and spacing

**Why desktop-first:**
- Primary use case: focused work at a computer
- Learning project - not a mobile-first consumer app
- Simpler to build and test
- Mobile-responsive as quality bar, not primary experience

**Layout Patterns:**
- Responsive grid for task/inspiration lists
- Collapsible navigation for smaller screens
- Stack forms vertically on mobile
- No native mobile features (GPS, camera, push notifications)

### Performance Targets

**Page Load Performance:**
- **Initial load:** < 3 seconds (including auth redirect if needed)
- **Subsequent navigation:** < 500ms (client-side routing)
- **API response time:** < 1 second for typical CRUD operations
- **Time to interactive:** < 2 seconds after initial load

**Why these targets:**
- Reasonable for learning project, not over-optimized
- User experience remains snappy
- Achievable without complex performance engineering
- Realistic for internal tools / authenticated apps

**Performance Patterns to Implement:**
- Code splitting with React lazy loading (if app grows)
- Minimal bundle size (modern dependencies, tree-shaking)
- Efficient Zustand state updates (no unnecessary re-renders)
- Appropriate database indexes for common queries
- Session caching to reduce auth checks

### SEO Strategy

**SEO Requirements:** None

**Why no SEO:**
- Authenticated application (all content behind login)
- Not a public website or content platform
- Search engines can't index user-specific data
- Focus remains on application patterns, not marketing

**Meta tags included:**
- Basic HTML meta (title, viewport, charset)
- Favicon and app manifest for bookmarking
- No Open Graph, Twitter Cards, structured data

### Accessibility Requirements

**Target Level:** WCAG 2.1 Level A (Basic Compliance)

**Why Level A (not AA or AAA):**
- Learning project - demonstrates awareness, not enterprise accessibility
- Level A covers fundamental requirements (keyboard nav, alt text, color contrast basics)
- AA/AAA add complexity without additional architectural learning
- Can be enhanced post-MVP if accessibility patterns become a learning goal

**Minimum Accessibility Features:**
- **Keyboard navigation:** All interactive elements accessible via keyboard (Tab, Enter, Escape)
- **Semantic HTML:** Proper heading hierarchy, button vs div, form labels
- **ARIA labels:** Screen reader support for interactive elements
- **Focus management:** Visible focus indicators, logical tab order
- **Color contrast:** Text meets minimum contrast ratios
- **Form validation:** Clear error messages, accessible form feedback

**Accessibility Patterns:**
- Use semantic HTML elements (`<button>`, `<nav>`, `<main>`)
- Label all form inputs with `<label>` or `aria-label`
- Provide focus styles for keyboard navigation
- Announce dynamic content changes (form errors, success messages)
- Avoid color-only indicators (pair with icons/text)

### API Design (BFF Pattern)

**Endpoint Structure:**
```
/api/auth/login          → Initiate OAuth2 flow
/api/auth/callback       → Handle OAuth2 callback
/api/auth/me             → Get current user profile
/api/auth/logout         → Destroy session

/api/tasks               → GET (list), POST (create)
/api/tasks/{id}          → GET (read), PUT (update), DELETE (delete)

/api/inspirations        → GET (list), POST (create)
/api/inspirations/{id}   → GET (read), PUT (update), DELETE (delete)
/api/inspirations/{id}/convert → POST (convert to task)

/api/users/me            → GET (user profile and preferences)
```

**BFF Principles Applied:**
- Endpoints shaped for frontend needs (not generic CRUD)
- Backend aggregates data (user + tasks in one call if needed)
- Backend handles complex logic (auth, validation, business rules)
- Frontend receives ready-to-render data
- Response formats optimized for React state shape

**Request/Response Format:**
- JSON for all API communication
- Consistent error response format
- Pagination for list endpoints (if lists grow large)
- ISO 8601 dates for consistency

**Authentication Pattern:**
- Session cookie automatically included in all requests
- No Authorization header or client-side token management
- Backend validates session on every protected endpoint
- 401 Unauthorized triggers logout flow in frontend

### Deployment Architecture

**Single-Server Pattern:**

```
[Browser]
    ↓ HTTPS
[FastAPI Server]
    ├── / → React static files (Vite build)
    ├── /api/* → FastAPI endpoints
    ├── /auth/* → Auth endpoints
    └── Session Store (Redis/In-memory)
    ↓
[PostgreSQL Database]
```

**Benefits of Single-Server:**
- Same origin = no CORS configuration
- Cookies work seamlessly (no credentials config)
- Simpler deployment (one server, one domain)
- Reduced infrastructure complexity
- Development proxy mirrors production architecture

**Production Requirements:**
- HTTPS required (for secure cookies)
- Environment variables for secrets (EntraID client secret, database URL, session secret)
- PostgreSQL database (managed service or containerized)
- Redis for session storage (recommended for production)
- Static file serving from FastAPI (mounting Vite build)

**Development Environment:**
- Vite dev server (port 5173) with HMR
- Vite proxy forwards `/api/*` to FastAPI (port 8000)
- No CORS issues - proxy makes requests appear same-origin
- Full hot module reload while API calls work seamlessly
- PostgreSQL (local or Docker)
- In-memory session storage for development

### Technology Stack Confirmation

**Frontend:**
- React 18+ with Vite
- Zustand for state management
- React Router for client-side routing
- TypeScript (recommended for type safety)
- Styling: Modern CSS or Tailwind CSS

**Backend:**
- FastAPI (Python 3.10+)
- Pydantic for validation
- SQLAlchemy ORM with Alembic migrations
- MSAL Python for EntraID OAuth2
- authlib for OAuth2 flow handling
- Session management with signed cookies

**Database:**
- PostgreSQL (production-grade relational)

**Infrastructure:**
- Single-server deployment
- Redis for production session storage
- Environment-based configuration

---

## User Experience Principles

Nomi's UX is **intentionally simple and functional** - designed to support architectural learning, not to be a design portfolio piece. The interface should be clean, predictable, and immediately understandable.

### Design Philosophy

**"Invisible UX"**

The UI should get out of the way and let the architecture shine:
- Clean, minimal interface with clear information hierarchy
- Standard UI patterns users already know (no novel interactions to learn)
- Functional over flashy - clarity over creativity
- Responsive state changes make Zustand patterns visible
- Forms and interactions demonstrate proper error handling

**The UX serves the architecture:**
- Loading states show async patterns working
- Error messages demonstrate proper error handling
- Instant updates prove state management efficiency
- Smooth navigation shows client-side routing
- Protected content demonstrates auth working

### Visual Personality

**Clean & Professional**
- Modern but not trendy (won't look dated in 2 years)
- Spacious layouts with breathing room
- Neutral color palette with purposeful accents
- Consistent typography hierarchy
- Subtle shadows and borders for depth

**Think:** Google Keep, Linear, or Notion - clean productivity tools, not creative playgrounds.

### Color Palette Approach

**Minimal color strategy:**
- **Primary:** Single accent color for CTAs and active states (blue, green, or purple)
- **Neutral grays:** Text, backgrounds, borders (light mode default)
- **Semantic colors:** Green (success), Red (error/delete), Yellow (warning)
- **No gradients or illustrations** - solid colors only

**Why minimal:**
- Faster development - no color system complexity
- Focus remains on functionality
- Professional appearance without design effort
- Easy to theme later if desired

### Key Interaction Patterns

**Standard Web Patterns - No Surprises:**

**Navigation:**
- Top nav bar or sidebar with clear sections (Tasks, Inspirations, Profile)
- Active state clearly indicated
- Logout button always accessible
- Client-side routing with no full page reloads

**Forms:**
- Standard form layouts with labels above inputs
- Inline validation with clear error messages
- Submit buttons disabled during processing
- Success feedback after successful creation/update
- Cancel/close options always available

**Lists (Tasks/Inspirations):**
- Card-based or simple list layout
- Hover states on interactive elements
- Click to edit or expand details
- Action buttons visible on hover or always visible (mobile)
- Empty states with helpful messaging ("No tasks yet - create your first one!")

**Modals/Dialogs:**
- Edit/create forms in modals or inline
- Confirmation dialogs for destructive actions (delete)
- Dismiss with X button, Cancel button, or ESC key
- Focus trapped within modal while open

**Loading States:**
- Skeleton screens or spinners during data fetching
- Disabled buttons during form submission
- Loading indicator for initial page load
- Optimistic updates where appropriate (add task → show immediately, update in background)

**Error Handling:**
- Toast notifications for success/error messages
- Inline form validation errors
- Graceful degradation if API call fails
- Retry options for failed operations

### Critical User Flows

**1. First-Time User Experience (Post-Auth)**

```
User completes EntraID auth → Redirected to app
↓
Lands on dashboard/home
↓
Sees welcome message + empty state
↓
Clear CTA: "Create your first task"
↓
Clicks CTA → Modal/form opens
↓
Fills form → Submits
↓
Success message + task appears in list
```

**Goal:** User creates first task within 30 seconds of landing.

**2. Daily Task Management Flow**

```
User arrives at app
↓
Sees list of tasks with clear status (todo/done)
↓
Scans list → Clicks task to view/edit OR marks done
↓
Done tasks move to completed section or fade
↓
Add new task via prominent button
↓
Filter to see only active tasks
```

**Goal:** Common operations (view, add, complete) require < 2 clicks.

**3. Inspiration → Task Conversion**

```
User captures inspiration
↓
Later browses inspirations list
↓
Finds one worth acting on
↓
Clicks "Convert to Task" or similar action
↓
Pre-filled task form opens with inspiration details
↓
User edits/confirms → Task created
↓
Inspiration marked as converted or archived
```

**Goal:** Demonstrate cross-entity operations smoothly.

**4. Session Expiry / Logout**

```
User's session expires OR clicks logout
↓
Immediately redirected to login/landing page
↓
No error state, no stuck pages
↓
Can log back in seamlessly
```

**Goal:** Auth state changes handled gracefully.

### Layout Structure

**Main Layout Components:**

```
┌────────────────────────────────────────┐
│  [Header: Logo | Nav | Profile/Logout] │
├────────────────────────────────────────┤
│                                        │
│  [Main Content Area]                   │
│                                        │
│  - Dashboard / Task List / Form        │
│  - Responsive grid or single column    │
│                                        │
│                                        │
└────────────────────────────────────────┘
```

**Responsive Behavior:**
- **Desktop (1024px+):** Sidebar nav + content area OR top nav + full width content
- **Tablet (768px-1023px):** Collapsible sidebar or top nav, full-width content
- **Mobile (320px-767px):** Top nav with hamburger menu, stacked content, full-width forms

### UI Component Patterns

**Reusable components to build:**
- Button (primary, secondary, danger variants)
- Input field (text, textarea)
- Card (for tasks/inspirations)
- Modal/Dialog
- Toast notification
- Loading spinner
- Empty state

**Why component focus:**
- Demonstrates React component patterns
- Promotes code reuse
- Consistent UX throughout app
- Easy to maintain and extend

### Typography & Spacing

**Simple system:**
- **Headings:** 1-2 font sizes (H1 for page titles, H2 for sections)
- **Body:** Single readable size (16px base)
- **Small:** For metadata/timestamps
- **Font:** System font stack (no custom fonts to load)

**Spacing scale:**
- Use consistent spacing units (4px, 8px, 16px, 24px, 32px)
- Generous padding in cards and forms
- Clear visual separation between sections

### What NOT to Include

**Avoid complexity that doesn't teach architecture:**
- ❌ Custom illustrations or iconography (use simple text or emoji)
- ❌ Animations beyond basic transitions
- ❌ Dark mode toggle (can be post-MVP if learning CSS variables)
- ❌ Advanced interactions (drag-and-drop, gesture controls)
- ❌ Custom design system or component library
- ❌ Sophisticated data visualization

**Keep it simple - the UX exists to make the architecture usable, not to win design awards.**

---

## Functional Requirements

These requirements transform the architectural learning goals into specific, implementable features. Each requirement is organized by capability area and includes clear acceptance criteria.

### 1. Authentication & Authorization

**Primary architectural learning goal: Master server-side OAuth2 with maximum security session management.**

#### FR-AUTH-001: EntraID OAuth2 Authentication
**Requirement:** Users must authenticate using Microsoft EntraID (Azure AD) via OAuth2 authorization code flow, with all token handling performed server-side.

**Acceptance Criteria:**
- User clicks "Sign in with Microsoft" button on landing page
- Backend redirects user to EntraID authorization URL with appropriate parameters (client_id, redirect_uri, scope, state)
- User authenticates with Microsoft (enters credentials, completes MFA if required)
- EntraID redirects to backend `/api/auth/callback` with authorization code
- Backend exchanges authorization code for access token and ID token using MSAL Python
- Backend validates ID token signature and claims
- Backend creates server-side session with user profile information
- Backend stores session in Redis (production) or in-memory (development)
- Backend sets HTTP-only, Secure, SameSite=Lax cookie with session ID
- Backend redirects user to frontend application home page
- Frontend calls `/api/auth/me` to retrieve user profile and authentication status
- User is now authenticated and can access protected resources

**Technical Details:**
- OAuth2 flow: Authorization Code Flow (not implicit or client credentials)
- Tokens never exposed to browser (stored server-side only)
- Session cookie: HTTP-only, Secure (HTTPS only), SameSite=Lax, signed
- MSAL Python library for token exchange
- authlib for OAuth2 flow management

#### FR-AUTH-002: Session-Based API Authentication
**Requirement:** All API requests to protected endpoints must validate session cookie to ensure user is authenticated.

**Acceptance Criteria:**
- Every request to `/api/tasks`, `/api/inspirations`, `/api/users/me` includes session cookie automatically
- Backend middleware validates session cookie signature
- Backend retrieves session from store (Redis/memory)
- If session valid: Request proceeds with user context available
- If session invalid/missing: Backend returns 401 Unauthorized
- Frontend intercepts 401 responses and redirects to login page

**Technical Details:**
- Session validation middleware on all protected routes
- User ID extracted from session and attached to request context
- No bearer tokens, no authorization headers - cookies only

#### FR-AUTH-003: Protected Routes (Frontend)
**Requirement:** Frontend must protect authenticated-only routes and redirect unauthenticated users to login.

**Acceptance Criteria:**
- Routes requiring authentication: `/tasks`, `/inspirations`, `/profile`
- Public routes: `/`, `/login`, `/auth/callback`
- Zustand auth store tracks authentication state (isAuthenticated, user profile)
- React Router guards check authentication state before rendering protected routes
- Unauthenticated users attempting to access protected routes are redirected to login
- After successful login, users are redirected to originally requested route (or home)

**Technical Details:**
- React Router with protected route wrapper component
- Auth state managed in Zustand store
- Initial app load calls `/api/auth/me` to check session status

#### FR-AUTH-004: User Profile Management
**Requirement:** System must retrieve and display authenticated user's profile information from EntraID.

**Acceptance Criteria:**
- User profile retrieved from ID token claims during authentication
- Profile includes: name, email, user ID (sub claim)
- Profile stored in session (server-side)
- Frontend can retrieve profile via `/api/auth/me` endpoint
- Profile displayed in UI (header, profile page)
- Profile information read-only (sourced from EntraID, not editable in app)

#### FR-AUTH-005: Logout Functionality
**Requirement:** Users must be able to log out, destroying their session and clearing authentication state.

**Acceptance Criteria:**
- Logout button accessible from all authenticated pages (header/nav)
- Clicking logout calls `/api/auth/logout` endpoint
- Backend destroys session in store (Redis/memory)
- Backend clears session cookie (sets empty value with immediate expiry)
- Frontend clears auth state in Zustand store
- User redirected to landing/login page
- Attempting to access protected routes after logout requires re-authentication

#### FR-AUTH-006: Session Expiry Handling
**Requirement:** Sessions must expire after period of inactivity, with graceful handling in UI.

**Acceptance Criteria:**
- Sessions expire after 24 hours of inactivity (configurable)
- API returns 401 Unauthorized when session expired
- Frontend intercepts 401 and redirects to login
- User sees message: "Your session has expired. Please log in again."
- After re-authentication, user can continue using app

### 2. Task Management

**Architectural learning goal: Demonstrate REST API design, CRUD operations, user-specific data isolation, and Zustand state management.**

#### FR-TASK-001: Create Task
**Requirement:** Authenticated users must be able to create new tasks with title, description, and default status.

**Acceptance Criteria:**
- User clicks "Add Task" button
- Task creation form appears (modal or inline)
- Form fields: Title (required, max 200 chars), Description (optional, max 2000 chars)
- Form validates: Title required, character limits enforced
- Submit button disabled while submitting
- On submit: POST to `/api/tasks` with task data
- Backend creates task with: user_id (from session), title, description, status="todo", timestamps
- Backend returns created task with generated ID
- Frontend adds task to Zustand store
- Task immediately appears in list (optimistic update)
- Success toast notification: "Task created"
- Form closes/resets

**Technical Details:**
- Database: Tasks table with columns (id, user_id, title, description, status, created_at, updated_at)
- User_id foreign key ensures tasks belong to specific user
- Backend validates user owns resource on all operations

#### FR-TASK-002: List Tasks
**Requirement:** Users must be able to view all their tasks in a list view.

**Acceptance Criteria:**
- On app load (authenticated): GET `/api/tasks` retrieves all user's tasks
- Backend filters tasks by user_id from session (user only sees own tasks)
- Tasks returned as JSON array with all fields
- Frontend stores tasks in Zustand store
- Tasks displayed in list/card view with: title, status, created date
- Empty state displayed if no tasks: "No tasks yet - create your first one!"
- List updates in real-time when tasks added/modified/deleted

**Technical Details:**
- Default sort: Most recently updated first
- Pagination not required for MVP (assume < 100 tasks)
- Backend query: `SELECT * FROM tasks WHERE user_id = ? ORDER BY updated_at DESC`

#### FR-TASK-003: Update Task
**Requirement:** Users must be able to edit task title, description, and status.

**Acceptance Criteria:**
- User clicks task to open edit view (modal or inline form)
- Form pre-populated with current values
- User can modify: title, description, status (todo/done)
- Validation same as create: title required, character limits
- On submit: PUT to `/api/tasks/{id}` with updated data
- Backend validates: user owns task (user_id matches session)
- Backend updates task, sets updated_at timestamp
- Backend returns updated task
- Frontend updates task in Zustand store
- UI reflects changes immediately
- Success toast: "Task updated"

#### FR-TASK-004: Update Task Status (Quick Action)
**Requirement:** Users must be able to quickly mark tasks as done/todo without opening full edit form.

**Acceptance Criteria:**
- Checkbox or toggle button visible on each task in list
- Clicking checkbox: PUT to `/api/tasks/{id}` with only status field
- Task status toggles between "todo" and "done"
- UI updates immediately (optimistic)
- Done tasks visually differentiated (strikethrough, faded, or moved to separate section)
- No confirmation required (quick action)

**Technical Details:**
- Partial update endpoint: Only updates status field
- Alternative: Use same update endpoint but frontend only sends changed fields

#### FR-TASK-005: Delete Task
**Requirement:** Users must be able to permanently delete tasks.

**Acceptance Criteria:**
- Delete button visible on task (trash icon)
- Clicking delete shows confirmation dialog: "Delete this task? This cannot be undone."
- User confirms or cancels
- On confirm: DELETE to `/api/tasks/{id}`
- Backend validates: user owns task
- Backend hard deletes task from database
- Frontend removes task from Zustand store
- Task disappears from list immediately
- Success toast: "Task deleted"

**Technical Details:**
- Hard delete (no soft delete for MVP)
- Cascade delete if task has relationships (future: comments, attachments)

### 3. Inspiration Management

**Architectural learning goal: Prove patterns work for multiple entity types, demonstrate cross-entity operations.**

#### FR-INSP-001: Create Inspiration
**Requirement:** Users must be able to capture inspirations with title and description.

**Acceptance Criteria:**
- User clicks "Add Inspiration" button
- Inspiration form appears (modal or inline)
- Form fields: Title (required, max 200 chars), Description (optional, max 2000 chars)
- Form validation: Title required, character limits enforced
- On submit: POST to `/api/inspirations` with data
- Backend creates inspiration with: user_id, title, description, captured_date (auto), timestamps
- Backend returns created inspiration
- Frontend adds to Zustand store
- Inspiration appears in list immediately
- Success toast: "Inspiration captured"

**Technical Details:**
- Database: Inspirations table (id, user_id, title, description, captured_date, created_at, updated_at)
- Similar structure to tasks but separate entity
- No status field (inspirations don't have todo/done states)

#### FR-INSP-002: List Inspirations
**Requirement:** Users must be able to view all their inspirations.

**Acceptance Criteria:**
- GET `/api/inspirations` retrieves all user's inspirations
- Backend filters by user_id from session
- Inspirations returned as JSON array
- Frontend stores in Zustand store (separate from tasks)
- Displayed in list/card view with: title, captured date
- Empty state: "No inspirations yet - capture your first idea!"
- List updates when inspirations added/modified/deleted

#### FR-INSP-003: Update Inspiration
**Requirement:** Users must be able to edit inspiration title and description.

**Acceptance Criteria:**
- User clicks inspiration to open edit view
- Form pre-populated with current values
- User modifies title and/or description
- On submit: PUT to `/api/inspirations/{id}`
- Backend validates user ownership
- Backend updates inspiration, sets updated_at
- Frontend updates Zustand store
- UI reflects changes immediately
- Success toast: "Inspiration updated"

#### FR-INSP-004: Delete Inspiration
**Requirement:** Users must be able to delete inspirations.

**Acceptance Criteria:**
- Delete button visible on inspiration
- Confirmation dialog: "Delete this inspiration?"
- On confirm: DELETE to `/api/inspirations/{id}`
- Backend validates ownership and deletes
- Frontend removes from store
- UI updates immediately
- Success toast: "Inspiration deleted"

#### FR-INSP-005: Convert Inspiration to Task
**Requirement:** Users must be able to convert an inspiration into a task, demonstrating cross-entity operations.

**Acceptance Criteria:**
- "Convert to Task" button visible on each inspiration
- Clicking button: POST to `/api/inspirations/{id}/convert`
- Backend creates new task with: title and description copied from inspiration
- Backend marks inspiration as converted (add converted_to_task_id field, or delete inspiration)
- Backend returns created task
- Frontend adds task to tasks store
- Frontend updates or removes inspiration from inspirations store
- User sees success message with link to new task
- Optional: Navigate to task view automatically

**Technical Details:**
- Decision needed: Delete inspiration after conversion OR mark as converted and keep
- Recommendation: Mark as converted (add converted_to_task_id field) for MVP - allows tracking inspiration source

### 4. Organization & Filtering

**Architectural learning goal: Demonstrate client-side state management for UI concerns, filtering patterns.**

#### FR-FILT-001: Filter by Entity Type
**Requirement:** Users must be able to switch between viewing tasks and inspirations.

**Acceptance Criteria:**
- Navigation or tabs for "Tasks" and "Inspirations"
- Clicking "Tasks" shows tasks list (filters out inspirations)
- Clicking "Inspirations" shows inspirations list (filters out tasks)
- Active view clearly indicated
- Client-side routing: `/tasks` and `/inspirations` routes
- Filter state managed in Zustand (or component state)

**Technical Details:**
- Separate pages/routes for tasks and inspirations (simplest approach)
- Alternative: Single page with filter toggle

#### FR-FILT-002: Filter Tasks by Status
**Requirement:** Users must be able to filter tasks to show only active (todo) or completed (done) tasks.

**Acceptance Criteria:**
- Filter options visible on tasks page: "All", "Active", "Completed"
- Clicking filter updates displayed tasks
- Filter applied client-side (no API call)
- Task count displayed for each filter option
- Filter state persisted while navigating within app (Zustand store)
- Default filter: "All" (shows both todo and done)

**Technical Details:**
- Client-side filtering in Zustand selector or component
- Example: `tasks.filter(task => filterState === 'active' ? task.status === 'todo' : filterState === 'completed' ? task.status === 'done' : true)`

#### FR-FILT-003: Sort Tasks and Inspirations
**Requirement:** Users must be able to sort items by date.

**Acceptance Criteria:**
- Sort options: "Newest first" (default), "Oldest first"
- Sort selector visible on list pages
- Clicking sort option re-orders list immediately
- Sort applied client-side
- Sort preference persisted in Zustand store

**Technical Details:**
- Sort by created_at or updated_at
- Client-side sort for MVP (backend sort if pagination added later)

### 5. User Profile

**Architectural learning goal: Display user context, demonstrate read-only data from identity provider.**

#### FR-PROF-001: View User Profile
**Requirement:** Users must be able to view their profile information.

**Acceptance Criteria:**
- Profile page accessible via navigation or user menu
- Profile displays: Name, Email, User ID (from EntraID)
- Profile information read-only (cannot edit - sourced from EntraID)
- Note displayed: "Profile information is managed by your Microsoft account"
- Logout button available on profile page

**Technical Details:**
- Data retrieved from `/api/auth/me` endpoint
- No database storage needed (profile in session)
- Optional: Store user in database for referential integrity (tasks.user_id references users.id)

### Summary of Functional Requirements

**Total Requirements:** 21 functional requirements across 5 capability areas

**Architectural Patterns Demonstrated:**
- ✅ Server-side OAuth2 authorization code flow (FR-AUTH-001)
- ✅ Session-based authentication with HTTP-only cookies (FR-AUTH-002)
- ✅ Protected routes (frontend and backend) (FR-AUTH-003)
- ✅ REST API design with proper methods (FR-TASK-*, FR-INSP-*)
- ✅ User-specific data isolation (all entity operations)
- ✅ CRUD operations for multiple entities (tasks, inspirations)
- ✅ Zustand state management (all entity lists and auth state)
- ✅ Cross-entity operations (FR-INSP-005 conversion)
- ✅ Client-side filtering and sorting (FR-FILT-*)
- ✅ Optimistic UI updates (FR-TASK-001, FR-TASK-004)
- ✅ Error handling and validation (all create/update operations)

**Every requirement serves the architectural learning goals - no feature bloat, just patterns you'll reuse.**

---

## Non-Functional Requirements

Only documenting NFRs that matter for THIS project. Learning-focused architecture projects need different constraints than production systems - we focus on patterns that demonstrate good practices without over-engineering.

### Performance Requirements

**Why performance matters for Nomi:**
- User experience should feel snappy (validates efficient patterns)
- Demonstrates understanding of performance implications
- Proves state management doesn't cause unnecessary re-renders
- Shows proper database query optimization

#### NFR-PERF-001: Page Load Performance
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

#### NFR-PERF-002: API Response Time
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

#### NFR-PERF-003: Frontend Rendering Efficiency
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

### Security Requirements

**Why security matters for Nomi:**
- **Primary learning goal:** Maximum-security authentication patterns
- Demonstrates defense-in-depth principles
- Proves understanding of OWASP top vulnerabilities
- Creates patterns safe for enterprise applications

#### NFR-SEC-001: Authentication Security (Maximum Security Pattern)
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

#### NFR-SEC-002: Data Access Control
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

#### NFR-SEC-003: Input Validation & Injection Prevention
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

#### NFR-SEC-004: Error Handling & Information Disclosure
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

#### NFR-SEC-005: Dependency Security
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

### Reliability Requirements

**Why reliability matters for Nomi:**
- Demonstrates proper error handling patterns
- Shows graceful degradation
- Learning goal: understand failure modes and recovery

#### NFR-REL-001: Error Handling & Recovery
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

#### NFR-REL-002: Database Integrity
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

### Maintainability Requirements

**Why maintainability matters for Nomi:**
- **Core learning goal:** Create reusable, understandable code
- Pattern library must be easy to adapt for future projects
- Code should be self-documenting through clarity

#### NFR-MAINT-001: Code Quality & Readability
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

#### NFR-MAINT-002: Project Structure & Organization
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

#### NFR-MAINT-003: Documentation
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

### What We're NOT Including (And Why)

**Scalability:** Not needed for learning project. Single-server deployment sufficient. No load balancing, no horizontal scaling, no microservices.

**High Availability:** Not needed. Downtime acceptable for learning project. No redundancy, no failover.

**Advanced Accessibility:** Basic Level A covered in UX section. AA/AAA not required for learning goals.

**Internationalization:** English only. No i18n complexity for learning project.

**Analytics/Monitoring:** Basic logging only. No APM, no metrics dashboard. Can add later if desired.

**Backup/Disaster Recovery:** Not required for learning project. Database backups good practice but not mandated.

### NFR Summary

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

## References

**Input Documents:**
- **Product Brief:** `/workspace/docs/product-brief-Nomi-2025-11-11.md`
- **Brainstorming Session:** `/workspace/docs/bmm-brainstorming-session-2025-11-10.md`
- **Workflow Status:** `/workspace/docs/bmm-workflow-status.yaml`

**Research Conducted:**
Product brief included web research on tech stack validation (FastAPI, Vite, React, Zustand industry adoption and best practices - 2024-2025).

---

## Next Steps

### Immediate: Epic & Story Breakdown (Required)

Requirements must be decomposed into implementable epics and bite-sized stories optimized for 200k context development agents.

**To proceed:**
1. Run `*create-epics-and-stories` workflow (PM agent, menu option 5)
2. This will transform the 21 functional requirements into epics organized by architectural pattern
3. Each epic will contain stories small enough for focused implementation

**Expected Epic Structure:**
- **Epic 1: Authentication & Session Management** (FR-AUTH-001 through FR-AUTH-006)
- **Epic 2: Task Management CRUD** (FR-TASK-001 through FR-TASK-005)
- **Epic 3: Inspiration Management** (FR-INSP-001 through FR-INSP-005)
- **Epic 4: Filtering & Organization** (FR-FILT-001 through FR-FILT-003)
- **Epic 5: User Profile & Settings** (FR-PROF-001)
- **Epic 6: Project Setup & Infrastructure** (Initial setup stories)
- **Epic 7: Documentation & Polish** (ADRs, README, deployment docs)

### Subsequent: Architecture Design (Required)

After epic breakdown, create technical architecture document:

**To proceed:**
1. Load architect agent
2. Run `*create-architecture` workflow
3. This will define technical implementation details, database schema, API contracts, deployment architecture

**Architecture will specify:**
- Database schema (tables, relationships, indexes)
- API endpoint specifications with request/response formats
- Authentication flow implementation details
- Frontend architecture (Zustand stores, component structure, routing)
- Deployment configuration and infrastructure
- Technology-specific implementation patterns

### Optional: UX Design

If desired, create detailed UX designs before implementation:

**To proceed:**
1. Load ux-designer agent
2. Run `*create-design` workflow
3. This will create wireframes, component specifications, and interaction details

**Note:** For Nomi's "invisible UX" approach, detailed UX design is optional. The UX principles section provides sufficient guidance for implementation.

---

## Appendix: The Product Magic Summary

**Nomi is the "Goldilocks" architectural template - just right complexity for learning and reuse.**

The magic of Nomi isn't in its features (task management is well-trodden ground) - it's in the **architectural clarity and reusability**:

- **Maximum-security authentication** patterns you can trust in enterprise applications
- **Clean BFF architecture** that demonstrates proper frontend/backend separation
- **Zustand state management** patterns proven across multiple entity types
- **Single-server deployment** that eliminates common web app deployment headaches
- **Well-documented decisions** captured as you build, not reconstructed later

Six months from now, when you start a new React + Python project, Nomi will be the reference implementation you open first - the one that answers "how do I structure this?" with confidence, not guesswork.

**That's the magic: A codebase that teaches, not just works.**

---

_This PRD was created through collaborative discovery between Justin and the PM agent, following the BMad Method for greenfield software projects._

_Document captures requirements adapted specifically for an architectural learning project - balancing real-world patterns with educational clarity._

