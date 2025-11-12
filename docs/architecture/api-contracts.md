# API Contracts

## Authentication Endpoints

**POST /api/auth/login**
- Initiates OAuth2 flow
- Redirects to EntraID authorization URL
- No request body
- Response: 302 Redirect to EntraID

**GET /api/auth/callback**
- OAuth2 callback from EntraID
- Query params: `code`, `state`
- Exchanges code for tokens (server-side)
- Creates session, sets HTTP-only cookie
- Response: 302 Redirect to frontend home

**GET /api/auth/me**
- Returns current user profile
- Requires valid session cookie
- Response 200:
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "User Name"
}
```
- Response 401: Not authenticated

**POST /api/auth/logout**
- Destroys session
- Clears session cookie
- Response 200: `{"message": "Logged out"}`

## Tasks Endpoints

**GET /api/tasks**
- Lists all user's tasks
- Requires authentication
- Response 200:
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "title": "Task title",
    "description": "Task description",
    "status": "todo",
    "created_at": "2025-11-12T10:30:00Z",
    "updated_at": "2025-11-12T10:30:00Z"
  }
]
```

**POST /api/tasks**
- Creates new task
- Request body:
```json
{
  "title": "New task",
  "description": "Optional description"
}
```
- Response 201: Created task object

**GET /api/tasks/{id}**
- Retrieves single task
- Response 200: Task object
- Response 403: Not owner
- Response 404: Not found

**PUT /api/tasks/{id}**
- Updates task (partial update)
- Request body (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "status": "done"
}
```
- Response 200: Updated task object

**DELETE /api/tasks/{id}**
- Deletes task
- Response 204: No content
- Response 403: Not owner
- Response 404: Not found

## Inspirations Endpoints

**GET /api/inspirations**
- Lists all user's inspirations
- Response 200: Array of inspiration objects

**POST /api/inspirations**
- Creates new inspiration
- Request body:
```json
{
  "title": "Inspiration title",
  "description": "Optional description"
}
```
- Response 201: Created inspiration object

**GET /api/inspirations/{id}**
- Retrieves single inspiration
- Response 200: Inspiration object

**PUT /api/inspirations/{id}**
- Updates inspiration
- Request body (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description"
}
```
- Response 200: Updated inspiration object

**DELETE /api/inspirations/{id}**
- Deletes inspiration
- Response 204: No content

**POST /api/inspirations/{id}/convert**
- Converts inspiration to task
- Creates task with copied title/description
- Deletes original inspiration
- Response 201: Created task object

## Common Response Codes

- **200 OK**: Successful GET/PUT
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Missing or invalid session
- **403 Forbidden**: Not authorized (wrong user)
- **404 Not Found**: Resource doesn't exist
- **422 Unprocessable Entity**: Validation error
