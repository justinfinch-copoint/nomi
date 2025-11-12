# User Experience Principles

Nomi's UX is **intentionally simple and functional** - designed to support architectural learning, not to be a design portfolio piece. The interface should be clean, predictable, and immediately understandable.

## Design Philosophy

**"Invisible UX"**

The UI should get out of the way and let the architecture shine:
- Clean, minimal interface with clear information hierarchy
- Standard UI patterns users already know (no novel interactions to learn)
- Functional over flashy - clarity over creativity
- Responsive state changes make Zustand patterns visible
- Forms and interactions demonstrate proper error handling

**The UX serves the architecture:**
- Loading states show async patterns working
- Error messages demonstrate proper error handling
- Instant updates prove state management efficiency
- Smooth navigation shows client-side routing
- Protected content demonstrates auth working

## Visual Personality

**Clean & Professional**
- Modern but not trendy (won't look dated in 2 years)
- Spacious layouts with breathing room
- Neutral color palette with purposeful accents
- Consistent typography hierarchy
- Subtle shadows and borders for depth

**Think:** Google Keep, Linear, or Notion - clean productivity tools, not creative playgrounds.

## Color Palette Approach

**Minimal color strategy:**
- **Primary:** Single accent color for CTAs and active states (blue, green, or purple)
- **Neutral grays:** Text, backgrounds, borders (light mode default)
- **Semantic colors:** Green (success), Red (error/delete), Yellow (warning)
- **No gradients or illustrations** - solid colors only

**Why minimal:**
- Faster development - no color system complexity
- Focus remains on functionality
- Professional appearance without design effort
- Easy to theme later if desired

## Key Interaction Patterns

**Standard Web Patterns - No Surprises:**

**Navigation:**
- Top nav bar or sidebar with clear sections (Tasks, Inspirations, Profile)
- Active state clearly indicated
- Logout button always accessible
- Client-side routing with no full page reloads

**Forms:**
- Standard form layouts with labels above inputs
- Inline validation with clear error messages
- Submit buttons disabled during processing
- Success feedback after successful creation/update
- Cancel/close options always available

**Lists (Tasks/Inspirations):**
- Card-based or simple list layout
- Hover states on interactive elements
- Click to edit or expand details
- Action buttons visible on hover or always visible (mobile)
- Empty states with helpful messaging ("No tasks yet - create your first one!")

**Modals/Dialogs:**
- Edit/create forms in modals or inline
- Confirmation dialogs for destructive actions (delete)
- Dismiss with X button, Cancel button, or ESC key
- Focus trapped within modal while open

**Loading States:**
- Skeleton screens or spinners during data fetching
- Disabled buttons during form submission
- Loading indicator for initial page load
- Optimistic updates where appropriate (add task → show immediately, update in background)

**Error Handling:**
- Toast notifications for success/error messages
- Inline form validation errors
- Graceful degradation if API call fails
- Retry options for failed operations

## Critical User Flows

**1. First-Time User Experience (Post-Auth)**

```
User completes EntraID auth → Redirected to app
↓
Lands on dashboard/home
↓
Sees welcome message + empty state
↓
Clear CTA: "Create your first task"
↓
Clicks CTA → Modal/form opens
↓
Fills form → Submits
↓
Success message + task appears in list
```

**Goal:** User creates first task within 30 seconds of landing.

**2. Daily Task Management Flow**

```
User arrives at app
↓
Sees list of tasks with clear status (todo/done)
↓
Scans list → Clicks task to view/edit OR marks done
↓
Done tasks move to completed section or fade
↓
Add new task via prominent button
↓
Filter to see only active tasks
```

**Goal:** Common operations (view, add, complete) require < 2 clicks.

**3. Inspiration → Task Conversion**

```
User captures inspiration
↓
Later browses inspirations list
↓
Finds one worth acting on
↓
Clicks "Convert to Task" or similar action
↓
Pre-filled task form opens with inspiration details
↓
User edits/confirms → Task created
↓
Inspiration marked as converted or archived
```

**Goal:** Demonstrate cross-entity operations smoothly.

**4. Session Expiry / Logout**

```
User's session expires OR clicks logout
↓
Immediately redirected to login/landing page
↓
No error state, no stuck pages
↓
Can log back in seamlessly
```

**Goal:** Auth state changes handled gracefully.

## Layout Structure

**Main Layout Components:**

```
┌────────────────────────────────────────┐
│  [Header: Logo | Nav | Profile/Logout] │
├────────────────────────────────────────┤
│                                        │
│  [Main Content Area]                   │
│                                        │
│  - Dashboard / Task List / Form        │
│  - Responsive grid or single column    │
│                                        │
│                                        │
└────────────────────────────────────────┘
```

**Responsive Behavior:**
- **Desktop (1024px+):** Sidebar nav + content area OR top nav + full width content
- **Tablet (768px-1023px):** Collapsible sidebar or top nav, full-width content
- **Mobile (320px-767px):** Top nav with hamburger menu, stacked content, full-width forms

## UI Component Patterns

**Reusable components to build:**
- Button (primary, secondary, danger variants)
- Input field (text, textarea)
- Card (for tasks/inspirations)
- Modal/Dialog
- Toast notification
- Loading spinner
- Empty state

**Why component focus:**
- Demonstrates React component patterns
- Promotes code reuse
- Consistent UX throughout app
- Easy to maintain and extend

## Typography & Spacing

**Simple system:**
- **Headings:** 1-2 font sizes (H1 for page titles, H2 for sections)
- **Body:** Single readable size (16px base)
- **Small:** For metadata/timestamps
- **Font:** System font stack (no custom fonts to load)

**Spacing scale:**
- Use consistent spacing units (4px, 8px, 16px, 24px, 32px)
- Generous padding in cards and forms
- Clear visual separation between sections

## What NOT to Include

**Avoid complexity that doesn't teach architecture:**
- ❌ Custom illustrations or iconography (use simple text or emoji)
- ❌ Animations beyond basic transitions
- ❌ Dark mode toggle (can be post-MVP if learning CSS variables)
- ❌ Advanced interactions (drag-and-drop, gesture controls)
- ❌ Custom design system or component library
- ❌ Sophisticated data visualization

**Keep it simple - the UX exists to make the architecture usable, not to win design awards.**

---
