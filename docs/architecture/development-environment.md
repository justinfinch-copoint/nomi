# Development Environment

## Prerequisites

- **Node.js 20.x+** and npm
- **Python 3.10+**
- **PostgreSQL 16.x** or 17.x
- **Redis 7.x** (optional for development)
- **EntraID Application** registered in Azure Portal

## Setup Commands

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

## Development Workflow

1. Start PostgreSQL (local or Docker)
2. Start Redis (optional - uses in-memory if not available)
3. Start backend: `uvicorn app.main:app --reload`
4. Start frontend: `npm run dev`
5. Access app: `http://localhost:5173`
6. API requests automatically proxied to backend
