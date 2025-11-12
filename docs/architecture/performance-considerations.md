# Performance Considerations

## Database Performance

**Indexes on hot paths:**
```sql
-- User lookup by EntraID ID
CREATE INDEX idx_users_entraid_user_id ON users(entraid_user_id);

-- Task queries by user
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_updated_at ON tasks(updated_at DESC);

-- Combined index for filtered queries
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
```

**Query Optimization:**
- Use `select()` with specific columns instead of `SELECT *`
- Limit result sets (pagination if lists grow beyond 100 items)
- Avoid N+1 queries (use `joinedload()` if needed)

## Session Performance

**Redis for Production:**
- Sub-millisecond session lookups
- Automatic TTL expiration
- Connection pooling

**Caching Strategy:**
- Session validation cached in request context
- No need to re-validate within same request

## Frontend Performance

**Code Splitting:**
```typescript
// Lazy load routes
const Tasks = lazy(() => import('./pages/Tasks'));
const Inspirations = lazy(() => import('./pages/Inspirations'));
```

**Optimistic Updates:**
- Immediate UI feedback
- No waiting for API responses
- Better perceived performance

**Bundle Size:**
- Vite tree-shaking removes unused code
- Tailwind purges unused CSS
- Target: < 500KB gzipped JavaScript
