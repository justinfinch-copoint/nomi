# Architecture

## Executive Summary

Nomi implements a **"Goldilocks" architectural template** - proving enterprise-grade patterns at a manageable scale. The architecture prioritizes **maximum-security authentication** (server-side OAuth2, zero token exposure), **single-server simplicity** (no CORS complexity), **vertical slice organization** (feature-first structure), **REPR pattern** (Request-Endpoint-Response), and **clean separation of concerns** (BFF pattern, Zustand state management).

This is not a typical todo app - it's an **architectural reference implementation** demonstrating:
- **Vertical Slice Architecture**: Backend organized by features (`features/tasks/`, `features/auth/`) - high cohesion, low coupling
- **REPR Pattern**: Each endpoint is explicit Request → Endpoint → Response with dedicated Pydantic schemas
- **Maximum Security**: Server-side OAuth2 with HTTP-only session cookies (complete XSS immunity)
- **Simple Deployment**: React + FastAPI single-server pattern (same origin, no CORS)
- **Modern Stack**: Zustand, React Router, Tailwind 4.0, SQLAlchemy 2.0 async, Pydantic validation
- **Production-Ready**: Patterns that scale without over-engineering

The architecture makes bold, opinionated choices to create patterns worth copying - not generic boilerplate.

## Project Initialization

**First Implementation Story** should execute these commands:

### Frontend Setup
```bash
# Create React + TypeScript + Vite project
npm create vite@latest nomi-frontend -- --template react-ts
cd nomi-frontend

# Install core dependencies
npm install react-router-dom zustand

# Install and configure Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Install development tooling
npm install
```

### Backend Setup
```bash
# Create backend directory
mkdir nomi-backend
cd nomi-backend

# Initialize Python project (using pip or poetry)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install FastAPI and core dependencies
pip install "fastapi[standard]>=0.121.0" "sqlalchemy[asyncio]>=2.0.44" "alembic>=1.13.0" "msal>=1.34.0"
pip install "psycopg[binary]>=3.1.0" "python-dotenv>=1.0.0" "pydantic>=2.0.0"
```

This establishes the base architecture - all decisions below build on this foundation.

## Decision Summary

| Category | Decision | Version | Affects Epics | Rationale |
| -------- | -------- | ------- | ------------- | --------- |
| **Authentication** | Server-side OAuth2 (EntraID + MSAL Python) | MSAL 1.34.0 | All epics | Maximum security: zero token exposure, HTTP-only cookies, complete XSS immunity |
| **Session Storage** | Redis (prod) / In-memory (dev) | Redis 7.x | All authenticated epics | Fast session lookup, production-grade scalability, simple dev workflow |
| **Backend Framework** | FastAPI | 0.121.1 | All backend epics | Modern async Python, auto-generated OpenAPI docs, excellent performance |
| **Database** | PostgreSQL | 16.x or 17.x | All epics with data | Production-grade relational DB, excellent JSON support, rock-solid reliability |
| **ORM** | SQLAlchemy (async) | 2.0.44 | All data epics | Modern async support, type-safe queries, mature ecosystem |
| **Migrations** | Alembic | 1.13.x | All schema changes | SQLAlchemy-native migrations, version control for schema |
| **API Pattern** | REST (BFF style) | N/A | All client-facing epics | Simple, well-understood, frontend-shaped endpoints |
| **Frontend Framework** | React | 19.2.0 | All frontend epics | Modern hooks, concurrent features, ecosystem maturity |
| **Build Tool** | Vite | 7.1.9 | All frontend epics | Lightning-fast HMR, excellent DX, modern module system |
| **Language (Frontend)** | TypeScript | 5.9.x | All frontend epics | Type safety, better DX, catches errors at compile time |
| **State Management** | Zustand | 5.0.8 | All frontend epics | Minimal boilerplate, excellent performance, simple mental model |
| **Routing** | React Router | 7.9.x | All navigation | Client-side routing, protected routes, type-safe navigation |
| **Styling** | Tailwind CSS | 4.0 | All frontend epics | Utility-first, fast builds, consistent design system |
| **Deployment Pattern** | Single-server (FastAPI serves all) | N/A | All epics | No CORS, simplified deployment, production-viable |
| **Python Version** | Python 3.10+ | 3.10+ | All backend epics | Modern async syntax, type hints, FastAPI requirement |

## Project Structure

```
nomi/
├── nomi-frontend/                # React + Vite frontend
│   ├── public/                   # Static assets (favicon, etc.)
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   │   ├── common/           # Shared components (Button, Input, Modal, etc.)
│   │   │   ├── tasks/            # Task-specific components (TaskCard, TaskForm, etc.)
│   │   │   ├── inspirations/     # Inspiration components
│   │   │   └── layout/           # Layout components (Header, Nav, etc.)
│   │   ├── pages/                # Route components
│   │   │   ├── Home.tsx          # Landing page
│   │   │   ├── Login.tsx         # Login/auth page
│   │   │   ├── Tasks.tsx         # Tasks list page
│   │   │   ├── Inspirations.tsx  # Inspirations list page
│   │   │   └── Profile.tsx       # User profile page
│   │   ├── stores/               # Zustand state stores
│   │   │   ├── authStore.ts      # Authentication state
│   │   │   ├── tasksStore.ts     # Tasks state & actions
│   │   │   └── inspirationsStore.ts  # Inspirations state & actions
│   │   ├── services/             # API client functions
│   │   │   ├── api.ts            # Base API client (fetch wrapper)
│   │   │   ├── authService.ts    # Auth API calls
│   │   │   ├── tasksService.ts   # Tasks CRUD API calls
│   │   │   └── inspirationsService.ts  # Inspirations CRUD API calls
│   │   ├── utils/                # Helper functions
│   │   │   ├── formatDate.ts     # Date formatting utilities
│   │   │   └── validators.ts     # Form validation helpers
│   │   ├── types/                # TypeScript type definitions
│   │   │   ├── auth.ts           # Auth-related types
│   │   │   ├── task.ts           # Task entity types
│   │   │   └── inspiration.ts    # Inspiration entity types
│   │   ├── App.tsx               # Root component with routing
│   │   ├── main.tsx              # Entry point
│   │   └── index.css             # Tailwind imports & global styles
│   ├── .env.example              # Environment variables template
│   ├── .eslintrc.cjs             # ESLint configuration
│   ├── tailwind.config.js        # Tailwind configuration
│   ├── tsconfig.json             # TypeScript configuration
│   ├── vite.config.ts            # Vite configuration (with proxy)
│   └── package.json              # Frontend dependencies
│
├── nomi-backend/                 # FastAPI backend (Vertical Slice + REPR Architecture)
│   ├── app/
│   │   ├── features/             # Feature slices (vertical organization)
│   │   │   ├── auth/             # Authentication feature slice
│   │   │   │   ├── __init__.py
│   │   │   │   ├── login.py      # REPR: POST /api/auth/login endpoint
│   │   │   │   ├── callback.py   # REPR: GET /api/auth/callback endpoint
│   │   │   │   ├── me.py         # REPR: GET /api/auth/me endpoint
│   │   │   │   ├── logout.py     # REPR: POST /api/auth/logout endpoint
│   │   │   │   ├── service.py    # OAuth2 flow, session management logic
│   │   │   │   └── dependencies.py  # Auth-specific dependencies (get_current_user)
│   │   │   ├── tasks/            # Task management feature slice
│   │   │   │   ├── __init__.py
│   │   │   │   ├── create_task.py       # REPR: POST /api/tasks (Request, Endpoint, Response)
│   │   │   │   ├── list_tasks.py        # REPR: GET /api/tasks (Endpoint, Response)
│   │   │   │   ├── get_task.py          # REPR: GET /api/tasks/{id} (Endpoint, Response)
│   │   │   │   ├── update_task.py       # REPR: PUT /api/tasks/{id} (Request, Endpoint, Response)
│   │   │   │   ├── delete_task.py       # REPR: DELETE /api/tasks/{id} (Endpoint only)
│   │   │   │   ├── model.py      # Task SQLAlchemy model (shared across endpoints)
│   │   │   │   └── service.py    # Task business logic (shared across endpoints)
│   │   │   ├── inspirations/     # Inspiration management feature slice
│   │   │   │   ├── __init__.py
│   │   │   │   ├── create_inspiration.py      # REPR: POST /api/inspirations
│   │   │   │   ├── list_inspirations.py       # REPR: GET /api/inspirations
│   │   │   │   ├── get_inspiration.py         # REPR: GET /api/inspirations/{id}
│   │   │   │   ├── update_inspiration.py      # REPR: PUT /api/inspirations/{id}
│   │   │   │   ├── delete_inspiration.py      # REPR: DELETE /api/inspirations/{id}
│   │   │   │   ├── convert_to_task.py         # REPR: POST /api/inspirations/{id}/convert
│   │   │   │   ├── model.py      # Inspiration SQLAlchemy model (shared)
│   │   │   │   └── service.py    # Inspiration business logic (shared)
│   │   │   └── users/            # User profile feature slice
│   │   │       ├── __init__.py
│   │   │       ├── get_profile.py  # REPR: GET /api/users/me
│   │   │       └── model.py      # User SQLAlchemy model
│   │   ├── core/                 # Shared infrastructure (cross-cutting concerns)
│   │   │   ├── config.py         # Settings (environment variables)
│   │   │   ├── security.py       # Session validation, cookie signing
│   │   │   ├── database.py       # Database connection, session factory
│   │   │   └── session_store.py  # Session manager (Redis/in-memory)
│   │   └── main.py               # FastAPI app initialization, feature routers, static files
│   ├── alembic/                  # Database migrations
│   │   ├── versions/             # Migration scripts
│   │   └── env.py                # Alembic configuration
│   ├── tests/                    # Backend tests (mirroring feature structure)
│   │   ├── features/
│   │   │   ├── test_auth.py      # Auth feature tests
│   │   │   ├── test_tasks.py     # Tasks feature tests
│   │   │   └── test_inspirations.py  # Inspirations feature tests
│   │   └── conftest.py           # Shared test fixtures
│   ├── .env.example              # Environment variables template
│   ├── alembic.ini               # Alembic configuration
│   ├── requirements.txt          # Python dependencies
│   └── pyproject.toml            # Python project metadata (optional)
│
├── docs/                         # Documentation
│   ├── PRD.md                    # Product Requirements Document
│   ├── epics.md                  # Epic & story breakdown
│   ├── architecture.md           # This file
│   ├── SETUP.md                  # Developer setup guide
│   └── DEPLOYMENT.md             # Deployment instructions
│
├── .gitignore                    # Git ignore patterns
└── README.md                     # Project overview & quick start
```

## Epic to Architecture Mapping

| Epic | Feature Slice | Database Tables | API Endpoints | Frontend Pages/Stores |
| ---- | ------------- | --------------- | ------------- | --------------------- |
| **Epic 1: Project Foundation & Infrastructure** | `main.py`, `vite.config.ts`, `core/database.py`, `alembic/` | `users` (initial schema) | `/health` | Base layout, routing setup |
| **Epic 2: Authentication & Session Management** ⭐ | `features/auth/` (endpoints.py, schemas.py, service.py, dependencies.py), `core/security.py`, `core/session_store.py`, `stores/authStore.ts` | `users` (EntraID profile) | `/api/auth/login`, `/api/auth/callback`, `/api/auth/me`, `/api/auth/logout` | `Login.tsx`, `authStore.ts`, Protected routes |
| **Epic 3: Task Management** | `features/tasks/` (endpoints.py, model.py, schemas.py, service.py), `stores/tasksStore.ts`, `pages/Tasks.tsx` | `tasks` (user_id, title, description, status, timestamps) | `/api/tasks` (GET, POST), `/api/tasks/{id}` (GET, PUT, DELETE) | `Tasks.tsx`, `tasksStore.ts`, `components/tasks/` |
| **Epic 4: Inspiration Management** | `features/inspirations/` (endpoints.py, model.py, schemas.py, service.py), `stores/inspirationsStore.ts`, `pages/Inspirations.tsx` | `inspirations` (user_id, title, description, captured_date, timestamps) | `/api/inspirations` (GET, POST), `/api/inspirations/{id}` (GET, PUT, DELETE), `/api/inspirations/{id}/convert` (POST) | `Inspirations.tsx`, `inspirationsStore.ts`, `components/inspirations/` |
| **Epic 5: Organization & Filtering** | Zustand selectors in `tasksStore.ts` and `inspirationsStore.ts`, filter components | No new tables | No new endpoints (client-side filtering) | Filter UI components, sort selectors in stores |
| **Epic 6: User Profile & Settings** | `features/users/` (endpoints.py, model.py, schemas.py) | `users` (read-only EntraID data) | `/api/users/me` (GET) | `Profile.tsx`, profile components |
| **Epic 7: Deployment & Documentation** | `main.py` (static file serving), Docker config, deployment scripts | No new tables | No new endpoints | Production build (`npm run build`) |

### Key Architectural Boundaries

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

## Technology Stack Details

### Backend Stack

**FastAPI 0.121.1**
- Modern async Python web framework
- Automatic OpenAPI/Swagger documentation at `/docs`
- Native Pydantic validation
- Excellent performance (comparable to Node.js/Go)

**SQLAlchemy 2.0.44 (Async)**
- Use `AsyncSession` for all database operations
- Type-safe queries with modern ORM patterns
- Declarative models with proper relationships

**PostgreSQL 16.x/17.x**
- Primary database for all persistent data
- Use `psycopg` (v3) async driver
- UUID primary keys for all tables
- Indexed foreign keys for performance

**MSAL Python 1.34.0**
- Microsoft Authentication Library for OAuth2
- Server-side token exchange only
- Validate ID tokens with JWK

S
**Redis 7.x** (Production) / **In-Memory Dict** (Development)
- Session storage with 24-hour TTL
- Fast session lookup by session ID
- Simple key-value structure

### Frontend Stack

**React 19.2.0 + TypeScript 5.9.x**
- Functional components with hooks
- Type-safe props and state
- No class components

**Vite 7.1.9**
- Lightning-fast HMR in development
- Optimized production builds
- Proxy configuration for API requests during development

**Zustand 5.0.8**
- Minimal state management library
- No boilerplate (no actions/reducers/dispatch)
- Excellent TypeScript support
- Separate stores per concern (auth, tasks, inspirations)

**React Router 7.9.x**
- Client-side routing
- Protected route wrappers
- Type-safe navigation

**Tailwind CSS 4.0**
- Utility-first CSS framework
- Custom configuration for Nomi design system
- Responsive design utilities

### Integration Points

**EntraID (Azure AD)**
- OAuth2 authorization endpoint
- Token endpoint for code exchange
- JWKS endpoint for ID token validation
- User profile from ID token claims

**Vite Dev Proxy** (Development Only)
- Forwards `/api/*` requests to `localhost:8000`
- Eliminates CORS during development
- Mirrors production same-origin architecture

**FastAPI Static Files** (Production)
- Mounts React build at `/`
- Serves API at `/api/*`
- Fallback to `index.html` for SPA routing

## Implementation Patterns

**These patterns ensure consistent implementation across all AI agents. Every agent MUST follow these conventions to prevent conflicts.**

### NAMING PATTERNS

#### REST API Endpoints
```
CONVENTION: Plural nouns, lowercase, hyphen-separated for multi-word
✅ /api/tasks
✅ /api/inspirations
✅ /api/auth/callback
❌ /api/task (singular)
❌ /api/Tasks (capitalized)
❌ /api/task_list (underscore)
```

#### Database Tables & Columns
```
CONVENTION: Snake_case for tables and columns
✅ tasks, inspirations, users
✅ user_id, created_at, entraid_user_id
❌ Users, Tasks (PascalCase)
❌ userId, createdAt (camelCase)
```

#### Python Files & Classes
```
CONVENTION:
- Files: snake_case
- Classes: PascalCase
- Functions/variables: snake_case

✅ task.py → class Task
✅ auth_service.py → class AuthService → def create_session()
❌ TaskModel.py, task-service.py
```

#### TypeScript/React Files & Components
```
CONVENTION:
- Components: PascalCase files → PascalCase exports
- Services/utilities: camelCase files → camelCase exports
- Types: PascalCase

✅ TaskCard.tsx → export const TaskCard
✅ tasksService.ts → export const createTask
✅ task.ts → export type Task
❌ task-card.tsx, TasksService.ts
```

### STRUCTURE PATTERNS

#### Backend Feature Slice Organization (Vertical Slice + REPR Pattern)
```python
# VERTICAL SLICE: Everything for a feature lives together
# REPR PATTERN: Each endpoint is a separate file with its own Request/Response

# app/features/tasks/ contains ALL task-related code
# ONE FILE PER ENDPOINT (true REPR pattern)

# =========================================
# app/features/tasks/create_task.py
# =========================================
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from app.features.auth.dependencies import get_current_user
from app.features.users.model import User
from .service import TaskService

# Request schema for THIS endpoint only
class CreateTaskRequest(BaseModel):
    """REPR Request: Create task"""
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=2000)

# Response schema for THIS endpoint only
class CreateTaskResponse(BaseModel):
    """REPR Response: Created task"""
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# REPR Endpoint: Create Task
@router.post("/", response_model=CreateTaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: CreateTaskRequest,
    current_user: User = Depends(get_current_user)
):
    """
    REPR: Create a new task
    Request: CreateTaskRequest (title, description)
    Response: CreateTaskResponse (full task object)
    """
    task = await TaskService.create_task(current_user.id, request)
    return task

# =========================================
# app/features/tasks/list_tasks.py
# =========================================
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from app.features.auth.dependencies import get_current_user
from app.features.users.model import User
from .service import TaskService

# Response schema (individual task)
class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Response schema for THIS endpoint
class ListTasksResponse(BaseModel):
    """REPR Response: List of tasks"""
    tasks: list[TaskResponse]

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# REPR Endpoint: List Tasks
@router.get("/", response_model=ListTasksResponse, status_code=status.HTTP_200_OK)
async def list_tasks(current_user: User = Depends(get_current_user)):
    """
    REPR: List all tasks for authenticated user
    Request: None (user from session)
    Response: ListTasksResponse
    """
    tasks = await TaskService.get_user_tasks(current_user.id)
    return ListTasksResponse(tasks=tasks)

# =========================================
# app/features/tasks/update_task.py
# =========================================
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from app.features.auth.dependencies import get_current_user
from app.features.users.model import User
from .service import TaskService

# Request schema for THIS endpoint
class UpdateTaskRequest(BaseModel):
    """REPR Request: Update task"""
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=2000)
    status: str | None = Field(None, pattern="^(todo|done)$")

# Response schema for THIS endpoint
class UpdateTaskResponse(BaseModel):
    """REPR Response: Updated task"""
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# REPR Endpoint: Update Task
@router.put("/{task_id}", response_model=UpdateTaskResponse, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: str,
    request: UpdateTaskRequest,
    current_user: User = Depends(get_current_user)
):
    """
    REPR: Update existing task
    Request: task_id + UpdateTaskRequest
    Response: UpdateTaskResponse
    """
    task = await TaskService.update_task(task_id, current_user.id, request)
    return task

# =========================================
# app/features/tasks/delete_task.py
# =========================================
from fastapi import APIRouter, Depends, status
from app.features.auth.dependencies import get_current_user
from app.features.users.model import User
from .service import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# REPR Endpoint: Delete Task (no request/response schemas needed)
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    REPR: Delete task by ID
    Request: task_id (path parameter)
    Response: 204 No Content
    """
    await TaskService.delete_task(task_id, current_user.id)

# =========================================
# app/features/tasks/model.py (SHARED across endpoints)
# =========================================
from sqlalchemy import Column, String, UUID, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(2000))
    status = Column(String(20), nullable=False, default="todo")
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

# =========================================
# app/features/tasks/service.py (SHARED business logic)
# =========================================
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .model import Task

class TaskService:
    @staticmethod
    async def get_user_tasks(user_id: UUID, db: AsyncSession):
        result = await db.execute(
            select(Task).where(Task.user_id == user_id).order_by(Task.updated_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def create_task(user_id: UUID, request, db: AsyncSession):
        task = Task(
            user_id=user_id,
            title=request.title,
            description=request.description,
            status="todo"
        )
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    # ... other service methods

# =========================================
# app/main.py - Collecting all endpoint routers
# =========================================
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Import individual endpoint routers (one per endpoint file)
# Auth endpoints
from app.features.auth.login import router as auth_login_router
from app.features.auth.callback import router as auth_callback_router
from app.features.auth.me import router as auth_me_router
from app.features.auth.logout import router as auth_logout_router

# Task endpoints
from app.features.tasks.create_task import router as task_create_router
from app.features.tasks.list_tasks import router as task_list_router
from app.features.tasks.get_task import router as task_get_router
from app.features.tasks.update_task import router as task_update_router
from app.features.tasks.delete_task import router as task_delete_router

# Inspiration endpoints
from app.features.inspirations.create_inspiration import router as inspiration_create_router
from app.features.inspirations.list_inspirations import router as inspiration_list_router
# ... other inspiration routers

app = FastAPI(title="Nomi API", version="1.0.0")

# Include all endpoint routers
app.include_router(auth_login_router)
app.include_router(auth_callback_router)
app.include_router(auth_me_router)
app.include_router(auth_logout_router)

app.include_router(task_create_router)
app.include_router(task_list_router)
app.include_router(task_get_router)
app.include_router(task_update_router)
app.include_router(task_delete_router)

app.include_router(inspiration_create_router)
app.include_router(inspiration_list_router)
# ... other inspiration routers

# Serve React static files (production)
app.mount("/", StaticFiles(directory="../nomi-frontend/dist", html=True), name="static")
```

**Key Points:**
- ✅ Each endpoint = One file
- ✅ Each file contains its own Request/Response schemas
- ✅ model.py and service.py are SHARED across endpoints
- ✅ main.py imports and includes all individual routers

#### Frontend Component Organization
```typescript
// Pages in pages/ → route components
// Reusable UI in components/ → feature-organized

// pages/Tasks.tsx
export const Tasks = () => {
  const { tasks, fetchTasks } = useTasksStore();
  // Page-level logic
};

// components/tasks/TaskCard.tsx
export const TaskCard = ({ task }: { task: Task }) => {
  // Reusable task display
};
```

#### Test File Organization
```
Backend tests (mirroring feature structure):
tests/
  features/
    test_auth.py          # Tests for features/auth/
    test_tasks.py         # Tests for features/tasks/
    test_inspirations.py  # Tests for features/inspirations/
  conftest.py             # Shared fixtures

Frontend tests (if added):
src/
  components/
    tasks/
      TaskCard.tsx
      TaskCard.test.tsx
```

#### Vertical Slice Principles
```python
# PRINCIPLE 1: Feature independence
# Each feature slice is self-contained
✅ features/tasks/ has its own model, schemas, service, endpoints
✅ features/inspirations/ has its own model, schemas, service, endpoints

# PRINCIPLE 2: Shared infrastructure in core/
# Cross-cutting concerns live in core/
✅ core/database.py - Database connection
✅ core/security.py - Session validation
✅ core/config.py - Settings
❌ core/crud.py - NO generic CRUD (belongs in feature slices)

# PRINCIPLE 3: Allow intentional duplication
# Code duplication between slices is acceptable
✅ tasks/service.py and inspirations/service.py may have similar CRUD patterns
❌ Don't create shared base classes to eliminate duplication
Rationale: Slices evolve independently - premature abstraction creates coupling

# PRINCIPLE 4: Cross-slice dependencies when needed
# Slices can import from other slices for specific use cases
✅ inspirations/service.py can import tasks/service.py for convert_to_task()
⚠️ Keep these minimal - they create coupling
```

#### REPR Pattern Principles (Request-Endpoint-Response)

```python
# REPR PATTERN: Each endpoint follows Request → Endpoint → Response

# PRINCIPLE 1: Explicit Request Schemas
# Every endpoint that accepts input has a dedicated Pydantic request model
✅ TaskCreateRequest - for POST /api/tasks
✅ TaskUpdateRequest - for PUT /api/tasks/{id}
❌ Generic dict or untyped parameters

# PRINCIPLE 2: Explicit Response Schemas
# Every endpoint has a dedicated Pydantic response model
✅ TaskResponse - for single task responses
✅ TaskListResponse - for list responses
❌ Returning raw ORM models without schema

# PRINCIPLE 3: Single Responsibility per Endpoint
# Each endpoint function does ONE thing
✅ create_task() - only creates tasks
✅ update_task() - only updates tasks
❌ update_or_create_task() - don't combine operations

# PRINCIPLE 4: Clear API Contracts
# Request/Response schemas serve as API documentation
✅ Pydantic Field() with descriptions
✅ json_schema_extra with examples
✅ Validation rules (min_length, max_length, pattern)
❌ Undocumented magic behavior

# PRINCIPLE 5: Status Code Clarity
# Every endpoint specifies its status code explicitly
✅ @router.post(..., status_code=status.HTTP_201_CREATED)
✅ @router.get(..., status_code=status.HTTP_200_OK)
✅ @router.delete(..., status_code=status.HTTP_204_NO_CONTENT)
❌ Relying on FastAPI defaults without being explicit
```

**REPR Benefits:**
1. **Clear Contracts**: Request/Response schemas document the API
2. **Type Safety**: Pydantic validates all inputs/outputs
3. **Auto-Generated Docs**: OpenAPI/Swagger documentation is complete
4. **Easy Testing**: Mock requests/responses with known schemas
5. **Single Responsibility**: Each endpoint has one job
6. **No Surprises**: Explicit schemas prevent unexpected behavior

**REPR File & Naming Convention:**
```python
# FILE NAMES: Descriptive, one per endpoint
create_task.py       # Contains: CreateTaskRequest, CreateTaskResponse
list_tasks.py        # Contains: ListTasksResponse (no request)
get_task.py          # Contains: GetTaskResponse
update_task.py       # Contains: UpdateTaskRequest, UpdateTaskResponse
delete_task.py       # Endpoint only (no schemas needed)

# SCHEMA NAMES: Match the endpoint operation
# In create_task.py:
class CreateTaskRequest(BaseModel):   # Request for THIS endpoint
    ...
class CreateTaskResponse(BaseModel):  # Response for THIS endpoint
    ...

# In list_tasks.py:
class TaskResponse(BaseModel):        # Individual task (reused in list)
    ...
class ListTasksResponse(BaseModel):   # Response for THIS endpoint
    tasks: list[TaskResponse]

# In update_task.py:
class UpdateTaskRequest(BaseModel):   # Request for THIS endpoint
    ...
class UpdateTaskResponse(BaseModel):  # Response for THIS endpoint
    ...

# PRINCIPLE: Each endpoint file is self-contained
# - Contains only schemas it needs
# - Small schema duplication is OK (e.g., TaskResponse repeated)
# - Makes endpoint easy to understand in isolation

# Rationale: Allows adding metadata later without breaking changes
# Future: tasks: list[TaskResponse], total: int, page: int
```

### FORMAT PATTERNS

#### API Response Format
```json
SUCCESS (200/201):
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "Task title",
  "description": "Description",
  "status": "todo",
  "created_at": "2025-11-12T10:30:00Z",
  "updated_at": "2025-11-12T10:30:00Z"
}

ERROR (4xx/5xx):
{
  "detail": "Error message here"
}

// NO WRAPPER - FastAPI returns data directly
❌ { "data": {...}, "success": true }
❌ { "result": {...}, "error": null }
```

#### Date/Time Format
```
CONVENTION: ISO 8601 strings in UTC

Backend (Pydantic):
created_at: datetime  # Serializes to ISO 8601

Frontend (TypeScript):
created_at: string  # ISO 8601 from API
display: formatDate(task.created_at)  // Helper function

✅ "2025-11-12T10:30:00Z"
❌ "11/12/2025"
❌ Unix timestamps
```

#### Environment Variables
```
CONVENTION: SCREAMING_SNAKE_CASE

✅ DATABASE_URL
✅ ENTRAID_CLIENT_ID
✅ SESSION_SECRET_KEY
❌ databaseUrl, database-url
```

### COMMUNICATION PATTERNS

#### Zustand Store Pattern
```typescript
// EVERY store follows this structure
type StoreState = {
  // Data
  items: Item[];
  loading: boolean;
  error: string | null;
};

type StoreActions = {
  // Actions
  fetchItems: () => Promise<void>;
  createItem: (data: ItemCreate) => Promise<void>;
  updateItem: (id: string, data: ItemUpdate) => Promise<void>;
  deleteItem: (id: string) => Promise<void>;
};

// Combine in create
export const useItemStore = create<StoreState & StoreActions>((set, get) => ({
  items: [],
  loading: false,
  error: null,

  fetchItems: async () => {
    set({ loading: true });
    try {
      const items = await itemService.getItems();
      set({ items, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },
  // ... other actions
}));
```

#### FastAPI Dependency Pattern
```python
# EVERY protected endpoint uses this pattern
# get_current_user lives in auth feature slice

from app.features.auth.dependencies import get_current_user
from app.features.users.model import User

@router.get("/api/resource")
async def get_resource(
    current_user: User = Depends(get_current_user)
):
    # current_user is validated and populated from session
    # Automatic 401 if session invalid
    pass

# app/features/auth/dependencies.py
from fastapi import Depends, HTTPException, status, Request
from app.core.security import validate_session
from app.core.database import get_db
from app.features.users.model import User
from sqlalchemy.ext.asyncio import AsyncSession

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User:
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    user_data = await validate_session(session_id)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )

    # Fetch full user from database
    result = await db.execute(
        select(User).where(User.id == user_data["user_id"])
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
```

### CONSISTENCY PATTERNS

#### Error Handling
```typescript
// Frontend: Always use try/catch in store actions
try {
  const response = await api.post('/api/tasks', data);
  set({ tasks: [...get().tasks, response] });
} catch (error) {
  set({ error: error.message });
  // Toast notification for user feedback
  toast.error('Failed to create task');
}
```

```python
# Backend: Use FastAPI's HTTPException
from fastapi import HTTPException, status

if not task:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )

if task.user_id != current_user.id:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to access this task"
    )
```

#### User Data Isolation
```python
# EVERY query MUST filter by user_id from session

# ✅ Correct
tasks = await db.execute(
    select(Task).where(Task.user_id == current_user.id)
)

# ❌ WRONG - exposes all users' data
tasks = await db.execute(select(Task))
```

#### Optimistic Updates
```typescript
// Create/Update/Delete: Update UI immediately, rollback on error

deleteTask: async (id: string) => {
  const previousTasks = get().tasks;

  // Optimistic update
  set({ tasks: previousTasks.filter(t => t.id !== id) });

  try {
    await taskService.deleteTask(id);
    toast.success('Task deleted');
  } catch (error) {
    // Rollback on error
    set({ tasks: previousTasks });
    toast.error('Failed to delete task');
  }
}
```

## Data Architecture

### Database Schema

**Users Table**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entraid_user_id VARCHAR(255) UNIQUE NOT NULL,  -- 'sub' claim from ID token
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_entraid_user_id ON users(entraid_user_id);
```

**Tasks Table**
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'todo' CHECK (status IN ('todo', 'done')),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_updated_at ON tasks(updated_at DESC);
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
```

**Inspirations Table**
```sql
CREATE TABLE inspirations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    captured_date DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_inspirations_user_id ON inspirations(user_id);
CREATE INDEX idx_inspirations_captured_date ON inspirations(captured_date DESC);
```

### Entity Relationships

```
users (1) ────< (many) tasks
  │
  └──────────< (many) inspirations
```

**Key Constraints:**
- All entities belong to exactly one user
- Cascade delete: If user deleted, all tasks and inspirations deleted
- No cross-user references or sharing (single-tenant data model)

### Data Isolation Strategy

**Every query filters by user_id:**
```python
# SQLAlchemy pattern used throughout
async def get_user_tasks(user_id: UUID, db: AsyncSession):
    result = await db.execute(
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.updated_at.desc())
    )
    return result.scalars().all()
```

**Ownership validation before modifications:**
```python
task = await db.get(Task, task_id)
if not task or task.user_id != current_user.id:
    raise HTTPException(status_code=403, detail="Not authorized")
```

## API Contracts

### Authentication Endpoints

**POST /api/auth/login**
- Initiates OAuth2 flow
- Redirects to EntraID authorization URL
- No request body
- Response: 302 Redirect to EntraID

**GET /api/auth/callback**
- OAuth2 callback from EntraID
- Query params: `code`, `state`
- Exchanges code for tokens (server-side)
- Creates session, sets HTTP-only cookie
- Response: 302 Redirect to frontend home

**GET /api/auth/me**
- Returns current user profile
- Requires valid session cookie
- Response 200:
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "User Name"
}
```
- Response 401: Not authenticated

**POST /api/auth/logout**
- Destroys session
- Clears session cookie
- Response 200: `{"message": "Logged out"}`

### Tasks Endpoints

**GET /api/tasks**
- Lists all user's tasks
- Requires authentication
- Response 200:
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "title": "Task title",
    "description": "Task description",
    "status": "todo",
    "created_at": "2025-11-12T10:30:00Z",
    "updated_at": "2025-11-12T10:30:00Z"
  }
]
```

**POST /api/tasks**
- Creates new task
- Request body:
```json
{
  "title": "New task",
  "description": "Optional description"
}
```
- Response 201: Created task object

**GET /api/tasks/{id}**
- Retrieves single task
- Response 200: Task object
- Response 403: Not owner
- Response 404: Not found

**PUT /api/tasks/{id}**
- Updates task (partial update)
- Request body (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "status": "done"
}
```
- Response 200: Updated task object

**DELETE /api/tasks/{id}**
- Deletes task
- Response 204: No content
- Response 403: Not owner
- Response 404: Not found

### Inspirations Endpoints

**GET /api/inspirations**
- Lists all user's inspirations
- Response 200: Array of inspiration objects

**POST /api/inspirations**
- Creates new inspiration
- Request body:
```json
{
  "title": "Inspiration title",
  "description": "Optional description"
}
```
- Response 201: Created inspiration object

**GET /api/inspirations/{id}**
- Retrieves single inspiration
- Response 200: Inspiration object

**PUT /api/inspirations/{id}**
- Updates inspiration
- Request body (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description"
}
```
- Response 200: Updated inspiration object

**DELETE /api/inspirations/{id}**
- Deletes inspiration
- Response 204: No content

**POST /api/inspirations/{id}/convert**
- Converts inspiration to task
- Creates task with copied title/description
- Deletes original inspiration
- Response 201: Created task object

### Common Response Codes

- **200 OK**: Successful GET/PUT
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Missing or invalid session
- **403 Forbidden**: Not authorized (wrong user)
- **404 Not Found**: Resource doesn't exist
- **422 Unprocessable Entity**: Validation error

## Security Architecture

### Authentication Flow (Maximum Security Pattern)

```
┌─────────┐                                ┌──────────┐
│ Browser │                                │ Frontend │
└────┬────┘                                └─────┬────┘
     │                                           │
     │ 1. Click "Sign in with Microsoft"        │
     │─────────────────────────────────────────>│
     │                                           │
     │ 2. Redirect to /api/auth/login           │
     │<──────────────────────────────────────────│
     │                                           │
     │                                    ┌──────▼───────┐
     │                                    │   Backend    │
     │                                    │   (FastAPI)  │
     │                                    └──────┬───────┘
     │ 3. 302 Redirect to EntraID               │
     │<─────────────────────────────────────────┤
     │                                           │
┌────▼────────┐                                 │
│   EntraID   │                                 │
│ (Azure AD)  │                                 │
└────┬────────┘                                 │
     │                                           │
     │ 4. User authenticates (MFA, etc.)        │
     │                                           │
     │ 5. Redirect to /api/auth/callback        │
     │    with authorization code               │
     │──────────────────────────────────────────>│
     │                                           │
     │                                    ┌──────▼───────┐
     │                                    │   Backend    │
     │                                    │              │
     │                                    │ 6. Exchange  │
     │                                    │    code for  │
     │                                    │    tokens    │
     │                                    │              │
     │                                    │ 7. Validate  │
     │                                    │    ID token  │
     │                                    │              │
     │                                    │ 8. Create    │
     │                                    │    session   │
     │                                    │    in Redis  │
     │                                    │              │
     │                                    │ 9. Set       │
     │                                    │    HTTP-only │
     │                                    │    cookie    │
     │                                    └──────┬───────┘
     │                                           │
     │ 10. 302 Redirect to frontend home        │
     │<──────────────────────────────────────────┤
     │    with session cookie                    │
     │                                           │
┌────▼────┐                                     │
│ Browser │ Session cookie auto-included        │
│         │ in all subsequent requests          │
└─────────┘                                     │
```

### Session Security

**HTTP-only Signed Cookies:**
```python
# Cookie attributes
response.set_cookie(
    key="session_id",
    value=signed_session_id,  # Signed to prevent tampering
    httponly=True,            # JavaScript cannot access
    secure=True,              # HTTPS only (production)
    samesite="lax",           # CSRF protection
    max_age=86400             # 24 hours
)
```

**Session Storage:**
- Production: Redis with 24-hour TTL
- Development: In-memory dictionary
- Session contains: user_id, email, name, created_at, expires_at

**Zero Token Exposure:**
- Access tokens NEVER sent to browser
- Refresh tokens NEVER sent to browser
- ID tokens validated server-side only
- Only session ID (opaque, signed) exposed

### Data Security

**User Data Isolation:**
- Every query filters by `user_id` from session
- Ownership validation before updates/deletes
- No shared data between users

**Input Validation:**
- Pydantic schemas validate all inputs
- Character limits enforced (title: 200, description: 2000)
- SQL injection prevented (SQLAlchemy ORM, parameterized queries)
- XSS prevented (React escapes by default, no dangerouslySetInnerHTML)

**Secrets Management:**
- Environment variables for all secrets
- Never commit `.env` files
- Different secrets for dev/staging/prod

### HTTPS Requirement

**Production must use HTTPS:**
- Secure cookies require HTTPS
- Prevents session hijacking
- Protects against man-in-the-middle attacks

## Performance Considerations

### Database Performance

**Indexes on hot paths:**
```sql
-- User lookup by EntraID ID
CREATE INDEX idx_users_entraid_user_id ON users(entraid_user_id);

-- Task queries by user
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_updated_at ON tasks(updated_at DESC);

-- Combined index for filtered queries
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
```

**Query Optimization:**
- Use `select()` with specific columns instead of `SELECT *`
- Limit result sets (pagination if lists grow beyond 100 items)
- Avoid N+1 queries (use `joinedload()` if needed)

### Session Performance

**Redis for Production:**
- Sub-millisecond session lookups
- Automatic TTL expiration
- Connection pooling

**Caching Strategy:**
- Session validation cached in request context
- No need to re-validate within same request

### Frontend Performance

**Code Splitting:**
```typescript
// Lazy load routes
const Tasks = lazy(() => import('./pages/Tasks'));
const Inspirations = lazy(() => import('./pages/Inspirations'));
```

**Optimistic Updates:**
- Immediate UI feedback
- No waiting for API responses
- Better perceived performance

**Bundle Size:**
- Vite tree-shaking removes unused code
- Tailwind purges unused CSS
- Target: < 500KB gzipped JavaScript

## Deployment Architecture

### Single-Server Pattern

```
┌─────────────────────────────────────────┐
│         Production Server                │
│                                          │
│  ┌────────────────────────────────┐     │
│  │       FastAPI (uvicorn)        │     │
│  │                                 │     │
│  │  ┌──────────────────────────┐  │     │
│  │  │  /  → React static files │  │     │
│  │  │  /api/*  → API endpoints │  │     │
│  │  └──────────────────────────┘  │     │
│  └────────────────────────────────┘     │
│                │                         │
│                │                         │
│         ┌──────▼──────┐                  │
│         │   Redis     │                  │
│         │  (sessions) │                  │
│         └─────────────┘                  │
└─────────────────────────────────────────┘
               │
        ┌──────▼──────┐
        │ PostgreSQL  │
        │  Database   │
        └─────────────┘
```

### Environment Variables

**Backend (.env):**
```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/nomi

# EntraID OAuth
ENTRAID_CLIENT_ID=your-client-id
ENTRAID_CLIENT_SECRET=your-client-secret
ENTRAID_TENANT_ID=your-tenant-id
ENTRAID_REDIRECT_URI=https://yourdomain.com/api/auth/callback

# Session
SESSION_SECRET_KEY=random-secret-key-here
SESSION_BACKEND=redis  # or "memory" for dev
REDIS_URL=redis://localhost:6379

# Environment
ENVIRONMENT=production  # or "development"
```

**Frontend (.env):**
```bash
# Vite automatically prefixes with VITE_
VITE_API_URL=/api  # Same origin in production
```

### Production Deployment

**Build Frontend:**
```bash
cd nomi-frontend
npm run build
# Output: nomi-frontend/dist/
```

**Run Backend:**
```bash
cd nomi-backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**FastAPI Serves Both:**
```python
# app/main.py
from fastapi.staticfiles import StaticFiles

# API routes
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(inspirations_router)

# Serve React build
app.mount("/", StaticFiles(directory="../nomi-frontend/dist", html=True), name="static")
```

## Development Environment

### Prerequisites

- **Node.js 20.x+** and npm
- **Python 3.10+**
- **PostgreSQL 16.x** or 17.x
- **Redis 7.x** (optional for development)
- **EntraID Application** registered in Azure Portal

### Setup Commands

**1. Clone and Setup Frontend:**
```bash
# Create and enter frontend directory
npm create vite@latest nomi-frontend -- --template react-ts
cd nomi-frontend

# Install dependencies
npm install react-router-dom zustand
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Configure Vite proxy (vite.config.ts)
export default defineConfig({
  server: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})

# Start development server
npm run dev  # Runs on http://localhost:5173
```

**2. Setup Backend:**
```bash
mkdir nomi-backend && cd nomi-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install "fastapi[standard]>=0.121.0" "sqlalchemy[asyncio]>=2.0.44"
pip install "alembic>=1.13.0" "msal>=1.34.0" "psycopg[binary]>=3.1.0"
pip install "python-dotenv>=1.0.0" "redis>=5.0.0"

# Initialize Alembic
alembic init alembic

# Create .env file (copy from .env.example and fill in values)

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload  # Runs on http://localhost:8000
```

**3. Configure EntraID:**
- Azure Portal → App Registrations → New Registration
- Platform: Web
- Redirect URI: `http://localhost:8000/api/auth/callback`
- Generate client secret
- Add to `.env`: `ENTRAID_CLIENT_ID`, `ENTRAID_CLIENT_SECRET`, `ENTRAID_TENANT_ID`

### Development Workflow

1. Start PostgreSQL (local or Docker)
2. Start Redis (optional - uses in-memory if not available)
3. Start backend: `uvicorn app.main:app --reload`
4. Start frontend: `npm run dev`
5. Access app: `http://localhost:5173`
6. API requests automatically proxied to backend

## Architecture Decision Records (ADRs)

### ADR-001: Server-Side OAuth2 with HTTP-Only Cookies

**Context:** Need maximum-security authentication pattern for enterprise applications.

**Decision:** Use server-side OAuth2 authorization code flow with EntraID, storing sessions in HTTP-only signed cookies.

**Alternatives Considered:**
- Client-side MSAL.js with tokens in localStorage ❌ Vulnerable to XSS
- JWT in localStorage ❌ Token theft via XSS
- JWT in memory only ❌ Lost on page refresh

**Consequences:**
- ✅ Complete immunity to XSS token theft
- ✅ Browser cannot access tokens
- ✅ CSRF protected with SameSite cookies
- ⚠️ Requires session storage (Redis)
- ⚠️ Cannot call Microsoft Graph from frontend (backend proxy needed)

**Rationale:** This is THE crown jewel pattern - demonstrates enterprise-grade security worth copying.

### ADR-002: Single-Server Deployment Pattern

**Context:** Need simplified deployment while remaining production-viable.

**Decision:** FastAPI serves both React static files and API endpoints from same origin.

**Alternatives Considered:**
- Separate frontend (Vercel) + backend (AWS) ❌ CORS complexity
- Nginx reverse proxy ❌ Additional infrastructure
- API Gateway ❌ Over-engineering

**Consequences:**
- ✅ No CORS configuration needed
- ✅ Cookies work seamlessly (same origin)
- ✅ Simplified deployment (one server)
- ✅ Development proxy mirrors production
- ⚠️ Couples frontend/backend deployment

**Rationale:** Eliminates common deployment headaches while teaching clean patterns.

### ADR-003: Zustand Over Redux/Context API

**Context:** Need state management that's simple to learn but powerful enough for real apps.

**Decision:** Use Zustand for all client state management.

**Alternatives Considered:**
- Redux Toolkit ❌ Too much boilerplate for learning project
- Context API ❌ Performance issues, re-render problems
- Jotai/Recoil ❌ Atomic state adds complexity

**Consequences:**
- ✅ Minimal boilerplate (no actions/reducers)
- ✅ Excellent TypeScript support
- ✅ Simple mental model (just a hook)
- ✅ Good performance (selective subscriptions)
- ⚠️ Less structure than Redux (requires discipline)

**Rationale:** Best balance of simplicity and power for intermediate developers.

### ADR-004: PostgreSQL with SQLAlchemy 2.0 Async

**Context:** Need production-grade database with modern async patterns.

**Decision:** PostgreSQL with SQLAlchemy 2.0 async ORM and Alembic migrations.

**Alternatives Considered:**
- MongoDB ❌ Relational data fits better
- Prisma ❌ TypeScript-focused, not Python
- Django ORM ❌ Tied to Django framework

**Consequences:**
- ✅ ACID compliance for data integrity
- ✅ Excellent JSON support (JSONB)
- ✅ Mature ecosystem
- ✅ Modern async/await syntax
- ✅ Type-safe queries
- ⚠️ Requires understanding of async SQLAlchemy

**Rationale:** Industry-standard relational DB with modern Python async support.

### ADR-005: Vertical Slice Architecture (Feature-First Organization)

**Context:** Need backend architecture that maximizes maintainability, makes features easy to understand, and reduces coupling while serving as a learning reference.

**Decision:** Organize backend using Vertical Slice Architecture with feature-first structure (`features/tasks/`, `features/auth/`, etc.) instead of traditional layered architecture (`api/`, `models/`, `services/`, `schemas/`).

**Alternatives Considered:**
- **Layered Architecture** ❌ Feature code scattered across multiple directories, high cognitive load
- **Monolithic Single-File** ❌ Doesn't scale, hard to navigate
- **Microservices** ❌ Over-engineering for this scale, deployment complexity

**Vertical Slice Structure:**
```
features/
  tasks/
    endpoints.py   # FastAPI routes
    model.py       # SQLAlchemy model
    schemas.py     # Pydantic schemas
    service.py     # Business logic
  inspirations/
    endpoints.py
    model.py
    schemas.py
    service.py
```

**Key Principles:**
1. **High Cohesion Within Slices**: Everything for "tasks" lives in `features/tasks/`
2. **Low Coupling Between Slices**: Changes to tasks don't affect inspirations
3. **Intentional Duplication**: Similar CRUD patterns duplicated across slices (not shared)
4. **Cross-Cutting in Core**: Only infrastructure concerns (`database.py`, `security.py`, `config.py`)

**Consequences:**
- ✅ **Easy Navigation**: "Where's the task creation logic?" → `features/tasks/service.py`
- ✅ **Localized Changes**: New task field? Only touch `features/tasks/`
- ✅ **Parallel Development**: Multiple devs/agents can work on different features simultaneously
- ✅ **Better Learning**: Clear boundaries, easy to understand one feature at a time
- ✅ **Reduced Cognitive Load**: Don't need to understand whole system to change one feature
- ⚠️ **Code Duplication**: CRUD patterns repeated (this is intentional - slices evolve independently)
- ⚠️ **Discipline Required**: Must resist premature abstraction to shared base classes

**Comparison to Layered Architecture:**

| Aspect | Layered (api/, models/, services/) | Vertical Slice (features/) |
|--------|-----------------------------------|---------------------------|
| Add task filter | Touch: api/tasks.py, services/task_service.py, schemas/task.py | Touch: features/tasks/ only |
| Feature cohesion | Low (scattered) | High (co-located) |
| Code navigation | Jump between directories | Everything in one folder |
| Shared code | Encouraged (base classes) | Discouraged (duplication OK) |
| Coupling | High (layers depend on layers) | Low (slices independent) |
| Cognitive load | High (must understand all layers) | Low (understand one slice) |

**Rationale:**

For a **learning-focused reference architecture**, vertical slices provide:
1. **Clear Mental Model**: "Each feature is self-contained"
2. **Easy to Copy**: Copy `features/tasks/` pattern for new features
3. **Reduced Side Effects**: Changes don't ripple unexpectedly
4. **Production Viable**: Pattern scales from 3 features to 30 features

This architecture optimizes for **maintainability and understanding** over theoretical DRY principles. The intentional duplication between slices is a feature, not a bug - it allows each slice to evolve independently without breaking others.

**When to Use Vertical Slices:**
- ✅ Feature-rich applications (multiple distinct capabilities)
- ✅ Learning/reference codebases
- ✅ Teams with multiple developers
- ✅ Long-lived projects that will evolve

**When NOT to Use:**
- ❌ Microservices (each service is already a slice)
- ❌ Tiny apps (< 3 features) where layered is simpler
- ❌ Highly interconnected domain logic requiring shared business rules

### ADR-006: REPR Pattern (Request-Endpoint-Response)

**Context:** Need clear, maintainable API endpoint structure with strong contracts, automatic validation, and excellent documentation for both developers and AI agents implementing features.

**Decision:** Adopt REPR (Request-Endpoint-Response) pattern for all API endpoints - each endpoint has explicit Pydantic request/response schemas, single responsibility, and clear documentation.

**Pattern Definition:**
```
REQUEST → ENDPOINT → RESPONSE

Request:  Explicit Pydantic schema defining input (validation, documentation)
Endpoint: Single-purpose function handling one specific operation
Response: Explicit Pydantic schema defining output (serialization, documentation)
```

**REPR in FastAPI:**
```python
# Example: Create Task Endpoint

# REQUEST schema
class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=2000)

# ENDPOINT handler
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskCreateRequest,  # Explicit request
    current_user: User = Depends(get_current_user)
):
    task = await TaskService.create_task(current_user.id, request)
    return task  # FastAPI serializes via response_model

# RESPONSE schema
class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime
```

**Alternatives Considered:**

1. **Generic CRUD Controllers** ❌
   - Pro: Less code duplication
   - Con: Harder to customize per-endpoint
   - Con: Single controller handles multiple operations (bloated)
   - Con: Difficult to understand which schema applies to which operation

2. **Returning ORM Models Directly** ❌
   - Pro: No schema definition needed
   - Con: Exposes internal database structure
   - Con: No control over serialization
   - Con: Tight coupling between API and database

3. **Untyped Dictionaries** ❌
   - Pro: Maximum flexibility
   - Con: No validation
   - Con: No auto-generated documentation
   - Con: Runtime errors instead of compile-time checks

4. **Single Shared Request/Response Schema** ❌
   - Pro: Less schema definitions
   - Con: All fields optional (validation nightmare)
   - Con: Unclear which fields apply to which endpoint
   - Con: Breaking changes affect all endpoints

**Key Principles:**

1. **Explicit Request Schemas**
   - Every input has a dedicated schema
   - Validation rules in the schema (min_length, pattern, etc.)
   - Schema names end with "Request": `TaskCreateRequest`, `TaskUpdateRequest`

2. **Explicit Response Schemas**
   - Every output has a dedicated schema
   - Serialization controlled by schema
   - Schema names end with "Response": `TaskResponse`, `TaskListResponse`

3. **Single Responsibility**
   - Each endpoint does ONE thing
   - `create_task()` only creates tasks
   - `update_task()` only updates tasks
   - No combined operations like `upsert_task()`

4. **List Responses Wrapped**
   - Don't return `list[TaskResponse]` directly
   - Wrap in `TaskListResponse(tasks: list[TaskResponse])`
   - Allows future metadata without breaking changes

**Consequences:**

✅ **Benefits:**
- **Type Safety**: Pydantic validates all inputs/outputs at runtime
- **Auto-Documentation**: OpenAPI/Swagger docs are complete and accurate
- **Clear Contracts**: Developers know exactly what to send/receive
- **Easy Testing**: Mock requests/responses with known schemas
- **Refactor Safety**: Changes to one endpoint don't affect others
- **AI-Friendly**: Clear patterns for code generation
- **Version Tolerance**: Can add optional fields without breaking clients

⚠️ **Trade-offs:**
- **More Code**: Each endpoint needs request/response schemas
- **Schema Proliferation**: TaskCreateRequest, TaskUpdateRequest, etc.
- **Duplication**: Similar fields across schemas (intentional)

**Synergy with Vertical Slices:**

REPR and Vertical Slice Architecture work perfectly together:
- Each feature slice (e.g., `features/tasks/`) contains its schemas
- Request/Response schemas live in `features/tasks/schemas.py`
- All task-related contracts in one place
- High cohesion: schema + endpoint + service + model together

**Comparison:**

| Aspect | Generic Controllers | REPR Pattern |
|--------|-------------------|--------------|
| Endpoint responsibility | Multiple operations per controller | One operation per endpoint |
| Request validation | Scattered or implicit | Explicit Pydantic schema |
| Response structure | ORM models or dicts | Explicit Pydantic schema |
| Documentation | Manual or incomplete | Auto-generated from schemas |
| Customization | Difficult (affects all operations) | Easy (endpoint-specific) |
| Testability | Mock entire controller | Mock single endpoint |
| API contract | Implicit or documented separately | Explicit in code |

**Rationale:**

For Nomi as a **learning-focused reference architecture**, REPR provides:

1. **Clear Learning**: Each endpoint is self-documenting
2. **Best Practice**: Industry-standard pattern (originated in .NET, applies to all frameworks)
3. **Type Safety**: Catches errors at development time
4. **Copy-Paste Friendly**: Clear template for adding new endpoints
5. **Production Viable**: Pattern scales from 5 endpoints to 500 endpoints
6. **Auto-Documentation**: OpenAPI docs always accurate

The slight code duplication (multiple request/response schemas) is a feature, not a bug - it allows each endpoint to evolve independently without breaking others.

**Implementation Guidelines:**

```python
# NAMING: Descriptive and consistent
TaskCreateRequest     # POST request
TaskUpdateRequest     # PUT request
TaskResponse          # Single entity response
TaskListResponse      # Collection response

# VALIDATION: In the schema
title: str = Field(..., min_length=1, max_length=200)
status: str = Field(..., pattern="^(todo|done)$")

# DOCUMENTATION: Examples in schema
class Config:
    json_schema_extra = {
        "example": {...}
    }

# STATUS CODES: Explicit
@router.post(..., status_code=status.HTTP_201_CREATED)
@router.get(..., status_code=status.HTTP_200_OK)
@router.delete(..., status_code=status.HTTP_204_NO_CONTENT)
```

**When to Use REPR:**
- ✅ All API endpoints in the application
- ✅ Public and internal APIs
- ✅ REST APIs with clear operations

**When NOT to Use:**
- ❌ GraphQL APIs (different pattern)
- ❌ WebSocket/SSE (streaming, not request-response)
- ❌ Internal function calls (overhead without benefit)

---

**🎯 Architecture Complete**

This architecture document provides the complete technical blueprint for Nomi - a "Goldilocks" reference implementation proving enterprise patterns at learnable scale.

**Next Steps:**
1. Review this architecture document
2. Run `/bmad:bmm:workflows:solutioning-gate-check` (validates PRD + Architecture alignment)
3. Proceed to Epic breakdown and story creation
4. Begin implementation with Epic 1 (Project Foundation)

---

_Generated by BMAD Decision Architecture Workflow_
_Date: 2025-11-12_
_Updated: 2025-11-12 (Revised to Vertical Slice Architecture + REPR Pattern)_
_Architect: Winston (BMAD Architect Agent)_
_For: Justin_
