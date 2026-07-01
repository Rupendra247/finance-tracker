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
│   ├── models.py      # Database table definitions
│   ├── schemas.py     # Request/response data shapes
│   ├── routers.py     # API endpoint logic
│   └── auth.py        # Password hashing and JWT tokens
├── .env               # Secret keys (never commit this)
├── .gitignore
├── finance.db         # SQLite database file (auto-created)
└── README.md
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

### Request & Response Examples

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

## Security

- Passwords are hashed using **bcrypt** before storing
- Authentication uses **JWT tokens** that expire in 30 minutes
- Secret key is stored in `.env` and never committed to GitHub

## Concepts Demonstrated

- REST API design (GET, POST, PUT, DELETE)
- Database modeling with SQLAlchemy ORM
- Data validation with Pydantic schemas
- JWT-based authentication flow
- Password hashing and security best practices
- Environment variable management
- Auto-generated API documentation with Swagger UI

## Coming Soon

- Transactions (add/view/delete income and expenses)
- Categories (food, rent, salary, etc.)
- Budget tracking per category
- Summary endpoint (monthly totals and breakdowns)
- Deployment to Railway/Render (live URL)

**MIT License**

Copyright (c) 2026 Rupendra Dhungana

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Author

Rupendra Dhungana  
