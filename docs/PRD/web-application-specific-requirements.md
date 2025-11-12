# Web Application Specific Requirements

Nomi is a **Single-Page Application (SPA)** built with React + Vite, following modern web app patterns. These requirements shape the technical implementation and architectural decisions.

## Application Architecture Pattern

**SPA (Single-Page Application)**
- Client-side routing with React Router
- Dynamic content loading via API calls
- Single initial HTML load, subsequent navigation handled by JavaScript
- State managed client-side with Zustand
- Backend serves compiled static files + API endpoints

**Why SPA (not MPA):**
- Better demonstrates React patterns and Zustand state management
- Smoother user experience without full page reloads
- Clear separation between frontend state and backend API
- Modern standard for dashboard/tool applications
- Aligns with learning goals (client-side state management)

**Why not SSR/SSG:**
- Adds deployment complexity (Node.js server or build-time generation)
- Not required for authenticated application (no SEO needs)
- Focus remains on React + Python, not Next.js/Remix patterns
- Simpler mental model for learning

## Browser Support Matrix

**Target Browsers:**
- **Chrome/Edge:** Latest 2 versions (primary development browser)
- **Firefox:** Latest 2 versions
- **Safari:** Latest 2 versions

**Why modern browsers only:**
- Leverages modern JavaScript (ES6+) without transpilation complexity
- Supports modern CSS features (Grid, Flexbox, CSS variables)
- No legacy browser baggage (IE11, older Safari)
- Development efficiency - focus on patterns, not polyfills
- Realistic for internal tools / modern web apps

**Browser Features Required:**
- ES6+ JavaScript support
- Fetch API for HTTP requests
- LocalStorage for any client-side preferences
- Session cookies with secure, httpOnly, sameSite support
- Modern CSS (Grid, Flexbox, CSS Custom Properties)

## Responsive Design Requirements

**Design Approach:**
- **Desktop-first** with mobile responsive layouts
- Breakpoints: Desktop (1024px+), Tablet (768px-1023px), Mobile (320px-767px)
- Touch-friendly targets for mobile (min 44x44px touch areas)
- Responsive typography and spacing

**Why desktop-first:**
- Primary use case: focused work at a computer
- Learning project - not a mobile-first consumer app
- Simpler to build and test
- Mobile-responsive as quality bar, not primary experience

**Layout Patterns:**
- Responsive grid for task/inspiration lists
- Collapsible navigation for smaller screens
- Stack forms vertically on mobile
- No native mobile features (GPS, camera, push notifications)

## Performance Targets

**Page Load Performance:**
- **Initial load:** < 3 seconds (including auth redirect if needed)
- **Subsequent navigation:** < 500ms (client-side routing)
- **API response time:** < 1 second for typical CRUD operations
- **Time to interactive:** < 2 seconds after initial load

**Why these targets:**
- Reasonable for learning project, not over-optimized
- User experience remains snappy
- Achievable without complex performance engineering
- Realistic for internal tools / authenticated apps

**Performance Patterns to Implement:**
- Code splitting with React lazy loading (if app grows)
- Minimal bundle size (modern dependencies, tree-shaking)
- Efficient Zustand state updates (no unnecessary re-renders)
- Appropriate database indexes for common queries
- Session caching to reduce auth checks

## SEO Strategy

**SEO Requirements:** None

**Why no SEO:**
- Authenticated application (all content behind login)
- Not a public website or content platform
- Search engines can't index user-specific data
- Focus remains on application patterns, not marketing

**Meta tags included:**
- Basic HTML meta (title, viewport, charset)
- Favicon and app manifest for bookmarking
- No Open Graph, Twitter Cards, structured data

## Accessibility Requirements

**Target Level:** WCAG 2.1 Level A (Basic Compliance)

**Why Level A (not AA or AAA):**
- Learning project - demonstrates awareness, not enterprise accessibility
- Level A covers fundamental requirements (keyboard nav, alt text, color contrast basics)
- AA/AAA add complexity without additional architectural learning
- Can be enhanced post-MVP if accessibility patterns become a learning goal

**Minimum Accessibility Features:**
- **Keyboard navigation:** All interactive elements accessible via keyboard (Tab, Enter, Escape)
- **Semantic HTML:** Proper heading hierarchy, button vs div, form labels
- **ARIA labels:** Screen reader support for interactive elements
- **Focus management:** Visible focus indicators, logical tab order
- **Color contrast:** Text meets minimum contrast ratios
- **Form validation:** Clear error messages, accessible form feedback

**Accessibility Patterns:**
- Use semantic HTML elements (`<button>`, `<nav>`, `<main>`)
- Label all form inputs with `<label>` or `aria-label`
- Provide focus styles for keyboard navigation
- Announce dynamic content changes (form errors, success messages)
- Avoid color-only indicators (pair with icons/text)

## API Design (BFF Pattern)

**Endpoint Structure:**
```
/api/auth/login          → Initiate OAuth2 flow
/api/auth/callback       → Handle OAuth2 callback
/api/auth/me             → Get current user profile
/api/auth/logout         → Destroy session

/api/tasks               → GET (list), POST (create)
/api/tasks/{id}          → GET (read), PUT (update), DELETE (delete)

/api/inspirations        → GET (list), POST (create)
/api/inspirations/{id}   → GET (read), PUT (update), DELETE (delete)
/api/inspirations/{id}/convert → POST (convert to task)

/api/users/me            → GET (user profile and preferences)
```

**BFF Principles Applied:**
- Endpoints shaped for frontend needs (not generic CRUD)
- Backend aggregates data (user + tasks in one call if needed)
- Backend handles complex logic (auth, validation, business rules)
- Frontend receives ready-to-render data
- Response formats optimized for React state shape

**Request/Response Format:**
- JSON for all API communication
- Consistent error response format
- Pagination for list endpoints (if lists grow large)
- ISO 8601 dates for consistency

**Authentication Pattern:**
- Session cookie automatically included in all requests
- No Authorization header or client-side token management
- Backend validates session on every protected endpoint
- 401 Unauthorized triggers logout flow in frontend

## Deployment Architecture

**Single-Server Pattern:**

```
[Browser]
    ↓ HTTPS
[FastAPI Server]
    ├── / → React static files (Vite build)
    ├── /api/* → FastAPI endpoints
    ├── /auth/* → Auth endpoints
    └── Session Store (Redis/In-memory)
    ↓
[PostgreSQL Database]
```

**Benefits of Single-Server:**
- Same origin = no CORS configuration
- Cookies work seamlessly (no credentials config)
- Simpler deployment (one server, one domain)
- Reduced infrastructure complexity
- Development proxy mirrors production architecture

**Production Requirements:**
- HTTPS required (for secure cookies)
- Environment variables for secrets (EntraID client secret, database URL, session secret)
- PostgreSQL database (managed service or containerized)
- Redis for session storage (recommended for production)
- Static file serving from FastAPI (mounting Vite build)

**Development Environment:**
- Vite dev server (port 5173) with HMR
- Vite proxy forwards `/api/*` to FastAPI (port 8000)
- No CORS issues - proxy makes requests appear same-origin
- Full hot module reload while API calls work seamlessly
- PostgreSQL (local or Docker)
- In-memory session storage for development

## Technology Stack Confirmation

**Frontend:**
- React 18+ with Vite
- Zustand for state management
- React Router for client-side routing
- TypeScript (recommended for type safety)
- Styling: Modern CSS or Tailwind CSS

**Backend:**
- FastAPI (Python 3.10+)
- Pydantic for validation
- SQLAlchemy ORM with Alembic migrations
- MSAL Python for EntraID OAuth2
- authlib for OAuth2 flow handling
- Session management with signed cookies

**Database:**
- PostgreSQL (production-grade relational)

**Infrastructure:**
- Single-server deployment
- Redis for production session storage
- Environment-based configuration

---
