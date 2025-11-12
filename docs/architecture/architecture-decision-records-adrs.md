# Architecture Decision Records (ADRs)

## ADR-001: Server-Side OAuth2 with HTTP-Only Cookies

**Context:** Need maximum-security authentication pattern for enterprise applications.

**Decision:** Use server-side OAuth2 authorization code flow with EntraID, storing sessions in HTTP-only signed cookies.

**Alternatives Considered:**
- Client-side MSAL.js with tokens in localStorage ❌ Vulnerable to XSS
- JWT in localStorage ❌ Token theft via XSS
- JWT in memory only ❌ Lost on page refresh

**Consequences:**
- ✅ Complete immunity to XSS token theft
- ✅ Browser cannot access tokens
- ✅ CSRF protected with SameSite cookies
- ⚠️ Requires session storage (Redis)
- ⚠️ Cannot call Microsoft Graph from frontend (backend proxy needed)

**Rationale:** This is THE crown jewel pattern - demonstrates enterprise-grade security worth copying.

## ADR-002: Single-Server Deployment Pattern

**Context:** Need simplified deployment while remaining production-viable.

**Decision:** FastAPI serves both React static files and API endpoints from same origin.

**Alternatives Considered:**
- Separate frontend (Vercel) + backend (AWS) ❌ CORS complexity
- Nginx reverse proxy ❌ Additional infrastructure
- API Gateway ❌ Over-engineering

**Consequences:**
- ✅ No CORS configuration needed
- ✅ Cookies work seamlessly (same origin)
- ✅ Simplified deployment (one server)
- ✅ Development proxy mirrors production
- ⚠️ Couples frontend/backend deployment

**Rationale:** Eliminates common deployment headaches while teaching clean patterns.

## ADR-003: Zustand Over Redux/Context API

**Context:** Need state management that's simple to learn but powerful enough for real apps.

**Decision:** Use Zustand for all client state management.

**Alternatives Considered:**
- Redux Toolkit ❌ Too much boilerplate for learning project
- Context API ❌ Performance issues, re-render problems
- Jotai/Recoil ❌ Atomic state adds complexity

**Consequences:**
- ✅ Minimal boilerplate (no actions/reducers)
- ✅ Excellent TypeScript support
- ✅ Simple mental model (just a hook)
- ✅ Good performance (selective subscriptions)
- ⚠️ Less structure than Redux (requires discipline)

**Rationale:** Best balance of simplicity and power for intermediate developers.

## ADR-004: PostgreSQL with SQLAlchemy 2.0 Async

**Context:** Need production-grade database with modern async patterns.

**Decision:** PostgreSQL with SQLAlchemy 2.0 async ORM and Alembic migrations.

**Alternatives Considered:**
- MongoDB ❌ Relational data fits better
- Prisma ❌ TypeScript-focused, not Python
- Django ORM ❌ Tied to Django framework

**Consequences:**
- ✅ ACID compliance for data integrity
- ✅ Excellent JSON support (JSONB)
- ✅ Mature ecosystem
- ✅ Modern async/await syntax
- ✅ Type-safe queries
- ⚠️ Requires understanding of async SQLAlchemy

**Rationale:** Industry-standard relational DB with modern Python async support.

## ADR-005: Vertical Slice Architecture (Feature-First Organization)

**Context:** Need backend architecture that maximizes maintainability, makes features easy to understand, and reduces coupling while serving as a learning reference.

**Decision:** Organize backend using Vertical Slice Architecture with feature-first structure (`features/tasks/`, `features/auth/`, etc.) instead of traditional layered architecture (`api/`, `models/`, `services/`, `schemas/`).

**Alternatives Considered:**
- **Layered Architecture** ❌ Feature code scattered across multiple directories, high cognitive load
- **Monolithic Single-File** ❌ Doesn't scale, hard to navigate
- **Microservices** ❌ Over-engineering for this scale, deployment complexity

**Vertical Slice Structure:**
```
features/
  tasks/
    endpoints.py   # FastAPI routes
    model.py       # SQLAlchemy model
    schemas.py     # Pydantic schemas
    service.py     # Business logic
  inspirations/
    endpoints.py
    model.py
    schemas.py
    service.py
```

**Key Principles:**
1. **High Cohesion Within Slices**: Everything for "tasks" lives in `features/tasks/`
2. **Low Coupling Between Slices**: Changes to tasks don't affect inspirations
3. **Intentional Duplication**: Similar CRUD patterns duplicated across slices (not shared)
4. **Cross-Cutting in Core**: Only infrastructure concerns (`database.py`, `security.py`, `config.py`)

**Consequences:**
- ✅ **Easy Navigation**: "Where's the task creation logic?" → `features/tasks/service.py`
- ✅ **Localized Changes**: New task field? Only touch `features/tasks/`
- ✅ **Parallel Development**: Multiple devs/agents can work on different features simultaneously
- ✅ **Better Learning**: Clear boundaries, easy to understand one feature at a time
- ✅ **Reduced Cognitive Load**: Don't need to understand whole system to change one feature
- ⚠️ **Code Duplication**: CRUD patterns repeated (this is intentional - slices evolve independently)
- ⚠️ **Discipline Required**: Must resist premature abstraction to shared base classes

**Comparison to Layered Architecture:**

| Aspect | Layered (api/, models/, services/) | Vertical Slice (features/) |
|--------|-----------------------------------|---------------------------|
| Add task filter | Touch: api/tasks.py, services/task_service.py, schemas/task.py | Touch: features/tasks/ only |
| Feature cohesion | Low (scattered) | High (co-located) |
| Code navigation | Jump between directories | Everything in one folder |
| Shared code | Encouraged (base classes) | Discouraged (duplication OK) |
| Coupling | High (layers depend on layers) | Low (slices independent) |
| Cognitive load | High (must understand all layers) | Low (understand one slice) |

**Rationale:**

For a **learning-focused reference architecture**, vertical slices provide:
1. **Clear Mental Model**: "Each feature is self-contained"
2. **Easy to Copy**: Copy `features/tasks/` pattern for new features
3. **Reduced Side Effects**: Changes don't ripple unexpectedly
4. **Production Viable**: Pattern scales from 3 features to 30 features

This architecture optimizes for **maintainability and understanding** over theoretical DRY principles. The intentional duplication between slices is a feature, not a bug - it allows each slice to evolve independently without breaking others.

**When to Use Vertical Slices:**
- ✅ Feature-rich applications (multiple distinct capabilities)
- ✅ Learning/reference codebases
- ✅ Teams with multiple developers
- ✅ Long-lived projects that will evolve

**When NOT to Use:**
- ❌ Microservices (each service is already a slice)
- ❌ Tiny apps (< 3 features) where layered is simpler
- ❌ Highly interconnected domain logic requiring shared business rules

## ADR-006: REPR Pattern (Request-Endpoint-Response)

**Context:** Need clear, maintainable API endpoint structure with strong contracts, automatic validation, and excellent documentation for both developers and AI agents implementing features.

**Decision:** Adopt REPR (Request-Endpoint-Response) pattern for all API endpoints - each endpoint has explicit Pydantic request/response schemas, single responsibility, and clear documentation.

**Pattern Definition:**
```
REQUEST → ENDPOINT → RESPONSE

Request:  Explicit Pydantic schema defining input (validation, documentation)
Endpoint: Single-purpose function handling one specific operation
Response: Explicit Pydantic schema defining output (serialization, documentation)
```

**REPR in FastAPI:**
```python
# Example: Create Task Endpoint

# REQUEST schema
class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=2000)

# ENDPOINT handler
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskCreateRequest,  # Explicit request
    current_user: User = Depends(get_current_user)
):
    task = await TaskService.create_task(current_user.id, request)
    return task  # FastAPI serializes via response_model

# RESPONSE schema
class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime
```

**Alternatives Considered:**

1. **Generic CRUD Controllers** ❌
   - Pro: Less code duplication
   - Con: Harder to customize per-endpoint
   - Con: Single controller handles multiple operations (bloated)
   - Con: Difficult to understand which schema applies to which operation

2. **Returning ORM Models Directly** ❌
   - Pro: No schema definition needed
   - Con: Exposes internal database structure
   - Con: No control over serialization
   - Con: Tight coupling between API and database

3. **Untyped Dictionaries** ❌
   - Pro: Maximum flexibility
   - Con: No validation
   - Con: No auto-generated documentation
   - Con: Runtime errors instead of compile-time checks

4. **Single Shared Request/Response Schema** ❌
   - Pro: Less schema definitions
   - Con: All fields optional (validation nightmare)
   - Con: Unclear which fields apply to which endpoint
   - Con: Breaking changes affect all endpoints

**Key Principles:**

1. **Explicit Request Schemas**
   - Every input has a dedicated schema
   - Validation rules in the schema (min_length, pattern, etc.)
   - Schema names end with "Request": `TaskCreateRequest`, `TaskUpdateRequest`

2. **Explicit Response Schemas**
   - Every output has a dedicated schema
   - Serialization controlled by schema
   - Schema names end with "Response": `TaskResponse`, `TaskListResponse`

3. **Single Responsibility**
   - Each endpoint does ONE thing
   - `create_task()` only creates tasks
   - `update_task()` only updates tasks
   - No combined operations like `upsert_task()`

4. **List Responses Wrapped**
   - Don't return `list[TaskResponse]` directly
   - Wrap in `TaskListResponse(tasks: list[TaskResponse])`
   - Allows future metadata without breaking changes

**Consequences:**

✅ **Benefits:**
- **Type Safety**: Pydantic validates all inputs/outputs at runtime
- **Auto-Documentation**: OpenAPI/Swagger docs are complete and accurate
- **Clear Contracts**: Developers know exactly what to send/receive
- **Easy Testing**: Mock requests/responses with known schemas
- **Refactor Safety**: Changes to one endpoint don't affect others
- **AI-Friendly**: Clear patterns for code generation
- **Version Tolerance**: Can add optional fields without breaking clients

⚠️ **Trade-offs:**
- **More Code**: Each endpoint needs request/response schemas
- **Schema Proliferation**: TaskCreateRequest, TaskUpdateRequest, etc.
- **Duplication**: Similar fields across schemas (intentional)

**Synergy with Vertical Slices:**

REPR and Vertical Slice Architecture work perfectly together:
- Each feature slice (e.g., `features/tasks/`) contains its schemas
- Request/Response schemas live in `features/tasks/schemas.py`
- All task-related contracts in one place
- High cohesion: schema + endpoint + service + model together

**Comparison:**

| Aspect | Generic Controllers | REPR Pattern |
|--------|-------------------|--------------|
| Endpoint responsibility | Multiple operations per controller | One operation per endpoint |
| Request validation | Scattered or implicit | Explicit Pydantic schema |
| Response structure | ORM models or dicts | Explicit Pydantic schema |
| Documentation | Manual or incomplete | Auto-generated from schemas |
| Customization | Difficult (affects all operations) | Easy (endpoint-specific) |
| Testability | Mock entire controller | Mock single endpoint |
| API contract | Implicit or documented separately | Explicit in code |

**Rationale:**

For Nomi as a **learning-focused reference architecture**, REPR provides:

1. **Clear Learning**: Each endpoint is self-documenting
2. **Best Practice**: Industry-standard pattern (originated in .NET, applies to all frameworks)
3. **Type Safety**: Catches errors at development time
4. **Copy-Paste Friendly**: Clear template for adding new endpoints
5. **Production Viable**: Pattern scales from 5 endpoints to 500 endpoints
6. **Auto-Documentation**: OpenAPI docs always accurate

The slight code duplication (multiple request/response schemas) is a feature, not a bug - it allows each endpoint to evolve independently without breaking others.

**Implementation Guidelines:**

```python
# NAMING: Descriptive and consistent
TaskCreateRequest     # POST request
TaskUpdateRequest     # PUT request
TaskResponse          # Single entity response
TaskListResponse      # Collection response

# VALIDATION: In the schema
title: str = Field(..., min_length=1, max_length=200)
status: str = Field(..., pattern="^(todo|done)$")

# DOCUMENTATION: Examples in schema
class Config:
    json_schema_extra = {
        "example": {...}
    }

# STATUS CODES: Explicit
@router.post(..., status_code=status.HTTP_201_CREATED)
@router.get(..., status_code=status.HTTP_200_OK)
@router.delete(..., status_code=status.HTTP_204_NO_CONTENT)
```

**When to Use REPR:**
- ✅ All API endpoints in the application
- ✅ Public and internal APIs
- ✅ REST APIs with clear operations

**When NOT to Use:**
- ❌ GraphQL APIs (different pattern)
- ❌ WebSocket/SSE (streaming, not request-response)
- ❌ Internal function calls (overhead without benefit)

---

**🎯 Architecture Complete**

This architecture document provides the complete technical blueprint for Nomi - a "Goldilocks" reference implementation proving enterprise patterns at learnable scale.

**Next Steps:**
1. Review this architecture document
2. Run `/bmad:bmm:workflows:solutioning-gate-check` (validates PRD + Architecture alignment)
3. Proceed to Epic breakdown and story creation
4. Begin implementation with Epic 1 (Project Foundation)

---

_Generated by BMAD Decision Architecture Workflow_
_Date: 2025-11-12_
_Updated: 2025-11-12 (Revised to Vertical Slice Architecture + REPR Pattern)_
_Architect: Winston (BMAD Architect Agent)_
_For: Justin_
