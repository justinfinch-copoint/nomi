# Project Structure

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
