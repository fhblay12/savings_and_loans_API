# savings_and_loans_API

A RESTful API for managing a savings and loans system, built with FastAPI and PostgreSQL. The system handles the full lifecycle of customer accounts — from registration and savings management to loan applications, collateral tracking, and repayment processing.

---

## Tech Stack

- **Python** + **FastAPI**
- **PostgreSQL** (hosted on [Neon](https://neon.tech)) with **SQLAlchemy ORM**
- **Pydantic** for request/response schema validation
- **pytest** for testing
- **Docker** for containerization

---

## Features

- Customer registration and profile management
- Savings account creation and transaction history
- Loan applications with approval workflow
- Collateral registration and tracking
- Loan repayment processing
- Employment details management
- Admin management

---

## Project Structure

```
savings_and_loans_API/
├── routers/            # API route handlers (one file per resource)
├── services/           # Business logic layer
├── repositories/       # Database query layer
├── models/             # SQLAlchemy ORM models
├── schemas/            # Pydantic request/response schemas
├── tests/              # Unit and integration tests
├── database.py         # Database connection and session setup
├── main.py             # FastAPI app entry point
├── Dockerfile          # Container definition
├── docker-compose.yml  # Multi-service orchestration
├── requirements.txt    # Python dependencies
└── .env.example        # Environment variable template
```

The project follows a layered architecture — **routers → services → repositories** — keeping route handling, business logic, and database queries cleanly separated.

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) installed, or Python 3.11+ for local setup
- A PostgreSQL database (the project uses [Neon](https://neon.tech) — free tier works)

---

### Option 1: Run with Docker (Recommended)

The easiest way to run the project. No local Python setup needed.

1. Clone the repository
   ```bash
   git clone https://github.com/fhblay12/savings_and_loans_API.git
   cd savings_and_loans_API
   ```

2. Copy the environment file and fill in your Neon database credentials
   ```bash
   cp .env.example .env
   ```

3. Start the application
   ```bash
   docker-compose up --build
   ```

4. Visit the interactive API docs at `http://localhost:8000/docs`

---

### Option 2: Run Locally (without Docker)

Use this if you prefer a faster development loop and already have Python installed.

1. Clone the repository
   ```bash
   git clone https://github.com/fhblay12/savings_and_loans_API.git
   cd savings_and_loans_API
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the environment file and fill in your Neon database credentials
   ```bash
   cp .env.example .env
   ```

5. Start the application
   ```bash
   uvicorn main:app --reload
   ```

6. Visit the interactive API docs at `http://localhost:8000/docs`

---

## Environment Variables

Copy `.env.example` to `.env` and provide your values:

```
DATABASE_URL=postgresql://user:password@ep-xxxx.neon.tech/dbname?sslmode=require
```

The `DATABASE_URL` should match the connection string provided by your Neon project dashboard.

---

## API Reference

All endpoints are fully documented and testable via the built-in Swagger UI at `/docs` — no frontend required.

| Resource | Description |
|---|---|
| `/customers` | Register and manage customers |
| `/savings-accounts` | Create accounts and record transactions |
| `/loans` | Apply for and manage loans |
| `/loan-payments` | Process and track loan repayments |
| `/collateral` | Register and manage loan collateral |
| `/employment` | Manage customer employment details |
| `/admin` | Admin account management |

---

## Running Tests

```bash
pytest tests/
```

---

## Architecture Notes

This project was built with a deliberate layered structure:

- **Routers** handle HTTP requests and responses only
- **Services** contain all business logic and validation
- **Repositories** handle all direct database interaction
- **Models** define the database schema via SQLAlchemy
- **Schemas** define the API contract via Pydantic

This separation makes the codebase easier to test, extend, and maintain — each layer can be changed independently without affecting the others.
