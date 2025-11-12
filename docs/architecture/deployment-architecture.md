# Deployment Architecture

## Single-Server Pattern

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

## Environment Variables

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

## Production Deployment

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
