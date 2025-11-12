# Epic 2: Authentication & Session Management

**Epic Goal:** Implement maximum-security server-side OAuth2 authentication with EntraID, session-based API protection using HTTP-only signed cookies, and protected routes on both frontend and backend.

**Value:** This is THE crown jewel architectural pattern - demonstrating enterprise-grade authentication with zero token exposure to the browser. Complete immunity to XSS token theft.

---

## Story 2.1: Configure EntraID Application Registration

As a **developer**,
I want an EntraID (Azure AD) application registered and configured for OAuth2 authorization code flow,
So that I can authenticate users with Microsoft identity platform.

**Acceptance Criteria:**

**Given** I have access to Azure Portal
**When** I register a new application in EntraID
**Then** I have a client ID and client secret

**And** the redirect URI is set to `http://localhost:8000/api/auth/callback` (development)

**And** the application is configured for "Web" platform (not SPA)

**And** API permissions include: `openid`, `profile`, `email`

**And** I have documented the configuration steps for future deployments

**And** client ID and client secret are stored in environment variables (never committed to git)

**Prerequisites:** Story 1.1

**Technical Notes:**
- Azure Portal → App Registrations → New Registration
- Platform: Web (server-side OAuth2)
- Redirect URI will change for production deployment
- Client secret stored in `.env` file
- Document in `docs/SETUP.md` or similar
- Add production redirect URI when deploying

---

## Story 2.2: Implement OAuth2 Authorization Initiation (Login Redirect)

As a **user**,
I want to click "Sign in with Microsoft" and be redirected to EntraID login,
So that I can authenticate using my Microsoft account.

**Acceptance Criteria:**

**Given** I'm on the login page (unauthenticated)
**When** I click "Sign in with Microsoft" button
**Then** the frontend redirects to `/api/auth/login` endpoint

**And** the backend constructs an EntraID authorization URL with:
  - `client_id` (from environment)
  - `redirect_uri` (backend callback URL)
  - `scope` (openid, profile, email)
  - `state` (CSRF protection token - randomly generated and stored in session)
  - `response_type=code` (authorization code flow)

**And** the backend redirects my browser to the EntraID authorization URL

**And** I see the Microsoft login page

**Prerequisites:** Stories 1.1, 2.1

**Technical Notes:**
- Frontend: Button triggers `window.location.href = '/api/auth/login'`
- Backend: Use `authlib` or `msal` library to construct authorization URL
- Generate random `state` parameter and store in temporary session/cookie for CSRF validation
- EntraID authorization URL format: `https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?...`
- Use common tenant or specific tenant ID

---

## Story 2.3: Implement OAuth2 Token Exchange (Callback Handler)

As a **user returning from EntraID**,
I want the backend to exchange my authorization code for tokens,
So that my identity is verified and a session is created.

**Acceptance Criteria:**

**Given** I've authenticated with Microsoft
**When** EntraID redirects to `/api/auth/callback?code=...&state=...`
**Then** the backend validates the `state` parameter matches the stored CSRF token

**And** the backend uses MSAL Python to exchange the authorization code for tokens (access token + ID token)

**And** the backend validates the ID token signature using JWKS from Microsoft

**And** the backend extracts user profile from ID token claims:
  - `sub` (user ID)
  - `email`
  - `name`

**And** the ID token is successfully validated

**Prerequisites:** Story 2.2

**Technical Notes:**
- Use `msal.ConfidentialClientApplication` for token exchange
- Validate `state` parameter to prevent CSRF
- Verify ID token signature using Microsoft's JWKS endpoint
- Extract claims: `sub`, `email`, `name`, `preferred_username`
- Handle errors: invalid code, expired code, token validation failure
- Do NOT send tokens to frontend - keep them server-side only

---

## Story 2.4: Create Server-Side Session and Set HTTP-Only Cookie

As a **user with validated tokens**,
I want a server-side session created with an HTTP-only signed cookie,
So that I'm authenticated for subsequent API requests without exposing any tokens to the browser.

**Acceptance Criteria:**

**Given** the ID token is validated successfully
**When** the backend creates a session
**Then** a unique session ID is generated (UUID or secure random string)

**And** the session is stored in the session backend (Redis or in-memory) with:
  - session_id (key)
  - user_id (from ID token `sub` claim)
  - email, name (from ID token)
  - created_at, expires_at (24-hour TTL)

**And** an HTTP-only cookie is set with:
  - Name: `session_id`
  - Value: signed session ID (to prevent tampering)
  - HttpOnly: true (JavaScript cannot access)
  - Secure: true (HTTPS only in production)
  - SameSite: Lax (CSRF protection)
  - Max-Age: 86400 (24 hours)

**And** the backend redirects to the frontend home page (`/`)

**And** no tokens are ever sent to the browser

**Prerequisites:** Stories 1.4, 2.3

**Technical Notes:**
- Use session manager from Story 1.4
- Sign cookie value using secret key (prevents tampering)
- Use `itsdangerous` or FastAPI's built-in signing for cookie signature
- Session ID should be cryptographically random
- Store minimal data in session (user_id, email, name)
- Tokens remain server-side only (can be stored if needed for API calls, but not for MVP)

---

## Story 2.5: Create User Record in Database (First-Time Login)

As a **user logging in for the first time**,
I want a user record created in the database,
So that my tasks and inspirations can be associated with my account.

**Acceptance Criteria:**

**Given** the ID token is validated and session is being created
**When** the user_id (from `sub` claim) does not exist in the database
**Then** a new user record is created in the `users` table with:
  - `id` (UUID primary key)
  - `entraid_user_id` (from `sub` claim - unique index)
  - `email` (from ID token)
  - `name` (from ID token)
  - `created_at`, `updated_at` (timestamps)

**And** when the user_id already exists in the database
**Then** the existing user record is updated with latest email and name (in case they changed in EntraID)

**And** the database user ID is stored in the session for future requests

**Prerequisites:** Stories 1.2, 2.4

**Technical Notes:**
- Upsert logic: Check if `entraid_user_id` exists, create or update accordingly
- Use database user ID (not EntraID user ID) for foreign keys in tasks/inspirations
- Unique constraint on `entraid_user_id`
- Update `updated_at` timestamp on profile updates

---

## Story 2.6: Implement Session Validation Middleware for Protected API Endpoints

As a **backend service**,
I want all protected API endpoints to validate session cookies,
So that only authenticated users can access their data.

**Acceptance Criteria:**

**Given** a request is made to a protected endpoint (e.g., `/api/tasks`, `/api/inspirations`)
**When** the request includes a valid session cookie
**Then** the middleware validates the cookie signature

**And** the middleware retrieves the session from the session store using the session ID

**And** if the session is valid and not expired, the request proceeds with user context attached

**And** the user ID from the session is available to the endpoint handler

**And** if the session cookie is missing, invalid, or expired
**Then** the middleware returns 401 Unauthorized with JSON error: `{"detail": "Not authenticated"}`

**Prerequisites:** Story 2.4

**Technical Notes:**
- FastAPI dependency for session validation: `get_current_user()`
- Verify cookie signature to prevent tampering
- Check session expiry (TTL)
- Attach user object to request state for endpoint access
- Return 401 for missing/invalid/expired sessions
- Apply middleware to all `/api/*` routes except `/api/auth/*` and `/api/health`

---

## Story 2.7: Create /api/auth/me Endpoint to Retrieve User Profile

As a **frontend application**,
I want to call `/api/auth/me` to check authentication status and retrieve user profile,
So that I can display user information and determine if the user is logged in.

**Acceptance Criteria:**

**Given** I have a valid session cookie
**When** I call GET `/api/auth/me`
**Then** I receive a 200 OK response with JSON:
```json
{
  "authenticated": true,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

**And** if I don't have a valid session cookie
**Then** I receive a 401 Unauthorized response

**Prerequisites:** Story 2.6

**Technical Notes:**
- Protected endpoint using session validation middleware
- Returns user profile from session
- Frontend calls this on app initialization to check auth status
- Used by frontend to populate auth state in Zustand store

---

## Story 2.8: Implement Logout Functionality

As a **user**,
I want to log out and have my session destroyed,
So that I'm no longer authenticated and must log in again to access protected resources.

**Acceptance Criteria:**

**Given** I'm authenticated with a valid session
**When** I click the logout button
**Then** the frontend calls POST `/api/auth/logout`

**And** the backend deletes the session from the session store

**And** the backend clears the session cookie (sets empty value with immediate expiry)

**And** the backend returns 200 OK

**And** the frontend clears auth state from Zustand store

**And** the frontend redirects me to the landing page (`/`)

**And** I can no longer access protected API endpoints (401 Unauthorized)

**Prerequisites:** Stories 2.6, 2.7

**Technical Notes:**
- Backend deletes session from Redis/in-memory store
- Clear cookie: Set-Cookie with empty value, Max-Age=0
- Frontend clears Zustand auth store
- Redirect to landing page after logout

---

## Story 2.9: Implement Zustand Auth Store and Frontend Auth State Management

As a **frontend application**,
I want centralized auth state management with Zustand,
So that all components can access authentication status and user profile.

**Acceptance Criteria:**

**Given** the app initializes
**When** the React app loads
**Then** a Zustand auth store is initialized with state:
```typescript
{
  isAuthenticated: boolean,
  user: { id, email, name } | null,
  loading: boolean
}
```

**And** on app initialization, the store calls `/api/auth/me` to check auth status

**And** if the API returns user data, the store sets `isAuthenticated: true` and populates `user`

**And** if the API returns 401, the store sets `isAuthenticated: false` and `user: null`

**And** the store exposes actions: `login()`, `logout()`, `checkAuth()`

**And** components can access auth state using Zustand selectors

**Prerequisites:** Stories 1.5, 2.7

**Technical Notes:**
- Create `src/stores/authStore.ts`
- Use Zustand for state management
- Call `/api/auth/me` on app mount (in App.tsx or root component)
- Actions trigger API calls and update state
- Loading state for async operations

---

## Story 2.10: Implement Protected Route Guards in React Router

As a **frontend application**,
I want protected routes to redirect unauthenticated users to the login page,
So that authenticated-only pages are not accessible without login.

**Acceptance Criteria:**

**Given** I'm unauthenticated
**When** I attempt to navigate to a protected route (`/tasks`, `/inspirations`, `/profile`)
**Then** I'm redirected to `/login`

**And** given I'm authenticated
**When** I navigate to a protected route
**Then** I see the requested page

**And** given I'm on a protected page and my session expires
**When** the API returns 401 Unauthorized
**Then** the frontend clears auth state and redirects me to `/login`

**And** after logging in, I'm redirected to the originally requested route (or home if none)

**Prerequisites:** Stories 1.5, 2.9

**Technical Notes:**
- Create `ProtectedRoute` wrapper component
- Check `isAuthenticated` from Zustand auth store
- Redirect using React Router's `Navigate` component
- Store intended route in location state for post-login redirect
- API interceptor: Catch 401 responses globally, trigger logout + redirect

---

## Story 2.11: Implement Session Expiry Handling

As a **user with an expired session**,
I want to be gracefully logged out and redirected to login,
So that I understand my session has expired and can log in again.

**Acceptance Criteria:**

**Given** my session has expired (24 hours of inactivity)
**When** I make any API request
**Then** the backend returns 401 Unauthorized

**And** the frontend intercepts the 401 response

**And** the frontend displays a toast notification: "Your session has expired. Please log in again."

**And** the frontend clears auth state from Zustand store

**And** the frontend redirects me to `/login`

**And** I can log in again successfully

**Prerequisites:** Stories 2.6, 2.9, 2.10

**Technical Notes:**
- Session TTL enforced in session store (24 hours)
- Global API error interceptor in frontend
- Use toast notification library (react-hot-toast or similar)
- Clear auth state before redirect
- Store intended route for post-login redirect

---
