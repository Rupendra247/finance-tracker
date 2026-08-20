# Finance Tracker API

A REST API for tracking personal income and expenses. Users can register, log in, and manage their transactions with full CRUD operations. The API includes authentication, pagination, date filtering, and a summary endpoint.

---

## What This Project Does

- **Register & log in** with email and password (passwords are hashed, never stored plain text)
- **Create, read, update, and delete** income/expense transactions
- **List transactions** with pagination and date range filtering
- **Get a summary** of total income, total expenses, and current balance
- **Each user sees only their own data** — full user isolation

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework for building the API |
| [SQLAlchemy 2.0](https://docs.sqlalchemy.org/) | ORM — interact with the database using Python objects |
| [Pydantic v2](https://docs.pydantic.dev/) | Validate request data and format responses |
| [PostgreSQL](https://www.postgresql.org/) | Production database |
| [SQLite](https://www.sqlite.org/) | Development database (no setup needed) |
| [python-jose](https://python-jose.readthedocs.io/) | Generate and verify JWT authentication tokens |
| [passlib + bcrypt](https://passlib.readthedocs.io/) | Hash passwords securely |
| [Uvicorn](https://www.uvicorn.org/) | ASGI server to run the app |

---

## Project Structure

```
finance-tracker/
│
├── app/                        # Main application code
│   ├── __init__.py             # Makes "app" a Python package
│   ├── main.py                 # Entry point — creates FastAPI app, adds CORS, health check
│   ├── database.py             # Database connection, session management, Base class
│   ├── models.py               # SQLAlchemy models — defines database tables (User, Transaction)
│   ├── schemas.py              # Pydantic schemas — defines what request/response JSON looks like
│   ├── routers.py              # All API endpoints (register, login, transactions, summary)
│   └── auth.py                 # Password hashing, JWT token creation, get_current_user dependency
│
├── tests/                      # Automated tests
│   ├── __init__.py
│   ├── conftest.py             # Shared test fixtures (test client, test DB, auth helpers)
│   ├── test_schemas.py         # Tests for data validation rules
│   └── test_api.py             # Integration tests for all endpoints
│
├── .env                        # Your secret keys and config (NEVER commit this file)
├── .env.example                # Template showing what env vars are needed
├── .gitignore                  # Files Git should ignore
├── Dockerfile                  # Docker image build instructions
├── Procfile                    # Heroku/Railway start command
├── requirements.txt            # Python packages this project needs
├── pytest.ini                  # Pytest configuration
├── LICENSE                     # MIT License
└── README.md                   # This file
```

---

## Getting Started (Local Development)

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Step 1 — Clone the repository

```bash
git clone https://github.com/yourusername/finance-tracker.git
cd finance-tracker
```

### Step 2 — Create a virtual environment

A virtual environment keeps this project's packages separate from your other Python projects.

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

You'll know it's active because your terminal prompt will show `(venv)`.

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set up environment variables

Copy the example file and fill in your own values:

```bash
cp .env.example .env
```

Then open `.env` and edit it:

```bash
# Generate a real secret key with: python3 -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-generated-secret-key-here

# For local development, SQLite works great (no database server needed)
DATABASE_URL=sqlite:///./finance.db

# Comma-separated list of frontend URLs allowed to call this API
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Step 5 — Start the server

```bash
uvicorn app.main:app --reload
```

The `--reload` flag restarts the server automatically when you change code.

The API is now running at:

- **Base URL:** http://127.0.0.1:8000
- **Interactive docs (Swagger):** http://127.0.0.1:8000/docs
- **Alternative docs (ReDoc):** http://127.0.0.1:8000/redoc

---

## Running Tests

```bash
SECRET_KEY=test-secret DATABASE_URL=sqlite:///./test.db python -m pytest tests/ -v
```

The test suite covers:
- Schema validation (rejecting bad input)
- User registration and login
- Full transaction CRUD (create, read, update, delete)
- Pagination and filtering
- User isolation (Alice can't see Bob's transactions)
- Summary calculations
- Authentication enforcement on all protected endpoints

---

## API Reference

Every endpoint is documented automatically in the Swagger UI at `/docs`. Below is a summary.

### Health Check

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/` | No | Returns a status message confirming the API is running |
| `GET` | `/health` | No | Checks database connectivity. Returns `{"status": "healthy", "database": "ok"}` |

### Authentication

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/register` | No | Create a new user account |
| `POST` | `/login` | No | Log in and receive a JWT token |

### Transactions

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/transactions` | Yes | Create a new transaction (income or expense) |
| `GET` | `/transactions` | Yes | List your transactions (paginated, filterable) |
| `GET` | `/transactions/{id}` | Yes | Get a single transaction by ID |
| `PUT` | `/transactions/{id}` | Yes | Update a transaction (partial updates supported) |
| `DELETE` | `/transactions/{id}` | Yes | Delete a transaction |

### Summary

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/summary` | Yes | Get total income, total expenses, and balance |

---

## How Authentication Works

1. **Register** — Send your email and password to `POST /register`. Your password is hashed before being saved.
2. **Log in** — Send your email and password to `POST /login`. If valid, you receive a JWT token.
3. **Use the token** — For every protected endpoint, include this header in your request:
   ```
   Authorization: Bearer <your-token-here>
   ```
4. **Token expiry** — Tokens expire after 30 minutes. Log in again to get a new one.

---

## Request & Response Examples

### Register a new user

```bash
curl -X POST http://127.0.0.1:8000/register \
  -H "Content-Type: application/json" \
  -d '{"email": "rupendra@example.com", "password": "mypassword123"}'
```

Response (HTTP 201):
```json
{
  "id": 1,
  "email": "rupendra@example.com"
}
```

### Log in

```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=rupendra@example.com&password=mypassword123"
```

Response (HTTP 200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Create an income transaction

```bash
curl -X POST http://127.0.0.1:8000/transactions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"amount": 50000.0, "description": "Monthly salary", "type": "income"}'
```

Response (HTTP 201):
```json
{
  "id": 1,
  "amount": 50000.0,
  "description": "Monthly salary",
  "type": "income",
  "date": "2026-08-15T10:30:00Z"
}
```

### Create an expense transaction

```bash
curl -X POST http://127.0.0.1:8000/transactions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"amount": 1500.0, "description": "Grocery shopping", "type": "expense"}'
```

### List transactions with pagination and date filter

```bash
curl "http://127.0.0.1:8000/transactions?page=1&page_size=10&start_date=2026-01-01T00:00:00&end_date=2026-12-31T23:59:59" \
  -H "Authorization: Bearer <token>"
```

Response (HTTP 200):
```json
{
  "transactions": [
    {
      "id": 2,
      "amount": 1500.0,
      "description": "Grocery shopping",
      "type": "expense",
      "date": "2026-08-15T11:00:00Z"
    },
    {
      "id": 1,
      "amount": 50000.0,
      "description": "Monthly salary",
      "type": "income",
      "date": "2026-08-15T10:30:00Z"
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 10
}
```

### Update a transaction

```bash
curl -X PUT http://127.0.0.1:8000/transactions/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"description": "Monthly salary — August 2026"}'
```

### Delete a transaction

```bash
curl -X DELETE http://127.0.0.1:8000/transactions/1 \
  -H "Authorization: Bearer <token>"
```

Response: HTTP 204 (no body)

### Get summary

```bash
curl "http://127.0.0.1:8000/summary?start_date=2026-08-01&end_date=2026-08-31" \
  -H "Authorization: Bearer <token>"
```

Response (HTTP 200):
```json
{
  "total_income": 50000.0,
  "total_expense": 1500.0,
  "balance": 48500.0
}
```

---

## Query Parameters

### `GET /transactions`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | `1` | Page number (starts at 1) |
| `page_size` | integer | `20` | Results per page (1–100) |
| `start_date` | datetime | — | Only show transactions on or after this date |
| `end_date` | datetime | — | Only show transactions on or before this date |

### `GET /summary`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `start_date` | datetime | — | Only include transactions on or after this date |
| `end_date` | datetime | — | Only include transactions on or before this date |

Date format: ISO 8601, e.g. `2026-08-15T00:00:00` or `2026-08-15`

---

## Database Schema

### Users Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | Primary key, auto-increment | Unique user ID |
| `email` | String | Unique, indexed, not null | User's email address |
| `password` | String | Not null | Bcrypt-hashed password (never stored plain text) |
| `created_at` | DateTime (UTC) | Auto-set on creation | When the account was created |

### Transactions Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | Primary key, auto-increment | Unique transaction ID |
| `amount` | Float | Not null, must be > 0 | Transaction amount |
| `description` | String | Not null, 1–500 characters | What the transaction was for |
| `type` | Enum | Not null, "income" or "expense" | Whether this is money coming in or going out |
| `date` | DateTime (UTC) | Auto-set on creation | When the transaction was recorded |
| `user_id` | Integer | Foreign key → users.id, CASCADE delete | Which user owns this transaction |

**Relationship:** Each user has many transactions. Deleting a user automatically deletes all their transactions.

---

## Deployment

### Heroku / Railway / Render

1. Push your code to GitHub
2. Connect your repo to the hosting platform
3. Set these environment variables in the platform's dashboard:

```
SECRET_KEY=<generate-a-real-secret-key>
DATABASE_URL=postgresql://user:password@host:5432/dbname
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

The `Procfile` tells the platform how to start your app. No additional configuration needed.

**Important:** Use PostgreSQL for production. SQLite is fine for local development but won't work on most hosting platforms (the filesystem is wiped on every deploy).

### Docker

```bash
# Build the image
docker build -t finance-tracker .

# Run the container
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e DATABASE_URL=postgresql://user:pass@host:5432/dbname \
  -e ALLOWED_ORIGINS=https://your-frontend.vercel.app \
  finance-tracker
```

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | **Yes** | — | Secret key for signing JWT tokens. Generate with: `python3 -c "import secrets; print(secrets.token_hex(32))"` |
| `DATABASE_URL` | No | `sqlite:///./finance.db` | Database connection string. Use PostgreSQL for production. |
| `ALLOWED_ORIGINS` | No | `*` | Comma-separated list of frontend URLs allowed to call this API |

---

## Security

- **Password hashing** — Passwords are hashed with bcrypt before storage. Plain text passwords are never saved.
- **JWT authentication** — Tokens expire after 30 minutes. All transaction endpoints require a valid token.
- **User isolation** — Each user can only see and modify their own transactions. There is no way to access another user's data through the API.
- **Input validation** — All request data is validated. Emails must be valid, passwords must be at least 8 characters, amounts must be positive, and transaction types must be "income" or "expense".
- **Secrets management** — The `SECRET_KEY` and database credentials are stored in environment variables, never in code.

---

## Author

**Rupendra Dhungana**

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
