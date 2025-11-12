# Technology Stack Details

## Backend Stack

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

## Frontend Stack

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

## Integration Points

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
