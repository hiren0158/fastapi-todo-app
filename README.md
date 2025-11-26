# FastAPI Todo Application

A modern, production-ready Todo application built with FastAPI and MongoDB. Features user authentication, role-based access control, and a clean web interface.

## Features

- ✅ User authentication with JWT tokens
- ✅ Role-based access control (User/Admin)
- ✅ CRUD operations for todos
- ✅ MongoDB database with Beanie ODM
- ✅ Responsive web interface
- ✅ RESTful API with automatic documentation
- ✅ Docker support for easy deployment
- ✅ Environment-based configuration

## Tech Stack

- **Backend**: FastAPI 0.116+
- **Database**: MongoDB with Beanie ODM
- **Authentication**: JWT with passlib & python-jose
- **Frontend**: HTML templates with Jinja2
- **Deployment**: Docker & Docker Compose

## Project Structure

```
FastApi-main copy/
├── ToDoApp2/
│   ├── core/                  # Core utilities
│   │   ├── security.py        # Password hashing, JWT functions
│   │   ├── dependencies.py    # FastAPI dependencies
│   │   └── logging_config.py  # Logging configuration
│   ├── routers/               # API routes
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── todos.py          # Todo CRUD endpoints
│   │   ├── users.py          # User management
│   │   └── admin.py          # Admin endpoints
│   ├── schemas/               # Pydantic schemas
│   │   ├── auth.py           # Auth schemas
│   │   ├── todo.py           # Todo schemas
│   │   └── user.py           # User schemas
│   ├── static/                # Static files (CSS, JS)
│   ├── templates/             # HTML templates
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection
│   ├── models_beanie.py       # MongoDB models
│   └── main.py                # Application entry point
├── .env.example               # Environment variables template
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Quick Start

### Prerequisites

- Python 3.9+
- MongoDB (local or Docker)
- pip

### Local Development

1. **Clone the repository**
   ```bash
   cd "/Users/admin/Desktop/FastApi-main copy"
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and set your SECRET_KEY and other variables
   ```

5. **Start MongoDB** (if not using Docker)
   ```bash
   # macOS with Homebrew
   brew services start mongodb-community
   
   # Or use Docker
   docker run -d -p 27017:27017 --name mongodb mongo:latest
   ```

6. **Run the application**
   ```bash
   uvicorn ToDoApp2.main:app --reload --port 8081
   ```

7. **Access the application**
   - Web Interface: http://localhost:8081
   - API Documentation: http://localhost:8081/docs
   - Alternative API Docs: http://localhost:8081/redoc

### Docker Deployment

1. **Using Docker Compose** (recommended)
   ```bash
   docker-compose up -d
   ```

2. **Using Docker only**
   ```bash
   # Build the image
   docker build -t fastapi-todo .
   
   # Run the container
   docker run -d -p 8081:8081 \
     -e MONGODB_URL=mongodb://host.docker.internal:27017 \
     -e SECRET_KEY=your-secret-key \
     fastapi-todo
   ```

## Environment Variables

Create a `.env` file based on `.env.example`:

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | FastAPI Todo Application |
| `DEBUG` | Debug mode | False |
| `MONGODB_URL` | MongoDB connection URL | mongodb://localhost:27017 |
| `MONGODB_DB_NAME` | Database name | todoapp |
| `SECRET_KEY` | JWT secret key | **MUST CHANGE IN PRODUCTION** |
| `ALGORITHM` | JWT algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 20 |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8081 |

**⚠️ Important**: Generate a secure `SECRET_KEY` for production:
```bash
openssl rand -hex 32
```

## API Endpoints

### Authentication
- `POST /auth/` - Register new user
- `POST /auth/token` - Login and get JWT token
- `POST /auth/logout` - Logout user
- `GET /auth/login-page` - Login page
- `GET /auth/register-page` - Registration page

### Todos
- `GET /todos/` - Get all user's todos
- `GET /todos/todo/{todo_id}` - Get specific todo
- `POST /todos/todo` - Create new todo
- `PUT /todos/todo/update_todo/{todo_id}` - Update todo
- `DELETE /todos/todo/delete-todo/{todo_id}` - Delete todo
- `GET /todos/todo-page` - Todos page
- `GET /todos/add-todo-page` - Add todo page
- `GET /todos/edit-todo-page/{todo_id}` - Edit todo page

### User Management
- `GET /user/user` - Get current user info
- `PUT /user/password` - Change password

### Admin (Admin role required)
- `GET /admin/todo` - Get all todos
- `DELETE /admin/todo/{todo_id}` - Delete any todo

## User Roles

- **User**: Can manage their own todos
- **Admin**: Can view and delete all todos

## Development

### Running Tests

**Note**: The existing tests in `ToDoApp2/test/` are written for the old SQLAlchemy setup and need to be updated for Beanie/MongoDB. This is recommended as a follow-up task.

### Code Structure

The application follows a clean architecture pattern:

- **`core/`**: Reusable utilities (security, dependencies, logging)
- **`schemas/`**: Pydantic models for request/response validation
- **`routers/`**: API endpoint definitions
- **`models_beanie.py`**: Database models
- **`config.py`**: Centralized configuration
- **`database.py`**: Database connection management

### Adding New Features

1. Define Pydantic schemas in `schemas/`
2. Create/update database models in `models_beanie.py`
3. Implement business logic in `routers/`
4. Use core utilities from `core/` for common operations

## Deployment

### Production Checklist

- [ ] Set a strong `SECRET_KEY` in environment variables
- [ ] Set `DEBUG=False`
- [ ] Configure CORS origins in `main.py`
- [ ] Set up MongoDB with authentication
- [ ] Configure reverse proxy (nginx/traefik)
- [ ] Set up SSL/TLS certificates
- [ ] Configure log rotation
- [ ] Set up monitoring and alerting
- [ ] Regular database backups

### Docker Compose Production

```yaml
# Modify docker-compose.yml for production:
# - Add MongoDB authentication
# - Use environment file for secrets
# - Add nginx reverse proxy
# - Configure volumes for persistence
```

## Troubleshooting

### MongoDB Connection Issues
```bash
# Check if MongoDB is running
docker ps | grep mongo

# Check MongoDB logs
docker logs todoapp-mongodb
```

### Application Won't Start
```bash
# Check logs
docker logs todoapp-fastapi

# Verify environment variables
docker exec todoapp-fastapi env | grep MONGODB
```

### Port Already in Use
```bash
# Find process using port 8081
lsof -i :8081

# Kill the process or change PORT in .env
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Check the API documentation at `/docs`
- Review this README
- Check application logs in `logs/app.log`

## Changelog

### Version 1.0.0 (Current)
- ✅ Restructured project with proper separation of concerns
- ✅ Added configuration management with Pydantic Settings
- ✅ Implemented core utilities module
- ✅ Separated schemas from models
- ✅ Added Docker support
- ✅ Enhanced error handling and logging
- ✅ Fixed password hashing bugs
- ✅ Improved code documentation
