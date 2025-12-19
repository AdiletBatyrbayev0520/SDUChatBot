# API Documentation
# SDU AI Chatbot Platform

**Document Version:** 1.0  
**Last Updated:** December 19, 2025  
**Base URL (Backend):** `https://chat-back.sdu.edu.kz/api`  
**Base URL (AI Service):** `https://your-lambda-url.amazonaws.com`  
**API Version:** v1

---

## Table of Contents

1. [Authentication](#authentication)
2. [Authentication Endpoints](#authentication-endpoints)
3. [Chat Management Endpoints](#chat-management-endpoints)
4. [Message Endpoints](#message-endpoints)
5. [AI Service Endpoints](#ai-service-endpoints)
6. [Error Codes](#error-codes)
7. [Rate Limiting](#rate-limiting)
8. [Pagination](#pagination)

---

## Authentication

The SDU Chatbot API uses **JWT (JSON Web Token)** based authentication with Bearer tokens.

### Authentication Flow

1. **Login**: User authenticates via Google OAuth or developer credentials
2. **Token Issuance**: Server returns `accessToken` and `refreshToken`
3. **Token Usage**: Include `accessToken` in Authorization header for protected endpoints
4. **Token Refresh**: Use `refreshToken` to obtain new `accessToken` when expired

### Authorization Header Format

```
Authorization: Bearer <accessToken>
```

### Token Expiration
- **Access Token**: 24 hours
- **Refresh Token**: 30 days

### Protected Endpoints

All endpoints under `/chats` require authentication. Include the Bearer token in the Authorization header:

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     https://chat-back.sdu.edu.kz/api/chats
```

---

## Authentication Endpoints

### 1. Google OAuth Login

Complete Google OAuth authentication flow.

**Endpoint:** `GET /auth/login`

**Authentication Required:** No

**Query Parameters:**

| Parameter | Type   | Required | Description                                    |
|-----------|--------|----------|------------------------------------------------|
| code      | string | Yes      | Authorization code from Google OAuth redirect  |
| scope     | string | Yes      | Granted scopes from Google                     |
| authuser  | string | Yes      | Google user identifier                         |
| prompt    | string | Yes      | Prompt metadata from Google OAuth              |

**Example Request:**

```bash
GET /auth/login?code=4/0AY0e-g7X...&scope=email%20profile&authuser=0&prompt=consent
```

**Success Response (200 OK):**

```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwicmVmcmVzaCI6dHJ1ZSwiaWF0IjoxNTE2MjM5MDIyfQ.abc123xyz"
}
```

**Error Responses:**

- **400 Bad Request**: Invalid or expired authorization code
- **500 Internal Server Error**: Error contacting Google OAuth or issuing tokens

---

### 2. Developer Login

Direct authentication for developers (non-production only).

**Endpoint:** `POST /auth/login-dev`

**Authentication Required:** No

**Request Body:**

```json
{
  "email": "developer@sdu.edu.kz",
  "password": "securePassword123",
  "securityKey": "dev-security-key-2024"
}
```

**Request Schema:**

| Field       | Type   | Required | Description                        |
|-------------|--------|----------|------------------------------------|
| email       | string | Yes      | Developer email address            |
| password    | string | Yes      | Developer password                 |
| securityKey | string | Yes      | Out-of-band security key           |

**Success Response (200 OK):**

```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**

- **401 Unauthorized**: Invalid credentials or security key

---

### 3. Logout

Terminate current user session and revoke tokens.

**Endpoint:** `POST /auth/logout`

**Authentication Required:** Yes

**Request Headers:**

```
Authorization: Bearer <accessToken>
```

**Success Response (204 No Content):**

No response body.

**Error Responses:**

- **401 Unauthorized**: Missing or invalid bearer token

---

## Chat Management Endpoints

### 4. Check AI Connection Status

Verify if the AI service is connected and operational.

**Endpoint:** `GET /chats/connected`

**Authentication Required:** Yes

**Success Response (200 OK):**

```json
true
```

or

```json
false
```

**Response Schema:**

| Field  | Type    | Description                              |
|--------|---------|------------------------------------------|
| result | boolean | `true` if AI service is connected        |

---

### 5. List User Chats

Retrieve paginated list of chats for the authenticated user.

**Endpoint:** `GET /chats`

**Authentication Required:** Yes

**Query Parameters:**

| Parameter | Type    | Required | Default | Description                    |
|-----------|---------|----------|---------|--------------------------------|
| page      | integer | No       | 0       | Page number (0-indexed)        |
| size      | integer | No       | 10      | Items per page (1-100)         |

**Example Request:**

```bash
GET /chats?page=0&size=20
Authorization: Bearer <accessToken>
```

**Success Response (200 OK):**

```json
{
  "content": [
    {
      "id": 1,
      "title": "Admission Requirements",
      "createdDate": "2025-12-15T10:30:00"
    },
    {
      "id": 2,
      "title": "Course Registration",
      "createdDate": "2025-12-16T14:20:00"
    }
  ],
  "page": 0,
  "size": 20,
  "totalElements": 45,
  "totalPages": 3,
  "last": false
}
```

**Response Schema:**

| Field         | Type    | Description                           |
|---------------|---------|---------------------------------------|
| content       | array   | Array of chat objects                 |
| page          | integer | Current page number                   |
| size          | integer | Items per page                        |
| totalElements | integer | Total number of chats                 |
| totalPages    | integer | Total number of pages                 |
| last          | boolean | Whether this is the last page         |

**Chat Object Schema:**

| Field       | Type     | Description                    |
|-------------|----------|--------------------------------|
| id          | integer  | Unique chat identifier         |
| title       | string   | Chat title or subject          |
| createdDate | datetime | ISO 8601 timestamp             |

---

### 6. Get Chat by ID

Retrieve metadata for a specific chat.

**Endpoint:** `GET /chats/{chatId}`

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type    | Required | Description            |
|-----------|---------|----------|------------------------|
| chatId    | integer | Yes      | Unique chat identifier |

**Example Request:**

```bash
GET /chats/123
Authorization: Bearer <accessToken>
```

**Success Response (200 OK):**

```json
{
  "id": 123,
  "title": "SDU Admission Process",
  "createdDate": "2025-12-15T10:30:00"
}
```

**Error Responses:**

- **404 Not Found**: Chat does not exist or does not belong to user

```json
{
  "error": "Chat not found",
  "message": "",
  "timestamp": 1702648800
}
```

---

### 7. Create New Chat

Create an empty chat container for the user.

**Endpoint:** `POST /chats`

**Authentication Required:** Yes

**Request Body:**

```json
{
  "title": "Questions about Scholarships"
}
```

**Request Schema:**

| Field | Type   | Required | Description       |
|-------|--------|----------|-------------------|
| title | string | Yes      | Chat title/subject|

**Success Response (201 Created):**

No response body.

**Error Responses:**

- **400 Bad Request**: Validation error in request payload

```json
{
  "error": "Bad Request",
  "message": "Title cannot be empty",
  "timestamp": 1702648800
}
```

---

### 8. Delete Chat

Remove a chat and all its messages.

**Endpoint:** `DELETE /chats/{chatId}`

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type    | Required | Description            |
|-----------|---------|----------|------------------------|
| chatId    | integer | Yes      | Unique chat identifier |

**Example Request:**

```bash
DELETE /chats/123
Authorization: Bearer <accessToken>
```

**Success Response (204 No Content):**

No response body.

**Error Responses:**

- **404 Not Found**: Chat not found or does not belong to user

---

## Message Endpoints

### 9. List Chat Messages

Retrieve paginated message history for a specific chat.

**Endpoint:** `GET /chats/{chatId}/messages`

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type    | Required | Description            |
|-----------|---------|----------|------------------------|
| chatId    | integer | Yes      | Unique chat identifier |

**Query Parameters:**

| Parameter | Type    | Required | Default | Description             |
|-----------|---------|----------|---------|-------------------------|
| page      | integer | No       | 0       | Page number (0-indexed) |
| size      | integer | No       | 10      | Items per page (1-100)  |

**Example Request:**

```bash
GET /chats/123/messages?page=0&size=50
Authorization: Bearer <accessToken>
```

**Success Response (200 OK):**

```json
{
  "content": [
    {
      "id": 1,
      "content": "What are the admission requirements for Computer Science?",
      "sources": [],
      "isUser": true,
      "number": 1,
      "version": 1,
      "createdDate": "2025-12-15T10:30:00",
      "costUsd": null,
      "topic": null
    },
    {
      "id": 2,
      "content": "The admission requirements for Computer Science at SDU include...",
      "sources": [
        "admission_policy.pdf",
        "cs_program_guide.pdf"
      ],
      "isUser": false,
      "number": 2,
      "version": 1,
      "createdDate": "2025-12-15T10:30:05",
      "costUsd": 0.0087,
      "topic": "Computer Science Admission"
    }
  ],
  "page": 0,
  "size": 50,
  "totalElements": 12,
  "totalPages": 1,
  "last": true
}
```

**Message Object Schema:**

| Field       | Type     | Description                                |
|-------------|----------|--------------------------------------------|
| id          | integer  | Unique message identifier                  |
| content     | string   | Message text content                       |
| sources     | array    | Source documents (for AI responses)        |
| isUser      | boolean  | `true` if user message, `false` if AI      |
| number      | integer  | Message sequence number in conversation    |
| version     | integer  | Message version (for editing)              |
| createdDate | datetime | ISO 8601 timestamp                         |
| costUsd     | number   | AI processing cost (null for user messages)|
| topic       | string   | Extracted topic (null for user messages)   |

**Error Responses:**

- **404 Not Found**: Chat not found or does not belong to user

---

### 10. Send Message to Existing Chat

Send a user message to an existing chat and receive AI response.

**Endpoint:** `POST /chats/{chatId}/messages`

**Authentication Required:** Yes

**Path Parameters:**

| Parameter | Type    | Required | Description            |
|-----------|---------|----------|------------------------|
| chatId    | integer | Yes      | Unique chat identifier |

**Request Body:**

```json
{
  "content": "What are the tuition fees for international students?"
}
```

**Request Schema:**

| Field   | Type   | Required | Description          |
|---------|--------|----------|----------------------|
| content | string | Yes      | User message text    |

**Success Response (200 OK):**

```json
{
  "chatId": 123,
  "title": "SDU Admission Process",
  "messageResponse": {
    "id": 456,
    "content": "The tuition fees for international students at SDU vary by program...",
    "sources": [
      "tuition_fees_2025.pdf",
      "international_students_guide.pdf"
    ],
    "isUser": false,
    "number": 8,
    "version": 1,
    "createdDate": "2025-12-15T11:45:30",
    "costUsd": 0.0124,
    "topic": "International Student Tuition Fees"
  },
  "createdDate": "2025-12-15T11:45:30"
}
```

**Response Schema:**

| Field           | Type    | Description                    |
|-----------------|---------|--------------------------------|
| chatId          | integer | Chat identifier                |
| title           | string  | Chat title                     |
| messageResponse | object  | AI response message object     |
| createdDate     | datetime| Response timestamp             |

**Error Responses:**

- **404 Not Found**: Chat not found or does not belong to user

---

### 11. Create Chat and Send Message

Create a new chat and send the first message in a single request.

**Endpoint:** `POST /chats/send-message`

**Authentication Required:** Yes

**Request Body:**

```json
{
  "content": "How do I apply for a scholarship at SDU?"
}
```

**Request Schema:**

| Field   | Type   | Required | Description          |
|---------|--------|----------|----------------------|
| content | string | Yes      | User message text    |

**Success Response (200 OK):**

```json
{
  "chatId": 789,
  "title": "How do I apply for a scholarship at SDU?",
  "messageResponse": {
    "id": 1,
    "content": "To apply for a scholarship at SDU, you need to...",
    "sources": [
      "scholarship_guide.pdf",
      "financial_aid_policy.pdf"
    ],
    "isUser": false,
    "number": 2,
    "version": 1,
    "createdDate": "2025-12-15T12:00:00",
    "costUsd": 0.0095,
    "topic": "SDU Scholarship Application"
  },
  "createdDate": "2025-12-15T12:00:00"
}
```

**Note:** The chat title is automatically generated from the first message content.

---

## AI Service Endpoints

### 12. Ask Question (POST)

Send a question to the SDU AI knowledge base.

**Endpoint:** `POST /` (AWS Lambda)

**Authentication Required:** No (API Key in backend)

**Request Body:**

```json
{
  "question": "What are the admission requirements for SDU?",
  "chat_id": "user123",
  "isNeedTopic": true
}
```

**Request Schema:**

| Field       | Type    | Required | Description                           |
|-------------|---------|----------|---------------------------------------|
| question    | string  | Yes      | User question                         |
| chat_id     | string  | Yes      | Unique user/session identifier        |
| isNeedTopic | boolean | No       | Whether to generate topic (default: false) |

**Success Response (200 OK):**

```json
{
  "question": "What are the admission requirements for SDU?",
  "answer": "The admission process at Suleyman Demirel University (SDU) is comprehensive and competitive. Students must meet specific requirements, including academic achievements, language proficiency, and personal statements...",
  "sources": [
    "admission_policy_EN.md",
    "SDU_intro_EN.md",
    "requirements_2025.md"
  ],
  "usage_metadata": {
    "input_tokens": 1250,
    "output_tokens": 380,
    "total_tokens": 1630,
    "cacheReadInputTokens": 0,
    "cacheWriteInputTokens": 5000,
    "cacheHitCount": 0
  },
  "topic": "SDU Admission Requirements"
}
```

**Response Schema:**

| Field          | Type   | Description                              |
|----------------|--------|------------------------------------------|
| question       | string | Original user question                   |
| answer         | string | AI-generated response                    |
| sources        | array  | Source document filenames                |
| usage_metadata | object | Token usage and cost information         |
| topic          | string | Extracted conversation topic (optional)  |

**Usage Metadata Schema:**

| Field                  | Type    | Description                        |
|------------------------|---------|------------------------------------|
| input_tokens           | integer | Input tokens processed             |
| output_tokens          | integer | Output tokens generated            |
| total_tokens           | integer | Total tokens used                  |
| cacheReadInputTokens   | integer | Tokens read from cache             |
| cacheWriteInputTokens  | integer | Tokens written to cache            |
| cacheHitCount          | integer | Number of cache hits               |

---

### 13. Ask Question (GET)

Send a question via query parameters (for testing).

**Endpoint:** `GET /` (AWS Lambda)

**Authentication Required:** No

**Query Parameters:**

| Parameter | Type   | Required | Default    | Description                |
|-----------|--------|----------|------------|----------------------------|
| question  | string | Yes      | -          | User question              |
| user_id   | string | No       | test_user  | User identifier            |
| language  | string | No       | en         | Language code (en/ru/kk)   |

**Example Request:**

```bash
GET /?question=What%20are%20SDU%20office%20hours?&user_id=test_user&language=en
```

**Success Response (200 OK):**

Same format as POST endpoint.

---

## Error Codes

### Standard HTTP Status Codes

| Status Code | Description                                      |
|-------------|--------------------------------------------------|
| 200         | OK - Request successful                          |
| 201         | Created - Resource created successfully          |
| 204         | No Content - Request successful, no response body|
| 400         | Bad Request - Invalid request parameters         |
| 401         | Unauthorized - Missing or invalid authentication |
| 403         | Forbidden - Insufficient permissions             |
| 404         | Not Found - Resource does not exist              |
| 429         | Too Many Requests - Rate limit exceeded          |
| 500         | Internal Server Error - Server error occurred    |
| 503         | Service Unavailable - Service temporarily down   |

### Error Response Format

All error responses follow this structure:

```json
{
  "error": "Error Type",
  "message": "Detailed error message",
  "timestamp": 1702648800
}
```

**Error Response Schema:**

| Field     | Type    | Description                           |
|-----------|---------|---------------------------------------|
| error     | string  | Error type or category                |
| message   | string  | Human-readable error description      |
| timestamp | integer | Unix timestamp of error occurrence    |

### Common Error Examples

**401 Unauthorized - Expired Token:**

```json
{
  "error": "UNAUTHORIZED",
  "message": "Jwt expired",
  "timestamp": 1702648800
}
```

**401 Unauthorized - Invalid Token:**

```json
{
  "error": "UNAUTHORIZED",
  "message": "Jwt invalid",
  "timestamp": 1702648800
}
```

**404 Not Found - Chat Not Found:**

```json
{
  "error": "Chat not found",
  "message": "",
  "timestamp": 1702648800
}
```

**400 Bad Request - Validation Error:**

```json
{
  "error": "Bad Request",
  "message": "Title cannot be empty",
  "timestamp": 1702648800
}
```

**400 Bad Request - Invalid Credentials:**

```json
{
  "error": "BAD_REQUEST",
  "message": "auth.invalid-credentials",
  "timestamp": 1702648800
}
```

---

## Rate Limiting

### Rate Limit Rules

| Endpoint Type      | Limit              | Window  |
|--------------------|--------------------|---------|
| Authentication     | 10 requests        | 1 minute|
| Chat Operations    | 100 requests       | 1 minute|
| Message Sending    | 30 requests        | 1 minute|
| AI Service         | 50 requests        | 1 minute|

### Rate Limit Headers

Response headers include rate limit information:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1702648860
```

### Rate Limit Exceeded Response (429)

```json
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded. Please try again in 30 seconds.",
  "timestamp": 1702648800
}
```

---

## Pagination

### Pagination Parameters

All list endpoints support pagination with these query parameters:

| Parameter | Type    | Default | Min | Max | Description             |
|-----------|---------|---------|-----|-----|-------------------------|
| page      | integer | 0       | 0   | -   | Page number (0-indexed) |
| size      | integer | 10      | 1   | 100 | Items per page          |

### Pagination Response Format

```json
{
  "content": [...],
  "page": 0,
  "size": 10,
  "totalElements": 45,
  "totalPages": 5,
  "last": false
}
```

**Pagination Metadata:**

| Field         | Type    | Description                    |
|---------------|---------|--------------------------------|
| content       | array   | Array of items for current page|
| page          | integer | Current page number (0-indexed)|
| size          | integer | Items per page                 |
| totalElements | integer | Total number of items          |
| totalPages    | integer | Total number of pages          |
| last          | boolean | Whether this is the last page  |

### Pagination Examples

**First Page:**
```bash
GET /chats?page=0&size=20
```

**Second Page:**
```bash
GET /chats?page=1&size=20
```

**Large Page Size:**
```bash
GET /chats/123/messages?page=0&size=100
```

---

## CORS Configuration

### Allowed Origins

The API supports Cross-Origin Resource Sharing (CORS) for the following origins:

- `https://chat.sdu.edu.kz`
- `http://localhost:5173` (development)
- `http://localhost:3000` (development)

### Allowed Methods

- GET
- POST
- PUT
- DELETE
- OPTIONS

### Allowed Headers

- Authorization
- Content-Type
- Accept

---

## API Versioning

The current API version is **v1**. Future versions will be accessible via URL path:

- Current: `https://chat-back.sdu.edu.kz/api/chats`
- Future: `https://chat-back.sdu.edu.kz/api/v2/chats`

---

## Additional Resources

- **Swagger UI**: `https://chat-back.sdu.edu.kz/api/swagger-ui.html`
- **OpenAPI Spec**: `https://chat-back.sdu.edu.kz/api/v3/api-docs`
- **Postman Collection**: Available in repository `/docs/postman/`

---

**Document Approval:**
- **API Design Review:** SDU ChatBot Development Team
- **Security Review:** Meraliyev Meraryslan, Head of Information Systems Department
- **Next API Review:** March 2026