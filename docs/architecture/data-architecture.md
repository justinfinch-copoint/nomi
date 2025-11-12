# Data Architecture

## Database Schema

**Users Table**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entraid_user_id VARCHAR(255) UNIQUE NOT NULL,  -- 'sub' claim from ID token
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_entraid_user_id ON users(entraid_user_id);
```

**Tasks Table**
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'todo' CHECK (status IN ('todo', 'done')),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_updated_at ON tasks(updated_at DESC);
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
```

**Inspirations Table**
```sql
CREATE TABLE inspirations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    captured_date DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_inspirations_user_id ON inspirations(user_id);
CREATE INDEX idx_inspirations_captured_date ON inspirations(captured_date DESC);
```

## Entity Relationships

```
users (1) ────< (many) tasks
  │
  └──────────< (many) inspirations
```

**Key Constraints:**
- All entities belong to exactly one user
- Cascade delete: If user deleted, all tasks and inspirations deleted
- No cross-user references or sharing (single-tenant data model)

## Data Isolation Strategy

**Every query filters by user_id:**
```python
# SQLAlchemy pattern used throughout
async def get_user_tasks(user_id: UUID, db: AsyncSession):
    result = await db.execute(
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.updated_at.desc())
    )
    return result.scalars().all()
```

**Ownership validation before modifications:**
```python
task = await db.get(Task, task_id)
if not task or task.user_id != current_user.id:
    raise HTTPException(status_code=403, detail="Not authorized")
```
