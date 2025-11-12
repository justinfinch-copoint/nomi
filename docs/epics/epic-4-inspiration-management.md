# Epic 4: Inspiration Management

**Epic Goal:** Validate architectural patterns across multiple entity types with cross-entity operations, demonstrating that the task management patterns are reusable and that entities can interact (inspiration → task conversion).

**Value:** Second full entity implementation proving pattern reusability. The cross-entity conversion (FR-INSP-005) demonstrates that the architecture supports complex operations between different data models. Lower user value than tasks, but critical for architectural validation.

---

## Story 4.1: Create Inspirations Database Schema and Model

As a **developer**,
I want an inspirations table with proper schema and SQLAlchemy model,
So that I can store user-specific inspirations with all required properties.

**Acceptance Criteria:**

**Given** the database is initialized
**When** I run Alembic migrations
**Then** an `inspirations` table is created with columns:
  - `id` (UUID, primary key)
  - `user_id` (UUID, foreign key to users.id, not null)
  - `title` (VARCHAR(200), not null)
  - `description` (TEXT, nullable)
  - `captured_date` (DATE, not null, default current date)
  - `created_at` (TIMESTAMP, not null)
  - `updated_at` (TIMESTAMP, not null)

**And** a foreign key constraint ensures `user_id` references `users.id`

**And** an index is created on `user_id` for efficient queries

**And** an index is created on `captured_date` for sorting

**And** an SQLAlchemy model class `Inspiration` is defined with proper relationships

**Prerequisites:** Story 1.2 (database infrastructure), Story 2.5 (users table exists)

**Technical Notes:**
- Alembic migration: `alembic revision --autogenerate -m "Add inspirations table"`
- Foreign key with cascade delete (if user deleted, delete inspirations)
- SQLAlchemy model in `backend/app/models/inspiration.py`
- Relationship: `user = relationship("User", back_populates="inspirations")`
- No status field (unlike tasks - inspirations don't have todo/done states)
- captured_date automatically set to current date on creation

---

## Story 4.2: Create Inspiration Pydantic Schemas for API Validation

As a **developer**,
I want Pydantic schemas for inspiration creation, updates, and responses,
So that API requests and responses are validated and type-safe.

**Acceptance Criteria:**

**Given** I'm building the inspirations API
**When** I define Pydantic schemas
**Then** I have the following schemas:
  - `InspirationCreate`: title (required, max 200 chars), description (optional, max 2000 chars)
  - `InspirationUpdate`: title (optional, max 200 chars), description (optional, max 2000 chars)
  - `InspirationResponse`: id, user_id, title, description, captured_date, created_at, updated_at

**And** validation errors return 422 Unprocessable Entity with clear error messages

**And** character limits are enforced

**Prerequisites:** Story 4.1

**Technical Notes:**
- Pydantic schemas in `backend/app/schemas/inspiration.py`
- Use Field validators for max length
- Response schema includes all fields for frontend consumption
- captured_date is read-only (auto-generated on backend)

---

## Story 4.3: Implement POST /api/inspirations (Create Inspiration)

As a **user**,
I want to capture a new inspiration,
So that I can save ideas and thoughts for later.

**Acceptance Criteria:**

**Given** I'm authenticated
**When** I POST to `/api/inspirations` with JSON body:
```json
{
  "title": "My brilliant idea",
  "description": "Details about the idea"
}
```
**Then** a new inspiration is created in the database with:
  - My user_id (from session)
  - Provided title and description
  - captured_date set to current date
  - Generated id, created_at, updated_at

**And** the API returns 201 Created with the complete inspiration object

**And** if title is missing or exceeds 200 chars, I receive 422 Unprocessable Entity

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6 (auth middleware), 4.1, 4.2

**Technical Notes:**
- Protected endpoint requiring session validation
- Extract user_id from session
- Use InspirationCreate schema for validation
- Return InspirationResponse schema
- Auto-set captured_date to current date
- Handle database errors gracefully

---

## Story 4.4: Implement GET /api/inspirations (List All User's Inspirations)

As a **user**,
I want to retrieve all my inspirations,
So that I can review my captured ideas.

**Acceptance Criteria:**

**Given** I'm authenticated and have inspirations in the database
**When** I GET `/api/inspirations`
**Then** I receive 200 OK with JSON array of all my inspirations

**And** inspirations are filtered by my user_id (I only see my own inspirations)

**And** inspirations are sorted by `captured_date` descending (most recently captured first)

**And** each inspiration includes: id, title, description, captured_date, created_at, updated_at

**And** if I have no inspirations, I receive an empty array `[]`

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 4.1, 4.2

**Technical Notes:**
- Protected endpoint
- Query: `SELECT * FROM inspirations WHERE user_id = ? ORDER BY captured_date DESC`
- Return list of InspirationResponse schemas
- SQLAlchemy query with filter and order_by

---

## Story 4.5: Implement GET /api/inspirations/{id} (Read Single Inspiration)

As a **user**,
I want to retrieve a specific inspiration by ID,
So that I can view its details.

**Acceptance Criteria:**

**Given** I'm authenticated and an inspiration with the given ID exists
**When** I GET `/api/inspirations/{id}`
**Then** I receive 200 OK with the inspiration object

**And** the inspiration belongs to me (user_id matches my session)

**And** if the inspiration ID doesn't exist, I receive 404 Not Found

**And** if the inspiration exists but belongs to another user, I receive 403 Forbidden

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 4.1, 4.2

**Technical Notes:**
- Protected endpoint
- Validate ownership: inspiration.user_id == session.user_id
- Return 403 if user doesn't own the inspiration
- Use InspirationResponse schema

---

## Story 4.6: Implement PUT /api/inspirations/{id} (Update Inspiration)

As a **user**,
I want to update an inspiration's title or description,
So that I can refine my captured ideas.

**Acceptance Criteria:**

**Given** I'm authenticated and own an inspiration
**When** I PUT to `/api/inspirations/{id}` with JSON body:
```json
{
  "title": "Updated idea",
  "description": "Refined details"
}
```
**Then** the inspiration is updated with the provided fields

**And** the `updated_at` timestamp is set to the current time

**And** the `captured_date` remains unchanged (not modifiable)

**And** the API returns 200 OK with the updated inspiration object

**And** if the inspiration doesn't exist, I receive 404 Not Found

**And** if the inspiration belongs to another user, I receive 403 Forbidden

**And** if validation fails (title too long), I receive 422 Unprocessable Entity

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 4.1, 4.2

**Technical Notes:**
- Protected endpoint
- Validate ownership before update
- Use InspirationUpdate schema (all fields optional)
- Only update provided fields (partial update)
- Update `updated_at` timestamp
- Do NOT allow updating captured_date
- Return InspirationResponse schema

---

## Story 4.7: Implement DELETE /api/inspirations/{id} (Delete Inspiration)

As a **user**,
I want to delete an inspiration permanently,
So that I can remove ideas I no longer need.

**Acceptance Criteria:**

**Given** I'm authenticated and own an inspiration
**When** I DELETE `/api/inspirations/{id}`
**Then** the inspiration is permanently deleted from the database

**And** the API returns 204 No Content

**And** if the inspiration doesn't exist, I receive 404 Not Found

**And** if the inspiration belongs to another user, I receive 403 Forbidden

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 4.1, 4.2

**Technical Notes:**
- Protected endpoint
- Validate ownership before deletion
- Hard delete (no soft delete for MVP)
- Return 204 No Content on success

---

## Story 4.8: Create Zustand Inspirations Store for State Management

As a **frontend application**,
I want a Zustand store to manage inspirations state,
So that inspiration data is centralized and components stay in sync.

**Acceptance Criteria:**

**Given** the frontend needs to manage inspirations
**When** the inspirations store is initialized
**Then** it contains state:
```typescript
{
  inspirations: Inspiration[],
  loading: boolean,
  error: string | null
}
```

**And** it exposes actions:
  - `fetchInspirations()` - calls GET /api/inspirations and updates state
  - `createInspiration(data)` - calls POST /api/inspirations and adds to state
  - `updateInspiration(id, data)` - calls PUT /api/inspirations/{id} and updates state
  - `deleteInspiration(id)` - calls DELETE /api/inspirations/{id} and removes from state

**And** actions handle loading and error states

**And** components can subscribe to inspirations using selectors

**Prerequisites:** Story 1.5 (Zustand configured)

**Technical Notes:**
- Create `src/stores/inspirationsStore.ts`
- Use Zustand for state management (pattern reuse from tasks store)
- Actions call API and update state optimistically
- Error handling with try/catch
- Loading state for async operations
- Separate store from tasks (different entity)

---

## Story 4.9: Build Inspiration List UI Component

As a **user**,
I want to see all my inspirations in a list view,
So that I can quickly browse my captured ideas.

**Acceptance Criteria:**

**Given** I'm on the `/inspirations` page
**When** the page loads
**Then** inspirations are fetched from the API and displayed in a list

**And** each inspiration shows: title, captured date

**And** if I have no inspirations, I see an empty state: "No inspirations yet - capture your first idea!"

**And** inspirations are sorted by most recently captured first

**And** I see a loading indicator while inspirations are being fetched

**And** if an error occurs, I see an error message

**Prerequisites:** Stories 4.4, 4.8

**Technical Notes:**
- React component: `InspirationList.tsx`
- Use Zustand inspirations store to access state
- Call `fetchInspirations()` on component mount
- Map over inspirations array to render inspiration cards
- Loading skeleton or spinner
- Empty state design

---

## Story 4.10: Build Inspiration Creation Form

As a **user**,
I want to create a new inspiration via a form,
So that I can capture ideas as they come to me.

**Acceptance Criteria:**

**Given** I'm on the `/inspirations` page
**When** I click "Capture Inspiration" button
**Then** an inspiration creation form appears (modal or inline)

**And** the form has fields:
  - Title (required, max 200 chars)
  - Description (optional, textarea, max 2000 chars)

**And** the form validates: Title is required, character limits enforced

**And** when I submit the form
**Then** the inspiration is created via POST /api/inspirations

**And** the new inspiration appears in the list immediately (optimistic update)

**And** the form closes/resets

**And** I see a success toast notification: "Inspiration captured"

**And** if validation fails, I see inline error messages

**And** the submit button is disabled while submitting

**Prerequisites:** Stories 4.3, 4.8

**Technical Notes:**
- React component: `InspirationCreateForm.tsx`
- Modal component or inline form
- Form validation (required fields, max length)
- Call `createInspiration()` from Zustand store
- Optimistic update: Add to list before API confirms
- Toast notification library (reuse from tasks)
- Disable button during submission
- captured_date is auto-generated on backend (not in form)

---

## Story 4.11: Build Inspiration Edit Form

As a **user**,
I want to edit an inspiration's title and description,
So that I can refine my captured ideas.

**Acceptance Criteria:**

**Given** I'm viewing an inspiration in the list
**When** I click the inspiration or an "Edit" button
**Then** an edit form appears with fields pre-populated:
  - Title (current value)
  - Description (current value)

**And** I can modify any field

**And** when I submit the form
**Then** the inspiration is updated via PUT /api/inspirations/{id}

**And** the inspiration updates in the list immediately (optimistic update)

**And** the form closes

**And** I see a success toast: "Inspiration updated"

**And** if validation fails, I see inline error messages

**And** I can cancel without saving

**Prerequisites:** Stories 4.6, 4.8

**Technical Notes:**
- React component: `InspirationEditForm.tsx`
- Reuse or extend InspirationCreateForm component
- Pre-populate form with current inspiration values
- Call `updateInspiration(id, data)` from Zustand store
- Optimistic update
- Cancel button closes form without API call
- captured_date is read-only (not editable)

---

## Story 4.12: Build Inspiration Delete Functionality with Confirmation

As a **user**,
I want to delete inspirations with a confirmation dialog,
So that I can remove ideas I no longer need without accidental deletion.

**Acceptance Criteria:**

**Given** I'm viewing an inspiration in the list
**When** I click a "Delete" button (trash icon)
**Then** a confirmation dialog appears: "Delete this inspiration? This cannot be undone."

**And** I can confirm or cancel

**And** when I confirm
**Then** the inspiration is deleted via DELETE /api/inspirations/{id}

**And** the inspiration is removed from the list immediately (optimistic)

**And** I see a success toast: "Inspiration deleted"

**And** when I cancel, the dialog closes with no action

**Prerequisites:** Stories 4.7, 4.8, 4.9

**Technical Notes:**
- Delete button (trash icon) on each inspiration card
- Confirmation modal/dialog component (reuse from tasks)
- Call `deleteInspiration(id)` from Zustand store
- Optimistic removal from list
- Toast notification on success

---

## Story 4.13: Implement POST /api/inspirations/{id}/convert (Convert Inspiration to Task)

As a **user**,
I want to convert an inspiration into a task,
So that I can act on my ideas by turning them into actionable work items.

**Acceptance Criteria:**

**Given** I'm authenticated and own an inspiration
**When** I POST to `/api/inspirations/{id}/convert`
**Then** the backend creates a new task with:
  - title copied from inspiration
  - description copied from inspiration
  - status set to 'todo'
  - user_id from session

**And** the backend deletes the original inspiration (decision: delete after conversion for MVP simplicity)

**And** the backend returns 201 Created with the created task object

**And** if the inspiration doesn't exist, I receive 404 Not Found

**And** if the inspiration belongs to another user, I receive 403 Forbidden

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 3.1 (tasks table), 4.1, 4.2

**Technical Notes:**
- Protected endpoint
- Validate ownership before conversion
- Create transaction: Create task → Delete inspiration (atomic operation)
- Copy title and description from inspiration to task
- Set default task status to 'todo'
- Return task object (TaskResponse schema)
- Rollback transaction if either operation fails
- MVP decision: Delete inspiration after conversion (simpler than marking as converted)

---

## Story 4.14: Build "Convert to Task" UI Feature

As a **user**,
I want a "Convert to Task" button on each inspiration,
So that I can easily turn ideas into actionable tasks.

**Acceptance Criteria:**

**Given** I'm viewing my inspirations list
**When** I see a "Convert to Task" button on each inspiration
**Then** clicking the button calls POST /api/inspirations/{id}/convert

**And** the inspiration is removed from the inspirations store

**And** the new task is added to the tasks store

**And** I see a success toast: "Inspiration converted to task"

**And** the inspiration disappears from the inspirations list

**And** optional: I'm offered a link to view the new task or navigate to tasks page

**Prerequisites:** Stories 3.8 (tasks store), 4.8 (inspirations store), 4.9, 4.13

**Technical Notes:**
- "Convert to Task" button on each inspiration card
- Call conversion endpoint
- Update both stores: Remove from inspirations, add to tasks
- Toast notification with optional link to tasks page
- Consider confirmation dialog: "Convert this inspiration to a task?"
- Handle errors gracefully (show error toast if conversion fails)
- Optimistic UI update

---
