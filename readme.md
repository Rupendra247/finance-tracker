# Finance Tracker API

A REST API built with FastAPI and SQLite for tracking personal finances — income, expenses, and budgets.

## Tech Stack

- **FastAPI** — Python web framework for building APIs
- **SQLite** — lightweight database (file-based, no setup needed)
- **SQLAlchemy** — ORM for interacting with the database using Python
- **Pydantic** — data validation and serialization
- **JWT (JSON Web Tokens)** — secure authentication
- **Passlib + bcrypt** — password hashing

## Project Structure

```
finance-tracker/
├── app/
│   ├── __init__.py
│   ├── main.py        # App entry point, connects everything
│   ├── database.py    # Database connection setup
│   ├── models.py      # Database table definitions (User, Transaction)
│   ├── schemas.py     # Request/response data shapes
│   ├── routers.py     # API endpoint logic
│   └── auth.py        # Password hashing and JWT tokens
├── .env               # Secret keys (never commit this)
├── .gitignore
├── finance.db         # SQLite database file (auto-created)
└── README.md
└── requirement.txt
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/finance-tracker.git
cd finance-tracker
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy "fastapi[standard]" passlib[bcrypt] python-jose[cryptography] python-dotenv bcrypt==4.0.1
```

### 4. Create a `.env` file

```
SECRET_KEY=your-secret-key-here
```

### 5. Run the server

```bash
fastapi dev app/main.py
```

Server runs at: `http://127.0.0.1:8000`

Interactive docs at: `http://127.0.0.1:8000/docs`

## API Endpoints

### Auth

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register a new user | No |
| POST | `/login` | Login and receive JWT token | No |

### Transactions

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/transactions` | Add a new transaction | No (coming soon) |
| GET | `/transactions` | Get all transactions | No (coming soon) |

## Request & Response Examples

**POST /register**
```json
// Request
{
  "email": "user@example.com",
  "password": "securepassword"
}

// Response
{
  "id": 1,
  "email": "user@example.com"
}
```

**POST /login**
```json
// Request
{
  "email": "user@example.com",
  "password": "securepassword"
}

// Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**POST /transactions**
```json
// Request
{
  "amount": 500.0,
  "description": "Grocery shopping",
  "type": "expense"
}

// Response
{
  "id": 1,
  "amount": 500.0,
  "description": "Grocery shopping",
  "type": "expense",
  "date": "2026-06-28T10:00:00"
}
```

**GET /transactions**
```json
// Response
[
  {
    "id": 1,
    "amount": 500.0,
    "description": "Grocery shopping",
    "type": "expense",
    "date": "2026-06-28T10:00:00"
  }
]
```

## Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key, auto-increment |
| email | String | Unique user email |
| password | String | Bcrypt hashed password |
| created_at | DateTime | Account creation time |

### Transactions Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key, auto-increment |
| amount | Float | Transaction amount |
| description | String | What the transaction was for |
| type | String | "income" or "expense" |
| date | DateTime | When the transaction occurred |
| user_id | Integer | Foreign key linking to users table |

## Security

- Passwords are hashed using **bcrypt** before storing
- Authentication uses **JWT tokens** that expire in 30 minutes
- Secret key is stored in `.env` and never committed to GitHub

## Concepts Demonstrated

- REST API design (GET, POST, PUT, DELETE)
- Database modeling with SQLAlchemy ORM
- Table relationships with Foreign Keys
- Data validation with Pydantic schemas
- JWT-based authentication flow
- Password hashing and security best practices
- Environment variable management
- Auto-generated API documentation with Swagger UI

## Author

Rupendra Dhungana

---

**MIT License** — Copyright (c) 2026 Rupendra Dhungana
