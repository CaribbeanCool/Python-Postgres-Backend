# Python PostgreSQL Integration

This repository contains code and examples for integrating Python applications with PostgreSQL databases.

## Overview

This project demonstrates how to connect to, query, and manage PostgreSQL databases using Python. It includes examples of common database operations, best practices, and patterns for effective database integration.

## Requirements

- Python 3.6+
- PostgreSQL 10+
- psycopg2 (PostgreSQL adapter for Python)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/python_postgres.git

# Navigate to the project directory
cd python_postgres

# Install dependencies
uv sync
```

## Configuration

Create a `.env` file in the root directory with your database credentials:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
```

## Current DAOs

- `OrderDAO`: Manages order-related database operations.
- `CategoriesDAO`: Handles category-related database operations.
- `CustomersDAO`: Manages customer-related database operations.
- `ProductsDAO`: Handles product-related database operations
- `StudentsDAO`: Manages student-related database operations.

## TODO

- Implement additional DAOs for other entities.
- Add unit tests for existing DAOs.
- Improve error handling and logging.
