# Decision Summary

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
