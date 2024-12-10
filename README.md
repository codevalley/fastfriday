# Friday - Your Personal Life Logger

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://docs.python.org/3/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![OpenAPI](https://img.shields.io/badge/openapi-6BA539?style=for-the-badge&logo=openapi-initiative&logoColor=fff)](https://www.openapis.org/)
[![GraphQL](https://img.shields.io/badge/-GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white)](https://graphql.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://black.readthedocs.io/en/stable/)
[![Typed with: pydantic](https://img.shields.io/badge/typed%20with-pydantic-BA600F.svg?style=for-the-badge)](https://docs.pydantic.dev/)

## Description

_Your Personal Life Logger API_

Friday is a powerful API service designed to help you record and analyze the events of your daily life. Built with modern clean architecture principles, it provides a robust "API for Life" that lets you:

- Track daily activities and life events
- Record personal milestones and achievements
- Analyze patterns in your daily life
- Store and retrieve life memories securely

The service offers both REST and GraphQL interfaces, giving you flexibility in how you interact with your life data.

## Architecture Flexibility

### Database Agnostic
Friday follows clean architecture principles that isolate database dependencies. To switch databases (e.g., from MySQL to PostgreSQL or SQLite), you only need to modify:
1. Database configuration in `configs/Database.py`
2. Database dialect and credentials in `.env`
3. Install appropriate database driver

The rest of the application, including models, services, and API layers, remains unchanged due to:
- Use of SQLAlchemy ORM for database abstraction
- Repository pattern implementation
- Clean separation of concerns

### API Layer Flexibility
The application supports both REST and GraphQL APIs, demonstrating the power of clean architecture:
1. REST API endpoints in `routers/`
2. GraphQL schema in `schemas/graphql/`
3. Shared business logic in `services/`

Adding or modifying API endpoints only affects the outer API layer, leaving the core business logic untouched.

## Prerequisites

Before you can run Friday, ensure you have the following prerequisites set up:

1. **MySQL Server**
   ```sh
   # Install MySQL using Homebrew (macOS)
   $ brew install mysql
   
   # Start MySQL service
   $ brew services start mysql
   
   # Secure MySQL installation and set root password
   $ mysql_secure_installation
   ```

2. **MySQL Client Libraries**
   ```sh
   # Install MySQL connector (macOS)
   $ brew install mysql-connector-c
   
   # Set required environment variables
   $ export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
   $ export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
   ```

3. **Environment Setup**
   - Create a `.env` file in the project root with the following content:
   ```env
   APP_NAME=Friday
   API_VERSION=1.0.0
   DEBUG_MODE=True

   DATABASE_DIALECT=mysql
   DATABASE_HOSTNAME=localhost
   DATABASE_PORT=3306
   DATABASE_NAME=friday_db
   DATABASE_USERNAME=root
   DATABASE_PASSWORD=your_mysql_root_password
   ```

4. **Database Creation**
   ```sh
   # Create the database
   $ mysql -u root -p -e "CREATE DATABASE friday_db;"
   ```

## Installation

- Install all project dependencies using [Pipenv](https://pipenv.pypa.io):

  ```sh
  $ pipenv install --dev
  ```

- Run the application from command prompt:

  ```sh
  $ pipenv run uvicorn main:app --reload
  ```

- You can also open a shell inside virtual environment:

  ```sh
  $ pipenv shell
  ```

- Access your life logging API:
  - REST API Documentation: `localhost:8000/docs`
  - GraphQL Playground: `localhost:8000/graphql`

_*Note:* In case you are not able to access `pipenv` from your `PATH` locations, replace all instances of `pipenv` with `python3 -m pipenv`._

## Testing

For Testing, `unittest` module is used for Test Suite and Assertion, whereas `pytest` is being used for Test Runner and Coverage Reporter.

- Run the following command to initiate test:
  ```sh
  $ pipenv run pytest
  ```
- To include Coverage Reporting as well:
  ```sh
  $ pipenv run pytest --cov-report xml --cov .
  ```

## License

&copy; MIT License
