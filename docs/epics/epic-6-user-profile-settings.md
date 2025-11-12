# Epic 6: User Profile & Settings

**Epic Goal:** Display user context from identity provider, demonstrating how to present read-only data sourced from external authentication systems and provide account management features.

**Value:** Gives users visibility into their account info and provides essential logout functionality. Demonstrates working with identity provider data (read-only profile from EntraID).

---

## Story 6.1: Create Profile Page UI

As a **user**,
I want to view my profile information,
So that I can see my account details and verify my identity.

**Acceptance Criteria:**

**Given** I'm authenticated
**When** I navigate to `/profile`
**Then** I see a profile page displaying:
  - My name (from EntraID)
  - My email address (from EntraID)
  - Account type indicator: "Microsoft Account"

**And** all fields are read-only (no edit functionality)

**And** a note is displayed: "Profile information is managed by your Microsoft account"

**And** a "Logout" button is prominently displayed

**And** the page has a clean, professional layout

**Prerequisites:** Stories 2.7 (auth/me endpoint), 2.9 (auth store)

**Technical Notes:**
- React component: `Profile.tsx`
- Read user data from Zustand auth store
- Display fields as read-only text (not form inputs)
- Professional styling with clear information hierarchy
- Logout button calls logout action from auth store
- Route: `/profile` (protected route)

---

## Story 6.2: Add Profile Link to Navigation

As a **user**,
I want quick access to my profile from the navigation,
So that I can easily view my account details or log out.

**Acceptance Criteria:**

**Given** I'm authenticated
**When** I look at the navigation header
**Then** I see a profile link or user menu

**And** clicking it navigates to `/profile` or opens a dropdown with:
  - "Profile" link → navigates to `/profile`
  - "Logout" button → logs me out

**And** my name or email is displayed in the user menu trigger

**And** the user menu is visually distinct from main navigation

**Prerequisites:** Stories 2.9, 6.1

**Technical Notes:**
- User menu component in header
- Display user name from auth store
- Dropdown menu or direct link to profile
- Include logout action in dropdown for quick access
- Consider user avatar/initials icon
- Responsive design (mobile: hamburger menu or bottom nav)

---

## Story 6.3: Add Activity Summary to Profile Page

As a **user**,
I want to see summary statistics on my profile page,
So that I can quickly understand my usage of the application.

**Acceptance Criteria:**

**Given** I'm on the `/profile` page
**When** the page loads
**Then** I see summary cards displaying:
  - Total tasks count
  - Active tasks count (status='todo')
  - Completed tasks count (status='done')
  - Total inspirations count

**And** counts are computed from Zustand stores (no additional API calls)

**And** counts update in real-time if I create/delete items in another tab

**Prerequisites:** Stories 3.8, 4.8, 6.1

**Technical Notes:**
- Read from tasks and inspirations Zustand stores
- Computed values: filter tasks by status for counts
- Display as summary cards or statistics grid
- Use Zustand selectors for reactivity
- Simple, clear visualization (numbers + labels)
- Optional: Add date joined (user.created_at from database)

---
