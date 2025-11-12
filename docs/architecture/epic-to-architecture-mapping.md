# Epic to Architecture Mapping

| Epic | Feature Slice | Database Tables | API Endpoints | Frontend Pages/Stores |
| ---- | ------------- | --------------- | ------------- | --------------------- |
| **Epic 1: Project Foundation & Infrastructure** | `main.py`, `vite.config.ts`, `core/database.py`, `alembic/` | `users` (initial schema) | `/health` | Base layout, routing setup |
| **Epic 2: Authentication & Session Management** ⭐ | `features/auth/` (endpoints.py, schemas.py, service.py, dependencies.py), `core/security.py`, `core/session_store.py`, `stores/authStore.ts` | `users` (EntraID profile) | `/api/auth/login`, `/api/auth/callback`, `/api/auth/me`, `/api/auth/logout` | `Login.tsx`, `authStore.ts`, Protected routes |
| **Epic 3: Task Management** | `features/tasks/` (endpoints.py, model.py, schemas.py, service.py), `stores/tasksStore.ts`, `pages/Tasks.tsx` | `tasks` (user_id, title, description, status, timestamps) | `/api/tasks` (GET, POST), `/api/tasks/{id}` (GET, PUT, DELETE) | `Tasks.tsx`, `tasksStore.ts`, `components/tasks/` |
| **Epic 4: Inspiration Management** | `features/inspirations/` (endpoints.py, model.py, schemas.py, service.py), `stores/inspirationsStore.ts`, `pages/Inspirations.tsx` | `inspirations` (user_id, title, description, captured_date, timestamps) | `/api/inspirations` (GET, POST), `/api/inspirations/{id}` (GET, PUT, DELETE), `/api/inspirations/{id}/convert` (POST) | `Inspirations.tsx`, `inspirationsStore.ts`, `components/inspirations/` |
| **Epic 5: Organization & Filtering** | Zustand selectors in `tasksStore.ts` and `inspirationsStore.ts`, filter components | No new tables | No new endpoints (client-side filtering) | Filter UI components, sort selectors in stores |
| **Epic 6: User Profile & Settings** | `features/users/` (endpoints.py, model.py, schemas.py) | `users` (read-only EntraID data) | `/api/users/me` (GET) | `Profile.tsx`, profile components |
| **Epic 7: Deployment & Documentation** | `main.py` (static file serving), Docker config, deployment scripts | No new tables | No new endpoints | Production build (`npm run build`) |

## Key Architectural Boundaries

**Vertical Slice Architecture Benefits:**
- Each feature is self-contained with all its concerns in one place
- Changes to a feature don't ripple across the codebase
- Easy to understand: everything for tasks lives in `features/tasks/`
- High cohesion within slices, low coupling between slices

**Epic 2 (Authentication) is foundational** - all other epics depend on:
- Session validation (`core/security.py`)
- User context provider (`features/auth/dependencies.py::get_current_user`)
- Protected route wrapper (`components/layout/ProtectedRoute.tsx`)

**Epics 3 & 4 (Tasks & Inspirations) are independent vertical slices:**
- Each feature slice contains: endpoints.py → model.py → schemas.py → service.py
- User data isolation enforced at service layer (all queries filter by `user_id`)
- Optimistic UI updates in Zustand stores
- No shared business logic between slices (intentionally duplicated if needed)

**Epic 4 (Inspirations) demonstrates cross-slice communication:**
- `inspirations/service.py` imports `tasks/service.py` for conversion feature
- This is acceptable - slices can depend on other slices for specific use cases

**Epic 5 (Filtering) is pure frontend** - demonstrates client-side state management without backend changes.
