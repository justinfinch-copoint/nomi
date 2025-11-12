# Functional Requirements

These requirements transform the architectural learning goals into specific, implementable features. Each requirement is organized by capability area and includes clear acceptance criteria.

## 1. Authentication & Authorization

**Primary architectural learning goal: Master server-side OAuth2 with maximum security session management.**

### FR-AUTH-001: EntraID OAuth2 Authentication
**Requirement:** Users must authenticate using Microsoft EntraID (Azure AD) via OAuth2 authorization code flow, with all token handling performed server-side.

**Acceptance Criteria:**
- User clicks "Sign in with Microsoft" button on landing page
- Backend redirects user to EntraID authorization URL with appropriate parameters (client_id, redirect_uri, scope, state)
- User authenticates with Microsoft (enters credentials, completes MFA if required)
- EntraID redirects to backend `/api/auth/callback` with authorization code
- Backend exchanges authorization code for access token and ID token using MSAL Python
- Backend validates ID token signature and claims
- Backend creates server-side session with user profile information
- Backend stores session in Redis (production) or in-memory (development)
- Backend sets HTTP-only, Secure, SameSite=Lax cookie with session ID
- Backend redirects user to frontend application home page
- Frontend calls `/api/auth/me` to retrieve user profile and authentication status
- User is now authenticated and can access protected resources

**Technical Details:**
- OAuth2 flow: Authorization Code Flow (not implicit or client credentials)
- Tokens never exposed to browser (stored server-side only)
- Session cookie: HTTP-only, Secure (HTTPS only), SameSite=Lax, signed
- MSAL Python library for token exchange
- authlib for OAuth2 flow management

### FR-AUTH-002: Session-Based API Authentication
**Requirement:** All API requests to protected endpoints must validate session cookie to ensure user is authenticated.

**Acceptance Criteria:**
- Every request to `/api/tasks`, `/api/inspirations`, `/api/users/me` includes session cookie automatically
- Backend middleware validates session cookie signature
- Backend retrieves session from store (Redis/memory)
- If session valid: Request proceeds with user context available
- If session invalid/missing: Backend returns 401 Unauthorized
- Frontend intercepts 401 responses and redirects to login page

**Technical Details:**
- Session validation middleware on all protected routes
- User ID extracted from session and attached to request context
- No bearer tokens, no authorization headers - cookies only

### FR-AUTH-003: Protected Routes (Frontend)
**Requirement:** Frontend must protect authenticated-only routes and redirect unauthenticated users to login.

**Acceptance Criteria:**
- Routes requiring authentication: `/tasks`, `/inspirations`, `/profile`
- Public routes: `/`, `/login`, `/auth/callback`
- Zustand auth store tracks authentication state (isAuthenticated, user profile)
- React Router guards check authentication state before rendering protected routes
- Unauthenticated users attempting to access protected routes are redirected to login
- After successful login, users are redirected to originally requested route (or home)

**Technical Details:**
- React Router with protected route wrapper component
- Auth state managed in Zustand store
- Initial app load calls `/api/auth/me` to check session status

### FR-AUTH-004: User Profile Management
**Requirement:** System must retrieve and display authenticated user's profile information from EntraID.

**Acceptance Criteria:**
- User profile retrieved from ID token claims during authentication
- Profile includes: name, email, user ID (sub claim)
- Profile stored in session (server-side)
- Frontend can retrieve profile via `/api/auth/me` endpoint
- Profile displayed in UI (header, profile page)
- Profile information read-only (sourced from EntraID, not editable in app)

### FR-AUTH-005: Logout Functionality
**Requirement:** Users must be able to log out, destroying their session and clearing authentication state.

**Acceptance Criteria:**
- Logout button accessible from all authenticated pages (header/nav)
- Clicking logout calls `/api/auth/logout` endpoint
- Backend destroys session in store (Redis/memory)
- Backend clears session cookie (sets empty value with immediate expiry)
- Frontend clears auth state in Zustand store
- User redirected to landing/login page
- Attempting to access protected routes after logout requires re-authentication

### FR-AUTH-006: Session Expiry Handling
**Requirement:** Sessions must expire after period of inactivity, with graceful handling in UI.

**Acceptance Criteria:**
- Sessions expire after 24 hours of inactivity (configurable)
- API returns 401 Unauthorized when session expired
- Frontend intercepts 401 and redirects to login
- User sees message: "Your session has expired. Please log in again."
- After re-authentication, user can continue using app

## 2. Task Management

**Architectural learning goal: Demonstrate REST API design, CRUD operations, user-specific data isolation, and Zustand state management.**

### FR-TASK-001: Create Task
**Requirement:** Authenticated users must be able to create new tasks with title, description, and default status.

**Acceptance Criteria:**
- User clicks "Add Task" button
- Task creation form appears (modal or inline)
- Form fields: Title (required, max 200 chars), Description (optional, max 2000 chars)
- Form validates: Title required, character limits enforced
- Submit button disabled while submitting
- On submit: POST to `/api/tasks` with task data
- Backend creates task with: user_id (from session), title, description, status="todo", timestamps
- Backend returns created task with generated ID
- Frontend adds task to Zustand store
- Task immediately appears in list (optimistic update)
- Success toast notification: "Task created"
- Form closes/resets

**Technical Details:**
- Database: Tasks table with columns (id, user_id, title, description, status, created_at, updated_at)
- User_id foreign key ensures tasks belong to specific user
- Backend validates user owns resource on all operations

### FR-TASK-002: List Tasks
**Requirement:** Users must be able to view all their tasks in a list view.

**Acceptance Criteria:**
- On app load (authenticated): GET `/api/tasks` retrieves all user's tasks
- Backend filters tasks by user_id from session (user only sees own tasks)
- Tasks returned as JSON array with all fields
- Frontend stores tasks in Zustand store
- Tasks displayed in list/card view with: title, status, created date
- Empty state displayed if no tasks: "No tasks yet - create your first one!"
- List updates in real-time when tasks added/modified/deleted

**Technical Details:**
- Default sort: Most recently updated first
- Pagination not required for MVP (assume < 100 tasks)
- Backend query: `SELECT * FROM tasks WHERE user_id = ? ORDER BY updated_at DESC`

### FR-TASK-003: Update Task
**Requirement:** Users must be able to edit task title, description, and status.

**Acceptance Criteria:**
- User clicks task to open edit view (modal or inline form)
- Form pre-populated with current values
- User can modify: title, description, status (todo/done)
- Validation same as create: title required, character limits
- On submit: PUT to `/api/tasks/{id}` with updated data
- Backend validates: user owns task (user_id matches session)
- Backend updates task, sets updated_at timestamp
- Backend returns updated task
- Frontend updates task in Zustand store
- UI reflects changes immediately
- Success toast: "Task updated"

### FR-TASK-004: Update Task Status (Quick Action)
**Requirement:** Users must be able to quickly mark tasks as done/todo without opening full edit form.

**Acceptance Criteria:**
- Checkbox or toggle button visible on each task in list
- Clicking checkbox: PUT to `/api/tasks/{id}` with only status field
- Task status toggles between "todo" and "done"
- UI updates immediately (optimistic)
- Done tasks visually differentiated (strikethrough, faded, or moved to separate section)
- No confirmation required (quick action)

**Technical Details:**
- Partial update endpoint: Only updates status field
- Alternative: Use same update endpoint but frontend only sends changed fields

### FR-TASK-005: Delete Task
**Requirement:** Users must be able to permanently delete tasks.

**Acceptance Criteria:**
- Delete button visible on task (trash icon)
- Clicking delete shows confirmation dialog: "Delete this task? This cannot be undone."
- User confirms or cancels
- On confirm: DELETE to `/api/tasks/{id}`
- Backend validates: user owns task
- Backend hard deletes task from database
- Frontend removes task from Zustand store
- Task disappears from list immediately
- Success toast: "Task deleted"

**Technical Details:**
- Hard delete (no soft delete for MVP)
- Cascade delete if task has relationships (future: comments, attachments)

## 3. Inspiration Management

**Architectural learning goal: Prove patterns work for multiple entity types, demonstrate cross-entity operations.**

### FR-INSP-001: Create Inspiration
**Requirement:** Users must be able to capture inspirations with title and description.

**Acceptance Criteria:**
- User clicks "Add Inspiration" button
- Inspiration form appears (modal or inline)
- Form fields: Title (required, max 200 chars), Description (optional, max 2000 chars)
- Form validation: Title required, character limits enforced
- On submit: POST to `/api/inspirations` with data
- Backend creates inspiration with: user_id, title, description, captured_date (auto), timestamps
- Backend returns created inspiration
- Frontend adds to Zustand store
- Inspiration appears in list immediately
- Success toast: "Inspiration captured"

**Technical Details:**
- Database: Inspirations table (id, user_id, title, description, captured_date, created_at, updated_at)
- Similar structure to tasks but separate entity
- No status field (inspirations don't have todo/done states)

### FR-INSP-002: List Inspirations
**Requirement:** Users must be able to view all their inspirations.

**Acceptance Criteria:**
- GET `/api/inspirations` retrieves all user's inspirations
- Backend filters by user_id from session
- Inspirations returned as JSON array
- Frontend stores in Zustand store (separate from tasks)
- Displayed in list/card view with: title, captured date
- Empty state: "No inspirations yet - capture your first idea!"
- List updates when inspirations added/modified/deleted

### FR-INSP-003: Update Inspiration
**Requirement:** Users must be able to edit inspiration title and description.

**Acceptance Criteria:**
- User clicks inspiration to open edit view
- Form pre-populated with current values
- User modifies title and/or description
- On submit: PUT to `/api/inspirations/{id}`
- Backend validates user ownership
- Backend updates inspiration, sets updated_at
- Frontend updates Zustand store
- UI reflects changes immediately
- Success toast: "Inspiration updated"

### FR-INSP-004: Delete Inspiration
**Requirement:** Users must be able to delete inspirations.

**Acceptance Criteria:**
- Delete button visible on inspiration
- Confirmation dialog: "Delete this inspiration?"
- On confirm: DELETE to `/api/inspirations/{id}`
- Backend validates ownership and deletes
- Frontend removes from store
- UI updates immediately
- Success toast: "Inspiration deleted"

### FR-INSP-005: Convert Inspiration to Task
**Requirement:** Users must be able to convert an inspiration into a task, demonstrating cross-entity operations.

**Acceptance Criteria:**
- "Convert to Task" button visible on each inspiration
- Clicking button: POST to `/api/inspirations/{id}/convert`
- Backend creates new task with: title and description copied from inspiration
- Backend marks inspiration as converted (add converted_to_task_id field, or delete inspiration)
- Backend returns created task
- Frontend adds task to tasks store
- Frontend updates or removes inspiration from inspirations store
- User sees success message with link to new task
- Optional: Navigate to task view automatically

**Technical Details:**
- Decision needed: Delete inspiration after conversion OR mark as converted and keep
- Recommendation: Mark as converted (add converted_to_task_id field) for MVP - allows tracking inspiration source

## 4. Organization & Filtering

**Architectural learning goal: Demonstrate client-side state management for UI concerns, filtering patterns.**

### FR-FILT-001: Filter by Entity Type
**Requirement:** Users must be able to switch between viewing tasks and inspirations.

**Acceptance Criteria:**
- Navigation or tabs for "Tasks" and "Inspirations"
- Clicking "Tasks" shows tasks list (filters out inspirations)
- Clicking "Inspirations" shows inspirations list (filters out tasks)
- Active view clearly indicated
- Client-side routing: `/tasks` and `/inspirations` routes
- Filter state managed in Zustand (or component state)

**Technical Details:**
- Separate pages/routes for tasks and inspirations (simplest approach)
- Alternative: Single page with filter toggle

### FR-FILT-002: Filter Tasks by Status
**Requirement:** Users must be able to filter tasks to show only active (todo) or completed (done) tasks.

**Acceptance Criteria:**
- Filter options visible on tasks page: "All", "Active", "Completed"
- Clicking filter updates displayed tasks
- Filter applied client-side (no API call)
- Task count displayed for each filter option
- Filter state persisted while navigating within app (Zustand store)
- Default filter: "All" (shows both todo and done)

**Technical Details:**
- Client-side filtering in Zustand selector or component
- Example: `tasks.filter(task => filterState === 'active' ? task.status === 'todo' : filterState === 'completed' ? task.status === 'done' : true)`

### FR-FILT-003: Sort Tasks and Inspirations
**Requirement:** Users must be able to sort items by date.

**Acceptance Criteria:**
- Sort options: "Newest first" (default), "Oldest first"
- Sort selector visible on list pages
- Clicking sort option re-orders list immediately
- Sort applied client-side
- Sort preference persisted in Zustand store

**Technical Details:**
- Sort by created_at or updated_at
- Client-side sort for MVP (backend sort if pagination added later)

## 5. User Profile

**Architectural learning goal: Display user context, demonstrate read-only data from identity provider.**

### FR-PROF-001: View User Profile
**Requirement:** Users must be able to view their profile information.

**Acceptance Criteria:**
- Profile page accessible via navigation or user menu
- Profile displays: Name, Email, User ID (from EntraID)
- Profile information read-only (cannot edit - sourced from EntraID)
- Note displayed: "Profile information is managed by your Microsoft account"
- Logout button available on profile page

**Technical Details:**
- Data retrieved from `/api/auth/me` endpoint
- No database storage needed (profile in session)
- Optional: Store user in database for referential integrity (tasks.user_id references users.id)

## Summary of Functional Requirements

**Total Requirements:** 21 functional requirements across 5 capability areas

**Architectural Patterns Demonstrated:**
- ✅ Server-side OAuth2 authorization code flow (FR-AUTH-001)
- ✅ Session-based authentication with HTTP-only cookies (FR-AUTH-002)
- ✅ Protected routes (frontend and backend) (FR-AUTH-003)
- ✅ REST API design with proper methods (FR-TASK-*, FR-INSP-*)
- ✅ User-specific data isolation (all entity operations)
- ✅ CRUD operations for multiple entities (tasks, inspirations)
- ✅ Zustand state management (all entity lists and auth state)
- ✅ Cross-entity operations (FR-INSP-005 conversion)
- ✅ Client-side filtering and sorting (FR-FILT-*)
- ✅ Optimistic UI updates (FR-TASK-001, FR-TASK-004)
- ✅ Error handling and validation (all create/update operations)

**Every requirement serves the architectural learning goals - no feature bloat, just patterns you'll reuse.**

---
