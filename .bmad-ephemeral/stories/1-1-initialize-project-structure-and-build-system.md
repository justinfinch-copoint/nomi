# Story 1.1: Initialize Project Structure and Build System

Status: review

## Story

As a **developer**,
I want the complete project structure with React + Vite frontend and FastAPI backend initialized,
So that I have a working development environment with hot module reload and a clear separation of concerns.

## Acceptance Criteria

1. **Given** a greenfield project **When** I run the initialization commands **Then** I have a working frontend at `http://localhost:5173` with Vite HMR

2. **And** I have a working backend at `http://localhost:8000` with FastAPI auto-reload

3. **And** the frontend has a Vite proxy configured to forward `/api/*` requests to the backend

4. **And** the project structure follows best practices:
   - `frontend/src/` (components, pages, stores, services, utils)
   - `backend/app/` (api, models, schemas, services, core)

5. **And** I have package management configured (npm/pnpm for frontend, pip/poetry for backend)

6. **And** basic linting is configured (ESLint + Prettier for frontend, Black + Ruff for backend)

## Tasks / Subtasks

- [x] **Task 1: Initialize Frontend (React + Vite + TypeScript)** (AC: #1, #3, #4)
  - [x] Subtask 1.1: Create React + TypeScript + Vite project (`npm create vite@latest nomi-frontend -- --template react-ts`)
  - [x] Subtask 1.2: Install core dependencies (react-router-dom, zustand)
  - [x] Subtask 1.3: Install and configure Tailwind CSS
  - [x] Subtask 1.4: Configure Vite proxy to forward `/api/*` to `http://localhost:8000`
  - [x] Subtask 1.5: Create project structure folders (components/, pages/, stores/, services/, utils/, types/)
  - [x] Subtask 1.6: Install ESLint and Prettier for frontend linting
  - [x] Subtask 1.7: Verify frontend runs at `http://localhost:5173` with hot module reload

- [x] **Task 2: Initialize Backend (FastAPI + Python)** (AC: #2, #4)
  - [x] Subtask 2.1: Create backend directory `nomi-backend`
  - [x] Subtask 2.2: Initialize Python virtual environment (skipped - using devcontainer)
  - [x] Subtask 2.3: Install FastAPI and core dependencies (fastapi[standard], sqlalchemy[asyncio], alembic, msal, psycopg, python-dotenv, pydantic)
  - [x] Subtask 2.4: Create project structure (app/features/, app/core/, main.py)
  - [x] Subtask 2.5: Create basic FastAPI app with health check endpoint
  - [x] Subtask 2.6: Install Black and Ruff for backend linting
  - [x] Subtask 2.7: Verify backend runs at `http://localhost:8000` with auto-reload

- [x] **Task 3: Configure Project Files and Git** (AC: #5, #6)
  - [x] Subtask 3.1: Create `.gitignore` for both frontend and backend
  - [x] Subtask 3.2: Create `.env.example` files for environment variables template
  - [x] Subtask 3.3: Create `README.md` with project overview and quick start instructions
  - [x] Subtask 3.4: Initialize git repository and create initial commit (staged, pending user confirmation)
  - [x] Subtask 3.5: Document setup commands in README

- [x] **Task 4: Test Integration** (AC: #1, #2, #3)
  - [x] Subtask 4.1: Start both frontend and backend servers
  - [x] Subtask 4.2: Verify Vite proxy forwards requests from frontend to backend
  - [x] Subtask 4.3: Test HMR on frontend (make a change, verify hot reload)
  - [x] Subtask 4.4: Test auto-reload on backend (make a change, verify restart)

## Dev Notes

### Architecture Patterns and Constraints

**Project Structure Pattern:**
- Follow the exact structure defined in `/workspace/docs/architecture/project-structure.md`
- Frontend: `nomi-frontend/` with src/ subdirectories for components, pages, stores, services, utils, types
- Backend: `nomi-backend/` with app/features/ (vertical slice architecture) and app/core/ (shared infrastructure)
- Use Vertical Slice + REPR pattern for backend organization (each endpoint = one file)

**Technology Stack:**
- **Frontend:** React 19.2.0, TypeScript 5.9.x, Vite 7.1.9, Zustand 5.0.8, React Router 7.9.x, Tailwind CSS 4.0
- **Backend:** FastAPI 0.121.1+, SQLAlchemy 2.0.44 (async), PostgreSQL 16.x/17.x, MSAL Python 1.34.0, Alembic 1.13.0+
- **Python Version:** 3.10+

**Implementation Commands (from architecture/project-initialization.md):**

Frontend:
```bash
npm create vite@latest nomi-frontend -- --template react-ts
cd nomi-frontend
npm install react-router-dom zustand
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install
```

Backend:
```bash
mkdir nomi-backend
cd nomi-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install "fastapi[standard]>=0.121.0" "sqlalchemy[asyncio]>=2.0.44" "alembic>=1.13.0" "msal>=1.34.0"
pip install "psycopg[binary]>=3.1.0" "python-dotenv>=1.0.0" "pydantic>=2.0.0"
```

**Vite Proxy Configuration:**
Configure in `vite.config.ts` to forward `/api/*` requests to backend during development:
```typescript
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

**Naming Conventions (from implementation-patterns.md):**
- REST endpoints: Plural nouns, lowercase, hyphen-separated (`/api/tasks`)
- Database: snake_case for tables and columns (`tasks`, `user_id`, `created_at`)
- Python: Files in snake_case, Classes in PascalCase, functions/variables in snake_case
- TypeScript: Components PascalCase, services/utilities camelCase, types PascalCase

**Linting Configuration:**
- Frontend: ESLint + Prettier
- Backend: Black + Ruff for Python formatting
- Set up pre-commit hooks for consistency

**Environment Variables:**
- Create `.env.example` files showing required variables (DATABASE_URL, ENTRAID_CLIENT_ID, etc.)
- Use SCREAMING_SNAKE_CASE for all environment variables

### Project Structure Notes

The project follows a **single-server deployment pattern** where FastAPI will serve both the React build (in production) and API endpoints. During development:
- Frontend runs on port 5173 (Vite dev server with HMR)
- Backend runs on port 8000 (FastAPI with uvicorn auto-reload)
- Vite proxy forwards API requests to eliminate CORS issues

**Critical Directory Structure to Create:**

Frontend (`nomi-frontend/src/`):
```
components/
  common/       # Shared components (Button, Input, Modal)
  tasks/        # Task-specific components
  inspirations/ # Inspiration components
  layout/       # Layout components (Header, Nav)
pages/          # Route components (Home, Login, Tasks, Inspirations, Profile)
stores/         # Zustand stores (authStore, tasksStore, inspirationsStore)
services/       # API client functions (api.ts, authService.ts, tasksService.ts)
utils/          # Helper functions (formatDate.ts, validators.ts)
types/          # TypeScript types (auth.ts, task.ts, inspiration.ts)
```

Backend (`nomi-backend/app/`):
```
features/       # Feature slices (vertical organization)
  auth/         # Authentication feature slice
  tasks/        # Task management feature slice
  inspirations/ # Inspiration management feature slice
  users/        # User profile feature slice
core/           # Shared infrastructure
  config.py     # Settings (environment variables)
  security.py   # Session validation, cookie signing
  database.py   # Database connection, session factory
  session_store.py  # Session manager (Redis/in-memory)
main.py         # FastAPI app initialization
```

### References

- [Source: docs/epics/epic-1-project-foundation-infrastructure.md#Story-1.1]
- [Source: docs/architecture/project-initialization.md]
- [Source: docs/architecture/project-structure.md]
- [Source: docs/architecture/technology-stack-details.md]
- [Source: docs/architecture/implementation-patterns.md]
- [Source: docs/PRD/web-application-specific-requirements.md#Application-Architecture-Pattern]
- [Source: docs/PRD/non-functional-requirements.md#NFR-MAINT-002]

### Quality Standards

**Performance Targets (from PRD):**
- Initial page load: < 3 seconds
- Time to interactive: < 2 seconds
- Subsequent navigation: < 500ms (client-side routing)

**Security:**
- Follow maximum security patterns (HTTP-only cookies, server-side sessions)
- No tokens exposed to browser
- HTTPS required in production

**Maintainability:**
- Consistent code style via linting tools
- Meaningful variable and function names
- Components < 200 lines
- Clear separation of concerns

## Dev Agent Record

### Context Reference

- `.bmad-ephemeral/stories/1-1-initialize-project-structure-and-build-system.context.xml`

### Agent Model Used

Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

### Debug Log References

N/A - No blocking issues encountered

### Completion Notes List

- Successfully initialized frontend with React 19.2.0, Vite 7.2.2, TypeScript 5.9.x
- Installed all required dependencies: react-router-dom 7.9.6, zustand 5.0.8, tailwindcss 4.1.17
- Configured Vite proxy to forward /api/* requests to backend at http://localhost:8000
- Created complete frontend directory structure with components/ (common/, tasks/, inspirations/, layout/), pages/, stores/, services/, utils/, types/
- Initialized backend with FastAPI 0.121.2, SQLAlchemy 2.0.44, and all required dependencies
- Used requirements.txt instead of virtual environment (devcontainer environment)
- Created backend structure with app/features/ (Vertical Slice architecture) and app/core/
- Implemented basic FastAPI app with /api/health endpoint and CORS configuration
- Configured Black 25.11.0 and Ruff 0.14.4 for backend linting (updated to new ruff.lint config format)
- Configured ESLint 9.39.1 and Prettier for frontend linting
- Created comprehensive .gitignore files for both frontend and backend
- Created .env.example files with environment variable templates
- Created comprehensive README.md with project overview, technology stack, and quick start instructions
- Verified both servers start correctly (frontend on :5173, backend on :8000)
- Verified Vite proxy successfully forwards API requests to backend
- Verified auto-reload works on both frontend (HMR) and backend (uvicorn --reload)
- All linting checks pass (ESLint, Prettier, Black, Ruff)
- Git repository initialized with staged changes ready for initial commit

### File List

**Frontend (nomi-frontend/):**
- package.json - Dependencies and scripts
- vite.config.ts - Vite configuration with proxy setup
- tailwind.config.js - Tailwind CSS configuration
- postcss.config.js - PostCSS configuration
- .prettierrc - Prettier configuration
- .gitignore - Frontend gitignore
- .env.example - Environment variable template
- src/index.css - Tailwind directives
- src/App.tsx - Updated with project branding
- src/components/common/ - Common components directory
- src/components/tasks/ - Task components directory
- src/components/inspirations/ - Inspiration components directory
- src/components/layout/ - Layout components directory
- src/pages/ - Page components directory
- src/stores/ - Zustand stores directory
- src/services/ - API services directory
- src/utils/ - Utility functions directory
- src/types/ - TypeScript types directory

**Backend (nomi-backend/):**
- requirements.txt - Python dependencies
- pyproject.toml - Black and Ruff configuration
- .gitignore - Backend gitignore
- .env.example - Environment variable template
- app/__init__.py - App package marker
- app/main.py - FastAPI application with /api router and health endpoint
- app/features/__init__.py - Features package marker
- app/core/__init__.py - Core package marker

**Root:**
- README.md - Project documentation with setup instructions
- .gitignore - Root gitignore (updated with .claude/, .bmad/ exclusions)
