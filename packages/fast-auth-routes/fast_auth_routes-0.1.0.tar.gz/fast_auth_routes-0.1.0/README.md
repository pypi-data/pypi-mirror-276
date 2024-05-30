# Fast_Auth

Fast_Auth is a simple FastAPI application with authentication and user management using MongoDB.

## Features

- User Signup
- User Login
- User Recover Password
- Token-based Authentication

## Installation

To install the package, use pip:

```bash
pip install fast_auth
```

## Required Enviroment Variables

```bash
# MONGO DB
export MONGO_URI="mongodb://localhost:27017t"
export MONGO_DB_NAME="db_name"

# JWT
export SECRET_KEY="your_secret_key"
export ALGORITHM="HS256" 
export ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Usage

To run the application, use the following command:

```bash
uvicorn fast_auth.main:app --reload
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.