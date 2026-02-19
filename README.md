FastAPI Task Manager API
A clean‑architecture FastAPI backend that supports user authentication, JWT‑based authorization, and full task management.
This project demonstrates professional backend engineering practices including service‑layer abstraction, dependency injection, structured logging, validation, and modular routing.

🚀 Features
Authentication & Users
- User signup
- Secure login with JWT access tokens
- Password hashing
- Protected routes using Depends(get_current_user)
- Clean separation of concerns (routers → services → repositories)
Tasks
- Create tasks
- Retrieve all tasks for the authenticated user
- Retrieve a single task
- Mark tasks as completed
- Delete tasks
- Validation & error handling
- User‑scoped task isolation (no cross‑user access)
Architecture
- Clean architecture with clear domain boundaries
- Service layer for business logic
- Repository layer (in‑memory for now, database‑ready)
- Pydantic schemas for request validation
- Serializers for response formatting
- Centralized logging configuration
- JWT handler utilities
- Dependency injection for services

📁 Project Structure
project-root/
│
├── backend/
│   ├── api/
│   │   ├── user_routes.py
│   │   └── task_routes.py
│   │
│   ├── core/
│   │   └── logging_config.py
│   │
│   ├── domain/
│   │   ├── user.py
│   │   ├── task.py
│   │   └── interfaces.py
│   │
│   ├── repositories/
│   │   ├── in_memory_user_repository.py
│   │   └── in_memory_task_repository.py
│   │
│   ├── services/
│   │   ├── user_service.py
│   │   └── task_service.py
│   │
│   ├── schemas/
│   │   ├── user_schemas.py
│   │   └── task_schemas.py
│   │
│   ├── utils/
│   │   ├── jwt_handler.py
│   │   ├── dependencies.py
│   │   ├── user_serializer.py
│   │   └── task_serializer.py
│   │
│   ├── main.py
│   └── requirements.txt
│
└── .gitignore



🔐 Authentication Flow
- Signup
POST /users/signup
Creates a new user.
- Login
POST /users/login
Returns a JWT access token:
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
- Use Token in Requests
Add this header to all protected routes:
Authorization: Bearer <token>



🧪 Testing with Postman
To avoid copying tokens manually:
- Create a Postman environment variable named token
- In the Tests tab of the login request, add:
  
let data = pm.response.json();
pm.environment.set("token", data.access_token);

- In protected routes, set the header:
Authorization: Bearer {{token}}


Postman will automatically inject the token after login.

▶️ Running the Project
1. Install dependencies
pip install -r backend/requirements.txt


2. Start the server
uvicorn backend.main:app --reload


3. Open API docs
Visit:
http://127.0.0.1:8000/docs



🛠 Technologies Used
- FastAPI
- Python 3.10+
- JWT (PyJWT)
- Pydantic
- Uvicorn
- Clean Architecture Principles
- Structured Logging

📌 Future Improvements
- Database integration (PostgreSQL / MongoDB)
- Refresh tokens
- Role‑based access control (RBAC)
- Pagination & filtering for tasks
- Dockerization
- CI/CD with GitHub Actions

📄 License
This project is open‑source and available under the MIT License.
