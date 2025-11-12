# Product Scope

Scope is driven by **architectural learning value** - features exist to demonstrate patterns, not to build a competitive product. The MVP contains exactly what's needed to prove all key architectural patterns without overwhelming complexity.

## MVP - Minimum Viable Product

**Core principle:** Just enough features to demonstrate all critical architectural patterns in a realistic context.

### 1. Authentication & Authorization (EntraID + Session-Based)
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

### 2. Task Management (CRUD Operations)
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

### 3. Inspiration Capture (Secondary Entity)
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

### 4. Basic Organization & Filtering
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

## MVP Feature Selection Criteria

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

## Growth Features (Post-MVP)

**When MVP is complete and patterns are proven**, these features could be added to deepen specific pattern knowledge:

### Enhanced Organization
- Tags/categories for tasks and inspirations
- Search functionality (full-text search patterns)
- Bulk operations (select multiple, batch actions)

**Learning value:** Advanced state management, search patterns, batch operation handling.

### Collaboration Features (If exploring multi-user patterns)
- Share tasks/inspirations with other users
- Team workspaces
- Real-time updates (WebSocket patterns)

**Learning value:** Multi-tenant data isolation, real-time communication, WebSocket integration.

### Rich Content
- Markdown support for descriptions
- File attachments
- Image uploads

**Learning value:** File upload patterns, storage integration (S3), content sanitization.

### Enhanced UX
- Drag-and-drop reordering
- Keyboard shortcuts
- Dark mode toggle
- Mobile-responsive improvements

**Learning value:** Advanced UI patterns, responsive design, accessibility.

## Vision (Future Exploration)

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

## Scope Rationale

The MVP feature set achieves the core goal: **a reusable architectural template that's not trivial but not overwhelming.**

- **Not trivial:** Real auth, multiple entities, state management, deployment - all production patterns
- **Not overwhelming:** 4 focused feature areas, familiar domain, no complex algorithms or infrastructure
- **Just right:** Proves all key patterns, remains understandable, stays manageable

Every feature in MVP demonstrates a pattern you'll reuse. Every feature excluded simplifies focus without losing architectural value.

---
