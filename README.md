# 📚 Library Management API

![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge)
![JWT](https://img.shields.io/badge/Authentication-JWT-orange?style=for-the-badge)

**Version:** **1.0.0**

A RESTful Library Management API built using **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

The project demonstrates secure backend development through JWT authentication, role-based authorization, relational database design, and modular REST API architecture. It provides complete management of books, authors, borrowings, and reviews while following normalized database design principles.

**Repository:** https://github.com/mishilisious/Library-Management-API

---

# 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Database Design](#-database-design)
- [User Roles](#-user-roles)
- [API Endpoints](#-api-endpoints)
- [Installation](#-installation)
- [Running the Project](#-running-the-project)
- [Interactive API Documentation](#-interactive-api-documentation)
- [Project Statistics](#-project-statistics)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

---

# ✨ Features

### 🔐 Authentication

- JWT Authentication
- Secure password hashing
- Role-based authorization
- Protected API endpoints

### 📚 Book Management

- Create books
- View all books
- View individual books
- Update books
- Delete books
- Support multiple authors for a single book
- Automatic creation of new authors when required

### ✍️ Author Management

- Complete CRUD operations
- View all authors
- View books by author
- Update author information
- Delete authors
- Prevent deletion of authors currently linked to books

### 📖 Borrowing System

- Borrow books
- Return books
- Prevent duplicate active borrowings
- View personal borrowing history
- Admin view of all borrowing records

### ⭐ Review System

- Create reviews
- Update reviews
- Delete reviews
- One review per user per book
- Users can modify only their own reviews

---

# 🛠 Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python 3.14 |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Database Management | pgAdmin 4 |
| Authentication | JWT |
| Password Hashing | Passlib |
| Validation | Pydantic |
| Server | Uvicorn |

---

# 🏛 Architecture

The project follows a modular architecture where each resource is organized into its own router.

```text
Authentication
        │
        ▼
     FastAPI
        │
 ┌──────┼───────────────┐
 │      │       │       │
Books Authors Reviews Borrowings
        │
        ▼
 SQLAlchemy ORM
        │
        ▼
 PostgreSQL
```

Shared functionality such as authentication, database configuration, schemas, and helper functions are separated to improve maintainability, readability, and scalability.

---

# 📁 Project Structure

```text
Library-Management-API/
│
├── Library_api/
│   ├── auth.py
│   ├── authors.py
│   ├── books.py
│   ├── borrowings.py
│   ├── reviews.py
│   ├── helpers.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── main.py
│
├── images/
│   ├── swagger.png
│   └── ER_Diagram.png
│
├── README.md
└── requirements.txt
```

---

# 🗄 Database Design

The application follows a **normalized relational database design**.

### Database Tables

- Users
- Books
- Authors
- BookAuthors
- Borrowings
- Reviews

The relationship between **Books** and **Authors** is implemented using a **many-to-many** relationship through the **BookAuthors** junction table.

This design:

- Eliminates duplicate author records
- Supports multiple authors for a single book
- Allows authors to write multiple books
- Maintains referential integrity
- Improves scalability

---

## Entity Relationship Diagram

> Add the ER Diagram below after creating it.

```markdown
![ER Diagram](images/ER_Diagram.png)
```

---

# 👥 User Roles

## 👑 Admin

Administrators can:

- Create books
- Update books
- Delete books
- Create authors
- Update authors
- Delete authors
- View all borrowing records

---

## 👤 User

Users can:

- Borrow books
- Return books
- Create reviews
- Update their own reviews
- Delete their own reviews

---

# 📚 API Endpoints

## Authentication

| Method | Endpoint |
|---------|----------|
| POST | `/login` |

---

## Books

| Method | Endpoint |
|---------|----------|
| POST | `/books` |
| GET | `/books` |
| GET | `/books/{id}` |
| PUT | `/books/{id}` |
| PATCH | `/books/{id}` |
| DELETE | `/books/{id}` |

---

## Authors

| Method | Endpoint |
|---------|----------|
| POST | `/authors` |
| GET | `/authors` |
| GET | `/authors/{id}` |
| PATCH | `/authors/{id}` |
| DELETE | `/authors/{id}` |
| GET | `/authors/{id}/books` |

---

## Borrowings

| Method | Endpoint |
|---------|----------|
| POST | `/borrowings/borrow/{book_id}` |
| PATCH | `/borrowings/return/{book_id}` |
| GET | `/borrowings/me` |
| GET | `/borrowings` |

---

## Reviews

| Method | Endpoint |
|---------|----------|
| POST | `/reviews` |
| GET | `/reviews` |
| PATCH | `/reviews/{review_id}` |
| DELETE | `/reviews/{review_id}` |

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/mishilisious/Library-Management-API.git
```

Navigate into the project

```bash
cd Library-Management-API
```

Create and activate a virtual environment (recommended)

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

Install the required dependencies

```bash
pip install -r requirements.txt
```

Configure your PostgreSQL connection details inside `Library_api/database.py`.

Example:

```python
DATABASE_URL = "postgresql://username:password@localhost:5432/database_name"
```

---

# ▶ Running the Project

Start the FastAPI server

```bash
python -m uvicorn Library_api.main:app --reload
```

The application will be available at:

```
http://127.0.0.1:8000
```

---

# 📖 Interactive API Documentation

FastAPI automatically generates interactive Swagger documentation.

Visit:

```
http://127.0.0.1:8000/docs
```

to explore and test every endpoint directly from your browser.

### Swagger UI Preview

![Swagger UI](images/swagger.png)

---

# 📊 Project Statistics

| Property | Value |
|----------|-------|
| Version | 1.0.0 |
| Architecture | REST API |
| Authentication | JWT |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database Design | Normalized Relational Model |
| Framework | FastAPI |

---

# 🔮 Future Improvements

Potential enhancements include:

- Pagination
- Search functionality
- Book categories
- Average book ratings
- Reservation system
- Docker deployment
- Unit testing

---

# 👩‍💻 Author

**Amishi**

GitHub: https://github.com/mishilisious

This project was developed to strengthen backend development skills while exploring REST API design, authentication, authorization, relational database modeling, and modular application architecture using FastAPI and PostgreSQL.

---

# 📄 License

This project is intended for educational and learning purposes.

---

Thank you for taking the time to explore this project.

Feedback, suggestions, and contributions are always welcome.