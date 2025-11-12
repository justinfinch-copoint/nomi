# Security Architecture

## Authentication Flow (Maximum Security Pattern)

```
┌─────────┐                                ┌──────────┐
│ Browser │                                │ Frontend │
└────┬────┘                                └─────┬────┘
     │                                           │
     │ 1. Click "Sign in with Microsoft"        │
     │─────────────────────────────────────────>│
     │                                           │
     │ 2. Redirect to /api/auth/login           │
     │<──────────────────────────────────────────│
     │                                           │
     │                                    ┌──────▼───────┐
     │                                    │   Backend    │
     │                                    │   (FastAPI)  │
     │                                    └──────┬───────┘
     │ 3. 302 Redirect to EntraID               │
     │<─────────────────────────────────────────┤
     │                                           │
┌────▼────────┐                                 │
│   EntraID   │                                 │
│ (Azure AD)  │                                 │
└────┬────────┘                                 │
     │                                           │
     │ 4. User authenticates (MFA, etc.)        │
     │                                           │
     │ 5. Redirect to /api/auth/callback        │
     │    with authorization code               │
     │──────────────────────────────────────────>│
     │                                           │
     │                                    ┌──────▼───────┐
     │                                    │   Backend    │
     │                                    │              │
     │                                    │ 6. Exchange  │
     │                                    │    code for  │
     │                                    │    tokens    │
     │                                    │              │
     │                                    │ 7. Validate  │
     │                                    │    ID token  │
     │                                    │              │
     │                                    │ 8. Create    │
     │                                    │    session   │
     │                                    │    in Redis  │
     │                                    │              │
     │                                    │ 9. Set       │
     │                                    │    HTTP-only │
     │                                    │    cookie    │
     │                                    └──────┬───────┘
     │                                           │
     │ 10. 302 Redirect to frontend home        │
     │<──────────────────────────────────────────┤
     │    with session cookie                    │
     │                                           │
┌────▼────┐                                     │
│ Browser │ Session cookie auto-included        │
│         │ in all subsequent requests          │
└─────────┘                                     │
```

## Session Security

**HTTP-only Signed Cookies:**
```python
# Cookie attributes
response.set_cookie(
    key="session_id",
    value=signed_session_id,  # Signed to prevent tampering
    httponly=True,            # JavaScript cannot access
    secure=True,              # HTTPS only (production)
    samesite="lax",           # CSRF protection
    max_age=86400             # 24 hours
)
```

**Session Storage:**
- Production: Redis with 24-hour TTL
- Development: In-memory dictionary
- Session contains: user_id, email, name, created_at, expires_at

**Zero Token Exposure:**
- Access tokens NEVER sent to browser
- Refresh tokens NEVER sent to browser
- ID tokens validated server-side only
- Only session ID (opaque, signed) exposed

## Data Security

**User Data Isolation:**
- Every query filters by `user_id` from session
- Ownership validation before updates/deletes
- No shared data between users

**Input Validation:**
- Pydantic schemas validate all inputs
- Character limits enforced (title: 200, description: 2000)
- SQL injection prevented (SQLAlchemy ORM, parameterized queries)
- XSS prevented (React escapes by default, no dangerouslySetInnerHTML)

**Secrets Management:**
- Environment variables for all secrets
- Never commit `.env` files
- Different secrets for dev/staging/prod

## HTTPS Requirement

**Production must use HTTPS:**
- Secure cookies require HTTPS
- Prevents session hijacking
- Protects against man-in-the-middle attacks
