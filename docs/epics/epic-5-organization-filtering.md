# Epic 5: Organization & Filtering

**Epic Goal:** Enhance UX with client-side filtering and sorting patterns, demonstrating how to manage UI state without additional API calls and how to provide responsive user experience through frontend-only operations.

**Value:** Improves usability significantly by helping users focus on what matters. Demonstrates client-side state management patterns (Zustand selectors, computed state) without backend complexity.

---

## Story 5.1: Implement Client-Side Task Status Filter

As a **user**,
I want to filter my tasks to show only active or completed items,
So that I can focus on what I need to do or review what I've accomplished.

**Acceptance Criteria:**

**Given** I'm on the `/tasks` page with tasks loaded
**When** I see filter options: "All", "Active", "Completed"
**Then** clicking "All" shows all tasks (both todo and done)

**And** clicking "Active" shows only tasks with status='todo'

**And** clicking "Completed" shows only tasks with status='done'

**And** the filter is applied client-side (no API call)

**And** the active filter is visually highlighted

**And** task count is displayed for each filter option (e.g., "Active (5)")

**And** the filter state persists while I navigate away and return to tasks page

**Prerequisites:** Stories 3.4, 3.8, 3.9 (tasks loaded in store)

**Technical Notes:**
- Add `statusFilter` to tasks Zustand store state: 'all' | 'active' | 'completed'
- Create selector that filters tasks based on statusFilter
- Filter buttons component above task list
- Computed counts: `tasks.filter(t => t.status === 'todo').length`
- No API calls - pure frontend filtering
- Default filter: 'all'

---

## Story 5.2: Implement Client-Side Sort for Tasks

As a **user**,
I want to sort my tasks by date,
So that I can see newest or oldest tasks first.

**Acceptance Criteria:**

**Given** I'm on the `/tasks` page with tasks loaded
**When** I see sort options: "Newest first", "Oldest first"
**Then** clicking "Newest first" sorts tasks by `updated_at` descending

**And** clicking "Oldest first" sorts tasks by `updated_at` ascending

**And** the sort is applied client-side (no API call)

**And** the active sort option is visually indicated

**And** the sort preference persists while I navigate away and return

**And** sort works in combination with status filter

**Prerequisites:** Stories 3.4, 3.8, 3.9, 5.1

**Technical Notes:**
- Add `sortOrder` to tasks Zustand store state: 'newest' | 'oldest'
- Create selector that sorts filtered tasks based on sortOrder
- Sort dropdown or toggle buttons
- Sort by `updated_at` field (could also support `created_at`)
- Chain filters: filter by status first, then sort
- Default sort: 'newest'

---

## Story 5.3: Implement Client-Side Sort for Inspirations

As a **user**,
I want to sort my inspirations by date,
So that I can see newest or oldest inspirations first.

**Acceptance Criteria:**

**Given** I'm on the `/inspirations` page with inspirations loaded
**When** I see sort options: "Newest first", "Oldest first"
**Then** clicking "Newest first" sorts inspirations by `captured_date` descending

**And** clicking "Oldest first" sorts inspirations by `captured_date` ascending

**And** the sort is applied client-side (no API call)

**And** the active sort option is visually indicated

**And** the sort preference persists while I navigate away and return

**Prerequisites:** Stories 4.4, 4.8, 4.9

**Technical Notes:**
- Add `sortOrder` to inspirations Zustand store state: 'newest' | 'oldest'
- Create selector that sorts inspirations based on sortOrder
- Sort dropdown or toggle buttons (reuse component from tasks if possible)
- Sort by `captured_date` field
- Default sort: 'newest'

---

## Story 5.4: Add Task and Inspiration Counts to Navigation

As a **user**,
I want to see how many tasks and inspirations I have in the navigation,
So that I have quick visibility into my content at a glance.

**Acceptance Criteria:**

**Given** I'm authenticated and viewing the app
**When** I look at the navigation menu
**Then** I see "Tasks (5)" showing my total task count

**And** I see "Inspirations (3)" showing my total inspiration count

**And** counts update in real-time when I create, delete, or convert items

**And** counts are computed from Zustand stores (no additional API calls)

**Prerequisites:** Stories 3.8, 4.8

**Technical Notes:**
- Read counts from Zustand stores: `tasks.length`, `inspirations.length`
- Use Zustand selectors to subscribe to count changes
- Display in navigation component
- Counts update automatically via store reactivity
- Consider showing active task count vs total: "Tasks (3/10 active)"

---
