# Epic 3: Task Management

**Epic Goal:** Deliver complete task CRUD functionality with user-specific data isolation, demonstrating REST API design, database relationships, Zustand state management, and optimistic UI updates.

**Value:** First full entity implementation proving the complete stack works end-to-end. High user value. Foundation for understanding all patterns.

---

## Story 3.1: Create Tasks Database Schema and Model

As a **developer**,
I want a tasks table with proper schema and SQLAlchemy model,
So that I can store user-specific tasks with all required properties.

**Acceptance Criteria:**

**Given** the database is initialized
**When** I run Alembic migrations
**Then** a `tasks` table is created with columns:
  - `id` (UUID, primary key)
  - `user_id` (UUID, foreign key to users.id, not null)
  - `title` (VARCHAR(200), not null)
  - `description` (TEXT, nullable)
  - `status` (VARCHAR(20), default 'todo', values: 'todo', 'done')
  - `created_at` (TIMESTAMP, not null)
  - `updated_at` (TIMESTAMP, not null)

**And** a foreign key constraint ensures `user_id` references `users.id`

**And** an index is created on `user_id` for efficient queries

**And** an index is created on `updated_at` for sorting

**And** an SQLAlchemy model class `Task` is defined with proper relationships

**Prerequisites:** Story 1.2, Story 2.5 (users table exists)

**Technical Notes:**
- Alembic migration: `alembic revision --autogenerate -m "Add tasks table"`
- Foreign key with cascade delete (if user deleted, delete tasks - for future)
- SQLAlchemy model in `backend/app/models/task.py`
- Relationship: `user = relationship("User", back_populates="tasks")`
- Use UUID for IDs

---

## Story 3.2: Create Task Pydantic Schemas for API Validation

As a **developer**,
I want Pydantic schemas for task creation, updates, and responses,
So that API requests and responses are validated and type-safe.

**Acceptance Criteria:**

**Given** I'm building the tasks API
**When** I define Pydantic schemas
**Then** I have the following schemas:
  - `TaskCreate`: title (required, max 200 chars), description (optional, max 2000 chars)
  - `TaskUpdate`: title (optional, max 200 chars), description (optional, max 2000 chars), status (optional, 'todo' or 'done')
  - `TaskResponse`: id, user_id, title, description, status, created_at, updated_at

**And** validation errors return 422 Unprocessable Entity with clear error messages

**And** character limits are enforced

**And** status field only accepts 'todo' or 'done'

**Prerequisites:** Story 3.1

**Technical Notes:**
- Pydantic schemas in `backend/app/schemas/task.py`
- Use Field validators for max length
- Enum for status field
- Response schema includes all fields for frontend consumption

---

## Story 3.3: Implement POST /api/tasks (Create Task)

As a **user**,
I want to create a new task,
So that I can track things I need to do.

**Acceptance Criteria:**

**Given** I'm authenticated
**When** I POST to `/api/tasks` with JSON body:
```json
{
  "title": "My new task",
  "description": "Task details"
}
```
**Then** a new task is created in the database with:
  - My user_id (from session)
  - Provided title and description
  - Default status: 'todo'
  - Generated id, created_at, updated_at

**And** the API returns 201 Created with the complete task object

**And** if title is missing or exceeds 200 chars, I receive 422 Unprocessable Entity

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 3.1, 3.2

**Technical Notes:**
- Protected endpoint requiring session validation
- Extract user_id from session
- Use TaskCreate schema for validation
- Return TaskResponse schema
- Handle database errors gracefully

---

## Story 3.4: Implement GET /api/tasks (List All User's Tasks)

As a **user**,
I want to retrieve all my tasks,
So that I can see what I need to do.

**Acceptance Criteria:**

**Given** I'm authenticated and have tasks in the database
**When** I GET `/api/tasks`
**Then** I receive 200 OK with JSON array of all my tasks

**And** tasks are filtered by my user_id (I only see my own tasks)

**And** tasks are sorted by `updated_at` descending (most recently updated first)

**And** each task includes: id, title, description, status, created_at, updated_at

**And** if I have no tasks, I receive an empty array `[]`

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 3.1, 3.2

**Technical Notes:**
- Protected endpoint
- Query: `SELECT * FROM tasks WHERE user_id = ? ORDER BY updated_at DESC`
- Return list of TaskResponse schemas
- SQLAlchemy query with filter and order_by

---

## Story 3.5: Implement GET /api/tasks/{id} (Read Single Task)

As a **user**,
I want to retrieve a specific task by ID,
So that I can view its details.

**Acceptance Criteria:**

**Given** I'm authenticated and a task with the given ID exists
**When** I GET `/api/tasks/{id}`
**Then** I receive 200 OK with the task object

**And** the task belongs to me (user_id matches my session)

**And** if the task ID doesn't exist, I receive 404 Not Found

**And** if the task exists but belongs to another user, I receive 403 Forbidden

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 3.1, 3.2

**Technical Notes:**
- Protected endpoint
- Validate ownership: task.user_id == session.user_id
- Return 403 if user doesn't own the task
- Use TaskResponse schema

---

## Story 3.6: Implement PUT /api/tasks/{id} (Update Task)

As a **user**,
I want to update a task's title, description, or status,
So that I can modify task details or mark it as done.

**Acceptance Criteria:**

**Given** I'm authenticated and own a task
**When** I PUT to `/api/tasks/{id}` with JSON body:
```json
{
  "title": "Updated title",
  "status": "done"
}
```
**Then** the task is updated with the provided fields

**And** the `updated_at` timestamp is set to the current time

**And** the API returns 200 OK with the updated task object

**And** if the task doesn't exist, I receive 404 Not Found

**And** if the task belongs to another user, I receive 403 Forbidden

**And** if validation fails (title too long, invalid status), I receive 422 Unprocessable Entity

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 3.1, 3.2

**Technical Notes:**
- Protected endpoint
- Validate ownership before update
- Use TaskUpdate schema (all fields optional)
- Only update provided fields (partial update)
- Update `updated_at` timestamp
- Return TaskResponse schema

---

## Story 3.7: Implement DELETE /api/tasks/{id} (Delete Task)

As a **user**,
I want to delete a task permanently,
So that I can remove tasks I no longer need.

**Acceptance Criteria:**

**Given** I'm authenticated and own a task
**When** I DELETE `/api/tasks/{id}`
**Then** the task is permanently deleted from the database

**And** the API returns 204 No Content

**And** if the task doesn't exist, I receive 404 Not Found

**And** if the task belongs to another user, I receive 403 Forbidden

**And** if I'm not authenticated, I receive 401 Unauthorized

**Prerequisites:** Stories 2.6, 3.1, 3.2

**Technical Notes:**
- Protected endpoint
- Validate ownership before deletion
- Hard delete (no soft delete for MVP)
- Return 204 No Content on success

---

## Story 3.8: Create Zustand Tasks Store for State Management

As a **frontend application**,
I want a Zustand store to manage tasks state,
So that task data is centralized and components stay in sync.

**Acceptance Criteria:**

**Given** the frontend needs to manage tasks
**When** the tasks store is initialized
**Then** it contains state:
```typescript
{
  tasks: Task[],
  loading: boolean,
  error: string | null
}
```

**And** it exposes actions:
  - `fetchTasks()` - calls GET /api/tasks and updates state
  - `createTask(data)` - calls POST /api/tasks and adds to state
  - `updateTask(id, data)` - calls PUT /api/tasks/{id} and updates state
  - `deleteTask(id)` - calls DELETE /api/tasks/{id} and removes from state

**And** actions handle loading and error states

**And** components can subscribe to tasks using selectors

**Prerequisites:** Story 1.5 (Zustand configured)

**Technical Notes:**
- Create `src/stores/tasksStore.ts`
- Use Zustand for state management
- Actions call API and update state optimistically (add before API confirms)
- Error handling with try/catch
- Loading state for async operations

---

## Story 3.9: Build Task List UI Component

As a **user**,
I want to see all my tasks in a list view,
So that I can quickly scan what I need to do.

**Acceptance Criteria:**

**Given** I'm on the `/tasks` page
**When** the page loads
**Then** tasks are fetched from the API and displayed in a list

**And** each task shows: title, status (todo/done indicator), created date

**And** if I have no tasks, I see an empty state: "No tasks yet - create your first one!"

**And** tasks are sorted by most recently updated first

**And** I see a loading indicator while tasks are being fetched

**And** if an error occurs, I see an error message

**Prerequisites:** Stories 3.4, 3.8

**Technical Notes:**
- React component: `TaskList.tsx`
- Use Zustand tasks store to access state
- Call `fetchTasks()` on component mount
- Map over tasks array to render task cards
- Visual differentiation for done tasks (strikethrough, faded, or checkmark)
- Loading skeleton or spinner

---

## Story 3.10: Build Task Creation Form

As a **user**,
I want to create a new task via a form,
So that I can add items to my task list.

**Acceptance Criteria:**

**Given** I'm on the `/tasks` page
**When** I click "Add Task" button
**Then** a task creation form appears (modal or inline)

**And** the form has fields:
  - Title (required, max 200 chars)
  - Description (optional, textarea, max 2000 chars)

**And** the form validates: Title is required, character limits enforced

**And** when I submit the form
**Then** the task is created via POST /api/tasks

**And** the new task appears in the list immediately (optimistic update)

**And** the form closes/resets

**And** I see a success toast notification: "Task created"

**And** if validation fails, I see inline error messages

**And** the submit button is disabled while submitting

**Prerequisites:** Stories 3.3, 3.8

**Technical Notes:**
- React component: `TaskCreateForm.tsx`
- Modal component or inline form
- Form validation (required fields, max length)
- Call `createTask()` from Zustand store
- Optimistic update: Add to list before API confirms
- Toast notification library (react-hot-toast or similar)
- Disable button during submission

---

## Story 3.11: Build Task Edit Form

As a **user**,
I want to edit a task's title, description, or status,
So that I can modify task details.

**Acceptance Criteria:**

**Given** I'm viewing a task in the list
**When** I click the task or an "Edit" button
**Then** an edit form appears with fields pre-populated:
  - Title (current value)
  - Description (current value)
  - Status (dropdown: todo/done)

**And** I can modify any field

**And** when I submit the form
**Then** the task is updated via PUT /api/tasks/{id}

**And** the task updates in the list immediately (optimistic update)

**And** the form closes

**And** I see a success toast: "Task updated"

**And** if validation fails, I see inline error messages

**And** I can cancel without saving

**Prerequisites:** Stories 3.6, 3.8

**Technical Notes:**
- React component: `TaskEditForm.tsx`
- Reuse or extend TaskCreateForm component
- Pre-populate form with current task values
- Call `updateTask(id, data)` from Zustand store
- Optimistic update
- Cancel button closes form without API call

---

## Story 3.12: Build Quick Status Toggle for Tasks

As a **user**,
I want to quickly mark tasks as done or todo without opening the edit form,
So that I can efficiently update task status.

**Acceptance Criteria:**

**Given** I'm viewing my task list
**When** I click a checkbox next to a task
**Then** the task status toggles between 'todo' and 'done'

**And** the task is updated via PUT /api/tasks/{id}

**And** the UI updates immediately (optimistic)

**And** done tasks are visually differentiated (strikethrough, faded, checkmark icon)

**And** no confirmation is required (quick action)

**Prerequisites:** Stories 3.6, 3.8, 3.9

**Technical Notes:**
- Checkbox or toggle button on each task card
- OnClick handler calls `updateTask(id, { status: newStatus })`
- Optimistic UI update
- Visual styles for done vs todo tasks
- No loading indicator for this quick action

---

## Story 3.13: Build Task Delete Functionality with Confirmation

As a **user**,
I want to delete tasks with a confirmation dialog,
So that I can remove tasks I no longer need without accidental deletion.

**Acceptance Criteria:**

**Given** I'm viewing a task in the list
**When** I click a "Delete" button (trash icon)
**Then** a confirmation dialog appears: "Delete this task? This cannot be undone."

**And** I can confirm or cancel

**And** when I confirm
**Then** the task is deleted via DELETE /api/tasks/{id}

**And** the task is removed from the list immediately (optimistic)

**And** I see a success toast: "Task deleted"

**And** when I cancel, the dialog closes with no action

**Prerequisites:** Stories 3.7, 3.8, 3.9

**Technical Notes:**
- Delete button (trash icon) on each task card
- Confirmation modal/dialog component
- Call `deleteTask(id)` from Zustand store
- Optimistic removal from list
- Toast notification on success

---
