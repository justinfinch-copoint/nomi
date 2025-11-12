# Implementation Patterns

**These patterns ensure consistent implementation across all AI agents. Every agent MUST follow these conventions to prevent conflicts.**

## NAMING PATTERNS

### REST API Endpoints
```
CONVENTION: Plural nouns, lowercase, hyphen-separated for multi-word
✅ /api/tasks
✅ /api/inspirations
✅ /api/auth/callback
❌ /api/task (singular)
❌ /api/Tasks (capitalized)
❌ /api/task_list (underscore)
```

### Database Tables & Columns
```
CONVENTION: Snake_case for tables and columns
✅ tasks, inspirations, users
✅ user_id, created_at, entraid_user_id
❌ Users, Tasks (PascalCase)
❌ userId, createdAt (camelCase)
```

### Python Files & Classes
```
CONVENTION:
- Files: snake_case
- Classes: PascalCase
- Functions/variables: snake_case

✅ task.py → class Task
✅ auth_service.py → class AuthService → def create_session()
❌ TaskModel.py, task-service.py
```

### TypeScript/React Files & Components
```
CONVENTION:
- Components: PascalCase files → PascalCase exports
- Services/utilities: camelCase files → camelCase exports
- Types: PascalCase

✅ TaskCard.tsx → export const TaskCard
✅ tasksService.ts → export const createTask
✅ task.ts → export type Task
❌ task-card.tsx, TasksService.ts
```

## STRUCTURE PATTERNS

### Backend Feature Slice Organization (Vertical Slice + REPR Pattern)
```python
# VERTICAL SLICE: Everything for a feature lives together
# REPR PATTERN: Each endpoint is a separate file with its own Request/Response

# app/features/tasks/ contains ALL task-related code
# ONE FILE PER ENDPOINT (true REPR pattern)

# =========================================
# app/features/tasks/create_task.py
# =========================================
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from app.features.auth.dependencies import get_current_user
from app.features.users.model import User
from .service import TaskService

# Request schema for THIS endpoint only
class CreateTaskRequest(BaseModel):
    """REPR Request: Create task"""
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=2000)

# Response schema for THIS endpoint only
class CreateTaskResponse(BaseModel):
    """REPR Response: Created task"""
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# REPR Endpoint: Create Task
@router.post("/", response_model=CreateTaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: CreateTaskRequest,
    current_user: User = Depends(get_current_user)
):
    """
    REPR: Create a new task
    Request: CreateTaskRequest (title, description)
    Response: CreateTaskResponse (full task object)
    """
    task = await TaskService.create_task(current_user.id, request)
    return task

# =========================================
# app/features/tasks/list_tasks.py
# =========================================
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from app.features.auth.dependencies import get_current_user
from app.features.users.model import User
from .service import TaskService

# Response schema (individual task)
class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Response schema for THIS endpoint
class ListTasksResponse(BaseModel):
    """REPR Response: List of tasks"""
    tasks: list[TaskResponse]

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# REPR Endpoint: List Tasks
@router.get("/", response_model=ListTasksResponse, status_code=status.HTTP_200_OK)
async def list_tasks(current_user: User = Depends(get_current_user)):
    """
    REPR: List all tasks for authenticated user
    Request: None (user from session)
    Response: ListTasksResponse
    """
    tasks = await TaskService.get_user_tasks(current_user.id)
    return ListTasksResponse(tasks=tasks)

# =========================================
# app/features/tasks/update_task.py
# =========================================
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from app.features.auth.dependencies import get_current_user
from app.features.users.model import User
from .service import TaskService

# Request schema for THIS endpoint
class UpdateTaskRequest(BaseModel):
    """REPR Request: Update task"""
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=2000)
    status: str | None = Field(None, pattern="^(todo|done)$")

# Response schema for THIS endpoint
class UpdateTaskResponse(BaseModel):
    """REPR Response: Updated task"""
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# REPR Endpoint: Update Task
@router.put("/{task_id}", response_model=UpdateTaskResponse, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: str,
    request: UpdateTaskRequest,
    current_user: User = Depends(get_current_user)
):
    """
    REPR: Update existing task
    Request: task_id + UpdateTaskRequest
    Response: UpdateTaskResponse
    """
    task = await TaskService.update_task(task_id, current_user.id, request)
    return task

# =========================================
# app/features/tasks/delete_task.py
# =========================================
from fastapi import APIRouter, Depends, status
from app.features.auth.dependencies import get_current_user
from app.features.users.model import User
from .service import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# REPR Endpoint: Delete Task (no request/response schemas needed)
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    REPR: Delete task by ID
    Request: task_id (path parameter)
    Response: 204 No Content
    """
    await TaskService.delete_task(task_id, current_user.id)

# =========================================
# app/features/tasks/model.py (SHARED across endpoints)
# =========================================
from sqlalchemy import Column, String, UUID, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(2000))
    status = Column(String(20), nullable=False, default="todo")
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

# =========================================
# app/features/tasks/service.py (SHARED business logic)
# =========================================
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .model import Task

class TaskService:
    @staticmethod
    async def get_user_tasks(user_id: UUID, db: AsyncSession):
        result = await db.execute(
            select(Task).where(Task.user_id == user_id).order_by(Task.updated_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def create_task(user_id: UUID, request, db: AsyncSession):
        task = Task(
            user_id=user_id,
            title=request.title,
            description=request.description,
            status="todo"
        )
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    # ... other service methods

# =========================================
# app/main.py - Collecting all endpoint routers
# =========================================
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Import individual endpoint routers (one per endpoint file)
# Auth endpoints
from app.features.auth.login import router as auth_login_router
from app.features.auth.callback import router as auth_callback_router
from app.features.auth.me import router as auth_me_router
from app.features.auth.logout import router as auth_logout_router

# Task endpoints
from app.features.tasks.create_task import router as task_create_router
from app.features.tasks.list_tasks import router as task_list_router
from app.features.tasks.get_task import router as task_get_router
from app.features.tasks.update_task import router as task_update_router
from app.features.tasks.delete_task import router as task_delete_router

# Inspiration endpoints
from app.features.inspirations.create_inspiration import router as inspiration_create_router
from app.features.inspirations.list_inspirations import router as inspiration_list_router
# ... other inspiration routers

app = FastAPI(title="Nomi API", version="1.0.0")

# Include all endpoint routers
app.include_router(auth_login_router)
app.include_router(auth_callback_router)
app.include_router(auth_me_router)
app.include_router(auth_logout_router)

app.include_router(task_create_router)
app.include_router(task_list_router)
app.include_router(task_get_router)
app.include_router(task_update_router)
app.include_router(task_delete_router)

app.include_router(inspiration_create_router)
app.include_router(inspiration_list_router)
# ... other inspiration routers

# Serve React static files (production)
app.mount("/", StaticFiles(directory="../nomi-frontend/dist", html=True), name="static")
```

**Key Points:**
- ✅ Each endpoint = One file
- ✅ Each file contains its own Request/Response schemas
- ✅ model.py and service.py are SHARED across endpoints
- ✅ main.py imports and includes all individual routers

### Frontend Component Organization
```typescript
// Pages in pages/ → route components
// Reusable UI in components/ → feature-organized

// pages/Tasks.tsx
export const Tasks = () => {
  const { tasks, fetchTasks } = useTasksStore();
  // Page-level logic
};

// components/tasks/TaskCard.tsx
export const TaskCard = ({ task }: { task: Task }) => {
  // Reusable task display
};
```

### Test File Organization
```
Backend tests (mirroring feature structure):
tests/
  features/
    test_auth.py          # Tests for features/auth/
    test_tasks.py         # Tests for features/tasks/
    test_inspirations.py  # Tests for features/inspirations/
  conftest.py             # Shared fixtures

Frontend tests (if added):
src/
  components/
    tasks/
      TaskCard.tsx
      TaskCard.test.tsx
```

### Vertical Slice Principles
```python
# PRINCIPLE 1: Feature independence
# Each feature slice is self-contained
✅ features/tasks/ has its own model, schemas, service, endpoints
✅ features/inspirations/ has its own model, schemas, service, endpoints

# PRINCIPLE 2: Shared infrastructure in core/
# Cross-cutting concerns live in core/
✅ core/database.py - Database connection
✅ core/security.py - Session validation
✅ core/config.py - Settings
❌ core/crud.py - NO generic CRUD (belongs in feature slices)

# PRINCIPLE 3: Allow intentional duplication
# Code duplication between slices is acceptable
✅ tasks/service.py and inspirations/service.py may have similar CRUD patterns
❌ Don't create shared base classes to eliminate duplication
Rationale: Slices evolve independently - premature abstraction creates coupling

# PRINCIPLE 4: Cross-slice dependencies when needed
# Slices can import from other slices for specific use cases
✅ inspirations/service.py can import tasks/service.py for convert_to_task()
⚠️ Keep these minimal - they create coupling
```

### REPR Pattern Principles (Request-Endpoint-Response)

```python
# REPR PATTERN: Each endpoint follows Request → Endpoint → Response

# PRINCIPLE 1: Explicit Request Schemas
# Every endpoint that accepts input has a dedicated Pydantic request model
✅ TaskCreateRequest - for POST /api/tasks
✅ TaskUpdateRequest - for PUT /api/tasks/{id}
❌ Generic dict or untyped parameters

# PRINCIPLE 2: Explicit Response Schemas
# Every endpoint has a dedicated Pydantic response model
✅ TaskResponse - for single task responses
✅ TaskListResponse - for list responses
❌ Returning raw ORM models without schema

# PRINCIPLE 3: Single Responsibility per Endpoint
# Each endpoint function does ONE thing
✅ create_task() - only creates tasks
✅ update_task() - only updates tasks
❌ update_or_create_task() - don't combine operations

# PRINCIPLE 4: Clear API Contracts
# Request/Response schemas serve as API documentation
✅ Pydantic Field() with descriptions
✅ json_schema_extra with examples
✅ Validation rules (min_length, max_length, pattern)
❌ Undocumented magic behavior

# PRINCIPLE 5: Status Code Clarity
# Every endpoint specifies its status code explicitly
✅ @router.post(..., status_code=status.HTTP_201_CREATED)
✅ @router.get(..., status_code=status.HTTP_200_OK)
✅ @router.delete(..., status_code=status.HTTP_204_NO_CONTENT)
❌ Relying on FastAPI defaults without being explicit
```

**REPR Benefits:**
1. **Clear Contracts**: Request/Response schemas document the API
2. **Type Safety**: Pydantic validates all inputs/outputs
3. **Auto-Generated Docs**: OpenAPI/Swagger documentation is complete
4. **Easy Testing**: Mock requests/responses with known schemas
5. **Single Responsibility**: Each endpoint has one job
6. **No Surprises**: Explicit schemas prevent unexpected behavior

**REPR File & Naming Convention:**
```python
# FILE NAMES: Descriptive, one per endpoint
create_task.py       # Contains: CreateTaskRequest, CreateTaskResponse
list_tasks.py        # Contains: ListTasksResponse (no request)
get_task.py          # Contains: GetTaskResponse
update_task.py       # Contains: UpdateTaskRequest, UpdateTaskResponse
delete_task.py       # Endpoint only (no schemas needed)

# SCHEMA NAMES: Match the endpoint operation
# In create_task.py:
class CreateTaskRequest(BaseModel):   # Request for THIS endpoint
    ...
class CreateTaskResponse(BaseModel):  # Response for THIS endpoint
    ...

# In list_tasks.py:
class TaskResponse(BaseModel):        # Individual task (reused in list)
    ...
class ListTasksResponse(BaseModel):   # Response for THIS endpoint
    tasks: list[TaskResponse]

# In update_task.py:
class UpdateTaskRequest(BaseModel):   # Request for THIS endpoint
    ...
class UpdateTaskResponse(BaseModel):  # Response for THIS endpoint
    ...

# PRINCIPLE: Each endpoint file is self-contained
# - Contains only schemas it needs
# - Small schema duplication is OK (e.g., TaskResponse repeated)
# - Makes endpoint easy to understand in isolation

# Rationale: Allows adding metadata later without breaking changes
# Future: tasks: list[TaskResponse], total: int, page: int
```

## FORMAT PATTERNS

### API Response Format
```json
SUCCESS (200/201):
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "Task title",
  "description": "Description",
  "status": "todo",
  "created_at": "2025-11-12T10:30:00Z",
  "updated_at": "2025-11-12T10:30:00Z"
}

ERROR (4xx/5xx):
{
  "detail": "Error message here"
}

// NO WRAPPER - FastAPI returns data directly
❌ { "data": {...}, "success": true }
❌ { "result": {...}, "error": null }
```

### Date/Time Format
```
CONVENTION: ISO 8601 strings in UTC

Backend (Pydantic):
created_at: datetime  # Serializes to ISO 8601

Frontend (TypeScript):
created_at: string  # ISO 8601 from API
display: formatDate(task.created_at)  // Helper function

✅ "2025-11-12T10:30:00Z"
❌ "11/12/2025"
❌ Unix timestamps
```

### Environment Variables
```
CONVENTION: SCREAMING_SNAKE_CASE

✅ DATABASE_URL
✅ ENTRAID_CLIENT_ID
✅ SESSION_SECRET_KEY
❌ databaseUrl, database-url
```

## COMMUNICATION PATTERNS

### Zustand Store Pattern
```typescript
// EVERY store follows this structure
type StoreState = {
  // Data
  items: Item[];
  loading: boolean;
  error: string | null;
};

type StoreActions = {
  // Actions
  fetchItems: () => Promise<void>;
  createItem: (data: ItemCreate) => Promise<void>;
  updateItem: (id: string, data: ItemUpdate) => Promise<void>;
  deleteItem: (id: string) => Promise<void>;
};

// Combine in create
export const useItemStore = create<StoreState & StoreActions>((set, get) => ({
  items: [],
  loading: false,
  error: null,

  fetchItems: async () => {
    set({ loading: true });
    try {
      const items = await itemService.getItems();
      set({ items, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },
  // ... other actions
}));
```

### FastAPI Dependency Pattern
```python
# EVERY protected endpoint uses this pattern
# get_current_user lives in auth feature slice

from app.features.auth.dependencies import get_current_user
from app.features.users.model import User

@router.get("/api/resource")
async def get_resource(
    current_user: User = Depends(get_current_user)
):
    # current_user is validated and populated from session
    # Automatic 401 if session invalid
    pass

# app/features/auth/dependencies.py
from fastapi import Depends, HTTPException, status, Request
from app.core.security import validate_session
from app.core.database import get_db
from app.features.users.model import User
from sqlalchemy.ext.asyncio import AsyncSession

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User:
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    user_data = await validate_session(session_id)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )

    # Fetch full user from database
    result = await db.execute(
        select(User).where(User.id == user_data["user_id"])
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
```

## CONSISTENCY PATTERNS

### Error Handling
```typescript
// Frontend: Always use try/catch in store actions
try {
  const response = await api.post('/api/tasks', data);
  set({ tasks: [...get().tasks, response] });
} catch (error) {
  set({ error: error.message });
  // Toast notification for user feedback
  toast.error('Failed to create task');
}
```

```python
# Backend: Use FastAPI's HTTPException
from fastapi import HTTPException, status

if not task:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )

if task.user_id != current_user.id:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to access this task"
    )
```

### User Data Isolation
```python
# EVERY query MUST filter by user_id from session

# ✅ Correct
tasks = await db.execute(
    select(Task).where(Task.user_id == current_user.id)
)

# ❌ WRONG - exposes all users' data
tasks = await db.execute(select(Task))
```

### Optimistic Updates
```typescript
// Create/Update/Delete: Update UI immediately, rollback on error

deleteTask: async (id: string) => {
  const previousTasks = get().tasks;

  // Optimistic update
  set({ tasks: previousTasks.filter(t => t.id !== id) });

  try {
    await taskService.deleteTask(id);
    toast.success('Task deleted');
  } catch (error) {
    // Rollback on error
    set({ tasks: previousTasks });
    toast.error('Failed to delete task');
  }
}
```
