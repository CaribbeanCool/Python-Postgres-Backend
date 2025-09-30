# Python RESTful API Backend with Python, Flask, and PostgreSQL

This repository contains code and examples for integrating Python applications with PostgreSQL databases.

## Overview

This personal project demonstrates how to create a RESTful API backend using Python, Flask, and PostgreSQL. It includes Data Access Objects (DAOs), routes, and authentication using JWT.

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

- CategoriesDAO
- ProductsDAO
- CustomersDAO
- OrdersDAO
- PartsDAO
- SuppliersDAO
- SuppliesDAO
- StudentsDAO

## TODO

- Implement additional DAOs for other entities.
- Add unit tests for existing DAOs.
- Improve error handling and logging.
