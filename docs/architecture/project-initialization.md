# Project Initialization

**First Implementation Story** should execute these commands:

## Frontend Setup
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

## Backend Setup
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
