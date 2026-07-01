# Backend & API — Complete Study Guide (Python Edition)

This covers every term from my notes, in the order you'd actually learn them, using **Python + FastAPI** instead of Node.js/Express.

---

## 1. Backend & Server

**Backend** = the part of an application that runs on a server (not visible to the user). It handles logic, talks to the database, and sends data to the frontend.

**Server** = a computer program (running on a machine) that listens for requests and sends back responses.

```
[Frontend/App] ---request---> [Backend/Server] ---query---> [Database]
[Frontend/App] <--response--- [Backend/Server] <--data----- [Database]
```

Example: When you open Instagram and see your feed, your phone (frontend) asks Instagram's server (backend) for your posts, and the server fetches them from a database.

---

## 2. API (Application Programming Interface)

**API = a way for two applications to "talk" to each other.** It's a set of rules that says: "send me a request in this format, and I'll give you a response in this format."

Your note "(connect app)" is exactly right — APIs connect apps (frontend to backend, or backend to backend).

Analogy: A restaurant menu. You (the app) don't go into the kitchen (server) yourself. You give the waiter (API) your order, and the waiter brings back food (data) in a standard way.

---

## 3. REST API & Python

**REST (Representational State Transfer)** is a *style/convention* for building APIs using standard HTTP methods and URLs that represent resources.

Example of REST-style URLs:
```
GET    /users          → get all users
GET    /users/5        → get user with id 5
POST   /users          → create a new user
PUT    /users/5        → update user 5
DELETE /users/5        → delete user 5
```

**Python** is the runtime/language used to write this backend logic (it replaces Node.js entirely — you don't need Node.js if you're using Python).

```python
# The simplest possible Python web server (using FastAPI)
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from the backend!"}

# Run with: uvicorn main:app --reload --port 3000
```

---

## 4. JSON (JavaScript Object Notation)

**JSON** is the standard data format used to send data between frontend and backend — despite the name, every language including Python reads/writes it easily.

```json
{
  "id": 5,
  "name": "Aayush",
  "email": "aayush@example.com",
  "isActive": true
}
```

In Python, JSON maps directly to a dictionary:
```python
import json

data = {"id": 5, "name": "Aayush", "isActive": True}
json_string = json.dumps(data)   # Python dict → JSON string
parsed = json.loads(json_string) # JSON string → Python dict
```

With FastAPI, this conversion happens automatically — you just return a dictionary and it becomes JSON.

---

## 5. API Routes

A **route** is a specific URL path + HTTP method combination that your server listens for and responds to.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users")          # route 1
def get_users():
    return {"users": []}

@app.post("/users")         # route 2
def create_user():
    return {"message": "created"}

@app.get("/users/{id}")     # route 3
def get_user(id: int):
    return {"id": id}
```

---

## 6–7. HTTP Methods (GET, POST, PUT, DELETE)

HTTP methods tell the server **what action** you want to perform.

| Method | Purpose | Example |
|--------|---------|---------|
| **GET** | Read/fetch data | Get list of users |
| **POST** | Create new data | Add a new user |
| **PUT** | Update/replace data | Update a user's full profile |
| **PATCH** | Partially update data | Update just the user's email |
| **DELETE** | Remove data | Delete a user |

```python
@app.get("/products")
def get_all_products():
    return {"products": []}

@app.post("/products")
def create_product():
    return {"message": "Product created"}

@app.put("/products/{id}")
def update_product(id: int):
    return {"message": f"Product {id} updated"}

@app.delete("/products/{id}")
def delete_product(id: int):
    return {"message": f"Product {id} deleted"}
```

---

## 8. Query Params

**Query parameters** are extra data sent in the URL after a `?`, usually used for filtering, sorting, or pagination.

```
GET /products?category=shoes&sort=price&limit=10
```

In FastAPI, query params are just regular function arguments (not in the URL path):
```python
@app.get("/products")
def get_products(category: str = None, sort: str = None, limit: int = 10):
    print(category)  # "shoes"
    return {"category": category, "sort": sort, "limit": limit}
```

---

## 9. Body Params

**Body parameters** are data sent inside the **request body** (not the URL) — used mainly with POST/PUT for sending larger or sensitive data like form data.

FastAPI uses **Pydantic models** to define the expected body shape:
```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

@app.post("/users")
def create_user(user: UserCreate):
    print(user.name)   # "Aayush"
    print(user.email)  # "aayush@example.com"
    return {"message": "User created", "user": user}
```

**Query params vs Body params:** query params are visible in the URL (good for filters, IDs), body params are hidden in the request body (good for passwords, forms, large data).

---

## 10. FastAPI (Python's Express.js Equivalent)

**FastAPI** is the most popular modern Python framework for building APIs — it's the direct equivalent of Express.js, but with built-in data validation and auto-generated documentation.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
def home():
    return {"message": "Welcome to my API"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items")
def create_item(item: Item):
    return {"created": item}

# Run: uvicorn main:app --reload --port 3000
# Auto docs available at: http://localhost:3000/docs
```

> **Note:** Other Python framework options exist — **Flask** (simpler, more manual, closer to raw routing) and **Django** (full-featured, includes ORM + auth + admin panel built-in). FastAPI is recommended for REST APIs because it maps closest to what your notes describe (Routes, Body Params, Validation) with the least extra setup.

---

## 11. Middleware

**Middleware** is a function that runs *between* the request coming in and the final response going out. Used for things like logging, authentication, or parsing data.

```python
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"{request.method} request to {request.url}")
    start = time.time()
    response = await call_next(request)  # pass control to the next handler
    duration = time.time() - start
    print(f"Completed in {duration:.2f}s")
    return response

@app.get("/users")
def get_users():
    return {"users": []}
```

Common middleware: request logging, authentication checks, CORS handling, error handling.

---

## 12–14. SQL, Schema, and Queries

**SQL (Structured Query Language)** is used to talk to relational databases (like PostgreSQL, MySQL) — this is the same regardless of backend language.

**Schema** = the structure/blueprint of your database — tables, columns, and data types.

```sql
-- Schema: defining a table
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  email VARCHAR(100) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Queries** = the actual commands you run to interact with data.

```sql
SELECT * FROM users;                                    -- read all users
SELECT * FROM users WHERE id = 5;                        -- read one user
INSERT INTO users (name, email) VALUES ('Aayush', 'a@x.com'); -- create
UPDATE users SET name = 'Aayush K' WHERE id = 5;          -- update
DELETE FROM users WHERE id = 5;                           -- delete
```

Running these from Python using **SQLAlchemy** (the most popular Python SQL toolkit):
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)

engine = create_engine("postgresql://user:password@localhost/myapp")
Session = sessionmaker(bind=engine)
session = Session()

# Queries using SQLAlchemy (Python objects instead of raw SQL)
all_users = session.query(User).all()                    # SELECT *
one_user = session.query(User).filter_by(id=5).first()    # SELECT WHERE
new_user = User(name="Aayush", email="a@x.com")
session.add(new_user); session.commit()                   # INSERT
one_user.name = "Aayush K"; session.commit()               # UPDATE
session.delete(one_user); session.commit()                 # DELETE
```

Notice: SQL commands map directly to HTTP methods! `SELECT`→GET, `INSERT`→POST, `UPDATE`→PUT/PATCH, `DELETE`→DELETE.

---

## 15. Setting Up a Database

Installing a database (like PostgreSQL) and connecting your Python backend to it.

```python
# Connecting Python to PostgreSQL using psycopg2 (raw driver)
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="myapp",
    user="postgres",
    password="password",
    port=5432
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
print(rows)
```

Most projects use **SQLAlchemy** (shown above) instead of raw `psycopg2`, since it's easier to work with Python objects instead of raw SQL strings.

---

## 16. Migrations

**Migrations** are version-controlled files that change your database structure over time (like Git, but for your database schema) — so your team stays in sync.

In Python, the standard tool is **Alembic** (pairs with SQLAlchemy):

```python
# Example migration file (generated by Alembic)
def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100)),
        sa.Column('email', sa.String(100), unique=True),
    )

def downgrade():
    op.drop_table('users')
```

```bash
# Commands to generate and run migrations
alembic revision --autogenerate -m "create users table"
alembic upgrade head
```

If you later need to add a `phone` column, you write a *new* migration instead of editing the old one — this keeps a history of all schema changes.

---

## 17–18. File Uploads & Amazon S3

**File uploads**: handling files (images, PDFs) sent from the client to your server.

```python
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/upload")
async def upload_file(photo: UploadFile = File(...)):
    contents = await photo.read()
    with open(f"uploads/{photo.filename}", "wb") as f:
        f.write(contents)
    return {"message": "File uploaded!", "filename": photo.filename}
```

**Amazon S3 (Simple Storage Service)**: instead of storing files on your own server (which fills up and doesn't scale), you store them in the cloud on AWS S3, and just save the file's *URL* in your database.

```python
import boto3

s3 = boto3.client('s3')

s3.upload_fileobj(
    file_object,
    'my-app-bucket',
    'profile-photos/user5.jpg'
)

file_url = f"https://my-app-bucket.s3.amazonaws.com/profile-photos/user5.jpg"
```

---

## 19. Router / Controller / Repository (Repos) Pattern

This is a way to **organize** your backend code into clean layers instead of one giant file.

- **Router** → defines the URL/endpoint and which controller handles it
- **Controller** → handles the request/response logic (the "traffic cop")
- **Repository** → handles direct database queries

```python
# user_repository.py
def find_by_id(session, user_id):
    return session.query(User).filter_by(id=user_id).first()

# user_controller.py
def get_user(user_id: int, session):
    user = find_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# user_router.py
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/users/{id}")
def get_user_route(id: int, session=Depends(get_db)):
    return get_user(id, session)

# main.py
app.include_router(router)
```

This separation makes code easier to test, read, and maintain as the app grows. FastAPI's `APIRouter` is built specifically for splitting routes into separate files like this.

---

## 20. Design Patterns

Reusable, proven solutions to common software design problems. Router-Controller-Repository (above) is one example. Others include:

- **MVC (Model-View-Controller)** — separates data, UI, and logic (Django follows this closely)
- **Singleton** — ensures only one instance of something exists (e.g., one DB connection)
- **Dependency Injection** — FastAPI's `Depends()` is a built-in example of this pattern

```python
# Dependency Injection example (FastAPI's Depends)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def get_users(db=Depends(get_db)):  # db is "injected" automatically
    return db.query(User).all()
```

---

## 21–23. Authentication, Authorization, OAuth

These three are often confused — here's the clear difference:

- **Authentication** = "Who are you?" (verifying identity — login with password)
- **Authorization** = "What are you allowed to do?" (permissions — is this user an admin?)
- **OAuth** = a *protocol* that lets users log in using another provider (e.g., "Sign in with Google") without giving your app their password.

```python
from fastapi import FastAPI, Depends, HTTPException
from passlib.context import CryptContext
import jwt

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"])
SECRET_KEY = "SECRET_KEY"

# Authentication example — login and issue a token
@app.post("/login")
def login(email: str, password: str):
    user = get_user_by_email(email)  # fetch from DB
    if user and pwd_context.verify(password, user.password_hash):
        token = jwt.encode({"user_id": user.id}, SECRET_KEY, algorithm="HS256")
        return {"token": token}  # client stores this token for future requests
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Authorization example — dependency to check role
def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return current_user

@app.delete("/users/{id}")
def delete_user(id: int, admin=Depends(require_admin)):
    return {"message": f"User {id} deleted"}
```

**OAuth flow (simplified):** User clicks "Login with Google" → Google verifies them → Google sends your app a token confirming who they are → your app creates a session, without ever seeing the user's Google password. Python's `authlib` library is commonly used to implement this.

---

## 24. Params Validation

Before trusting any data from the client (query params, body params, route params), you should **validate** it — check it's the right type, format, and not malicious.

FastAPI's biggest advantage: **validation is built-in automatically** using Pydantic — you don't need a separate library.

```python
from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    email: EmailStr                    # must be a valid email format
    password: constr(min_length=6)     # must be at least 6 characters

@app.post("/users")
def create_user(user: UserCreate):
    # If validation fails, FastAPI automatically returns a 422 error
    # with details — this code only runs if the data is valid
    return {"message": "User created", "user": user}
```

Without validation, a user could send `email: "not-an-email"` or malicious data straight into your database. FastAPI catches this before your function even runs.

---

## How It All Connects (Full Flow)

```
1. Client sends HTTP request (GET/POST/etc) to a Route
2. Request passes through Middleware (logging, auth check)
3. FastAPI automatically Validates the Body/Query Params
4. Router sends it to the right Controller
5. Controller calls Repository to run a SQL Query
6. Database returns data
7. Controller sends back a JSON response
```

Example — creating a user, end to end:
```python
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

router = APIRouter()

class UserCreate(BaseModel):              # 9. Body params + 24. Validation
    name: str
    email: EmailStr

@router.post("/users")
def create_user_route(
    user: UserCreate,
    current_user=Depends(get_current_user),  # 21. Authentication check
    db=Depends(get_db)
):
    new_user = user_repository.insert(db, user)  # 12-14. SQL via repository
    return {"message": "User created", "user": new_user}  # 4. JSON response
```

This is exactly the path a real backend engineer follows — you're learning things in the right order!

---

## Quick Reference: Node.js/Express vs Python Terms

| Concept | Node.js World | Python World |
|---|---|---|
| Runtime | Node.js | Python |
| Framework | Express.js | **FastAPI** (or Flask/Django) |
| Package manager | npm | pip |
| Data validation | express-validator (manual) | Pydantic (built-in) |
| SQL toolkit | Sequelize / Knex | SQLAlchemy |
| Migrations tool | Knex migrations | Alembic |
| File upload | multer | UploadFile (built-in) |
| Cloud storage | aws-sdk | boto3 |
| Auth tokens | jsonwebtoken | PyJWT |
| Password hashing | bcrypt | passlib |