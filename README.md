# Library Management System - Backend and Frontend APIs

## Overview

This project is a **Library Management System** composed of two independent APIs:

- **Backend/Admin API**: This API allows an admin to add, remove, and manage books, as well as track which books have been borrowed.
- **Frontend API**: This API allows users to enroll, browse books, borrow books, and filter them by categories or publishers.

Both APIs are **Dockerized** and communicate with each other to ensure that books created in the **Backend API** are available in the **Frontend API** for users to borrow. When a user borrows a book, the **Frontend API** syncs this information with the **Backend API**, marking the book as unavailable.

## Features

- **Backend API**:
  - Add new books to the catalog.
  - Remove books from the catalog.
  - List all borrowed books and their borrowers.
  - List all unavailable books (borrowed books).

- **Frontend API**:
  - List all books (fetched from the backend).
  - Filter books by category or publisher.
  - Borrow books and sync the borrowing information to the backend.

## Project Structure

- **Backend API**: Located in the `./backend` folder.
- **Frontend API**: Located in the `./frontend` folder.

## Requirements

- **Docker** and **Docker Compose** should be installed on your machine.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-repo/library-management-system.git
cd library-management-system
```

### 2. Build and Start the Docker Containers

```bash
# docker-compose up --build
docker compose up --build
```

### Postman Documentation
https://documenter.getpostman.com/view/23652017/2sAXqp8PK5

This will build and start both the **Frontend API** (on port `8000`) and the **Backend API** (on port `8001`).

### 3. Test the Application with Curl Commands

### Enroll a New User on the Frontend API
You can enroll a new user on the Frontend API by sending a POST request with the user information.
```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
           "email": "johndoe@example.com",
           "first_name": "John",
           "last_name": "Doe"
         }'
```

**Response**:
```json
{
  "message": "User created",
  "user": {
    "email": "johndoe@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

#### 1. **Add a Book to the Backend API**

This command adds a new book to the **Backend API** and syncs it with the **Frontend API**.

```bash
curl -X POST "http://localhost:8001/admin/books/" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "The Pragmatic Programmer",
           "author": "Andrew Hunt",
           "publisher": "Addison-Wesley",
           "category": "Technology"
         }'
```

**Response:**
```json
{
  "message": "Book added and synced with frontend",
  "book": {
    "id": 1,
    "title": "The Pragmatic Programmer",
    "author": "Andrew Hunt",
    "publisher": "Addison-Wesley",
    "category": "Technology"
  }
}
```

#### 2. **Get All Books from the Frontend API**

This command fetches all books from the **Frontend API**, which should include books created via the **Backend API**.

```bash
curl -X GET "http://localhost:8000/books/"
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "The Pragmatic Programmer",
    "author": "Andrew Hunt",
    "publisher": "Addison-Wesley",
    "category": "Technology",
    "available": true,
    "borrowed_until": null,
    "borrower_id": null
  }
]
```

#### 3. **Get Book by ID from the Frontend API**

This command retrieves a specific book by its ID from the **Frontend API**.

```bash
curl -X GET "http://localhost:8000/books/1"
```

**Response:**
```json
{
  "id": 1,
  "title": "The Pragmatic Programmer",
  "author": "Andrew Hunt",
  "publisher": "Addison-Wesley",
  "category": "Technology",
  "available": true,
  "borrowed_until": null,
  "borrower_id": null
}
```

#### 4. **Borrow a Book from the Frontend API**

This command borrows a book for a specific number of days and syncs the borrowed status with the **Backend API**.

```bash
curl -X POST "http://localhost:8000/books/borrow/1" \
     -H "Content-Type: application/json" \
     -d '{
           "user_id": 1,
           "days": 7
         }'
```

**Response:**
```json
{
  "message": "Book borrowed for 7 days by John Doe",
  "book": {
    "id": 1,
    "title": "The Pragmatic Programmer",
    "author": "Andrew Hunt",
    "publisher": "Addison-Wesley",
    "category": "Technology",
    "available": false,
    "borrowed_until": "2024-09-21T10:15:00Z",
    "borrower_id": 1
  }
}
```

#### 5. **List All Borrowed Books on the Backend API**

This command lists all books that have been borrowed, along with the borrower details.

```bash
curl -X GET "http://localhost:8001/admin/books/borrowed/"
```

**Response:**
```json
[
  {
    "book_id": 1,
    "borrower_name": "John Doe",
    "borrowed_until": "2024-09-21T10:15:00Z"
  }
]
```

#### 6. **List Unavailable Books on the Backend API**

This command lists all books that are currently unavailable (borrowed books).

```bash
curl -X GET "http://localhost:8001/admin/books/unavailable/"
```

**Response:**
```json
[
  {
    "book_id": 1,
    "borrower_name": "John Doe",
    "borrowed_until": "2024-09-21T10:15:00Z"
  }
]
```

#### 7. **Remove a Book from the Backend API**

This command deletes a book from the **Backend API**.

```bash
curl -X DELETE "http://localhost:8001/admin/books/1"
```

**Response:**
```json
{
  "message": "Book with ID 1 has been removed"
}
```

###  List Users from Frontend via Backend API

You can also list all users registered in the Frontend API through the Backend API using this command:

```bash
curl -X GET "http://localhost:8001/admin/users/"
```
```json
[
  {
    "id": 1,
    "email": "johndoe@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
]
```

### Conclusion

The Library Management System allows seamless communication between two APIs:
- The **Backend API** for managing book records and tracking borrowed books.
- The **Frontend API** for user interactions such as browsing and borrowing books.

The system also ensures data consistency between the two APIs by syncing book creation, borrowing, and availability status.

---

### Troubleshooting

- Ensure Docker is running correctly on your machine.
- Make sure both APIs are running on the correct ports (`8000` for the **Frontend API** and `8001` for the **Backend API**).
- If any issues arise with syncing between APIs, check the container logs:
  ```bash
  docker logs library-management-frontend_api-1
  docker logs library-management-backend_api-1
  ```

Feel free to extend or modify this project based on your needs!

---

That covers everything we implemented, including the **curl** commands with expected responses. Let me know if there's anything else you'd like to include!