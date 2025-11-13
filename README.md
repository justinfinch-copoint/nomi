# Nomi - Personal Task Management & Inspiration Platform

A modern web application that combines task management with AI-powered inspirational content, built with React, FastAPI, and PostgreSQL.

## Project Structure

```
nomi/
├── nomi-frontend/          # React + TypeScript + Vite frontend
│   ├── src/
│   │   ├── components/     # React components (common, tasks, inspirations, layout)
│   │   ├── pages/          # Route components
│   │   ├── stores/         # Zustand state management
│   │   ├── services/       # API client functions
│   │   ├── utils/          # Helper functions
│   │   └── types/          # TypeScript type definitions
│   └── package.json
│
└── nomi-backend/           # FastAPI backend
    ├── app/
    │   ├── features/       # Feature slices (vertical architecture)
    │   ├── core/           # Shared infrastructure
    │   └── main.py         # FastAPI app initialization
    └── requirements.txt
```

## Technology Stack

### Frontend
- **React** 19.2.0 - UI framework
- **TypeScript** 5.9.x - Type safety
- **Vite** 7.2.2 - Build tool with HMR
- **Zustand** 5.0.8 - State management
- **React Router** 7.9.x - Client-side routing
- **Tailwind CSS** 4.0 - Utility-first CSS

### Backend
- **FastAPI** 0.121+ - Modern Python web framework
- **SQLAlchemy** 2.0.44 - Async ORM
- **PostgreSQL** 16.x/17.x - Database
- **Alembic** 1.13+ - Database migrations
- **MSAL** 1.34+ - Microsoft Entra ID authentication

## Quick Start

### Prerequisites
- Node.js 18+ and npm/pnpm
- Python 3.10+
- PostgreSQL 16+ (for database features)

### Frontend Setup

```bash
cd nomi-frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:5173 with hot module reload.

### Backend Setup

```bash
cd nomi-backend
pip install -r requirements.txt

# Copy environment template and configure
cp .env.example .env
# Edit .env with your configuration

# Run the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at http://localhost:8000 with auto-reload.

### Development

**Frontend Development:**
- `npm run dev` - Start dev server with HMR
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run preview` - Preview production build

**Backend Development:**
- The frontend Vite dev server proxies `/api/*` requests to the backend
- Backend runs with uvicorn auto-reload for instant updates
- Format code: `black .`
- Lint code: `ruff check .`

## API Documentation

When the backend is running, visit:
- Interactive API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Architecture Patterns

### Backend
- **Vertical Slice Architecture**: Features organized by use case in `app/features/`
- **REPR Pattern**: Each endpoint in a separate file (Route, Endpoint, Processor, Repository)
- **Async/Await**: SQLAlchemy 2.0 async for optimal performance

### Frontend
- **Component Organization**: Features grouped by domain (tasks, inspirations, common)
- **State Management**: Zustand for simple, scalable state
- **API Layer**: Centralized API client in `services/`

## Configuration

### Environment Variables

**Frontend** (`.env.example`):
- `VITE_API_BASE_URL` - API base URL (defaults to `/api`)

**Backend** (`.env.example`):
- `DATABASE_URL` - PostgreSQL connection string
- `ENTRAID_CLIENT_ID` - Microsoft Entra ID client ID
- `ENTRAID_TENANT_ID` - Microsoft Entra ID tenant ID
- `SESSION_SECRET_KEY` - Secret key for session signing
- `CORS_ORIGINS` - Allowed CORS origins

## Development Workflow

1. Start the backend: `cd nomi-backend && uvicorn app.main:app --reload`
2. Start the frontend: `cd nomi-frontend && npm run dev`
3. Access the app at http://localhost:5173
4. API requests are automatically proxied to the backend

## License

Private - All Rights Reserved
