# FastAPI Product Management System

A complete REST API for product management built with FastAPI, SQLAlchemy, and MySQL/MariaDB. This project demonstrates modern Python web development practices including API design, database integration, data validation, and CORS configuration.

## 🚀 Features

- **Complete CRUD Operations**: Create, Read, Update, and Delete products
- **Database Integration**: MySQL/MariaDB with SQLAlchemy ORM
- **Data Validation**: Pydantic models for request/response validation
- **Dependency Injection**: Clean separation of database sessions
- **CORS Support**: Ready for frontend integration
- **Auto Documentation**: Interactive API docs with Swagger UI
- **Error Handling**: Comprehensive error messages and database transaction management

## 📁 Project Structure

```
Fast API practice/
├── main.py           # FastAPI application with API endpoints
├── models.py         # Pydantic models for data validation
├── db_models.py      # SQLAlchemy models for database operations
├── config.py         # Database configuration and connection
├── .env              # Environment variables (database credentials)
└── README.md         # Project documentation
```

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI
- **Database**: MySQL/MariaDB
- **ORM**: SQLAlchemy
- **Data Validation**: Pydantic
- **Database Driver**: PyMySQL
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.7+
- MySQL or MariaDB server
- pip (Python package manager)

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd "Fast API practice"
   ```

2. **Install dependencies**
   ```bash
   pip install fastapi uvicorn sqlalchemy pymysql python-dotenv
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   DB_USER=root
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_NAME=fastapi_practice
   ```

4. **Create database**
   
   Create a database in MySQL/MariaDB:
   ```sql
   CREATE DATABASE fastapi_practice;
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

## 🌐 API Endpoints

### Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message |
| `GET` | `/products` | Get all products |
| `GET` | `/products/id/{id}` | Get product by ID |
| `POST` | `/products/{id}` | Create new product |
| `PUT` | `/products/{id}` | Update existing product |
| `DELETE` | `/products/del_id/{id}` | Delete product by ID |

### 📝 API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

Visit `http://localhost:8000/redoc` for ReDoc documentation.

## 📊 Data Models

### Product Model
```json
{
  "id": 1,
  "name": "Product Name",
  "description": "Product Description",
  "price": 99.99,
  "quantity": 10
}
```

## 🔧 Usage Examples

### Get All Products
```bash
curl -X GET "http://localhost:8000/products"
```

### Get Product by ID
```bash
curl -X GET "http://localhost:8000/products/id/1"
```

### Create New Product
```bash
curl -X POST "http://localhost:8000/products/1" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "name": "Smartphone",
    "description": "Latest model smartphone",
    "price": 599.99,
    "quantity": 50
  }'
```

### Update Product
```bash
curl -X PUT "http://localhost:8000/products/1" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "name": "Updated Smartphone",
    "description": "Updated description",
    "price": 649.99,
    "quantity": 45
  }'
```

### Delete Product
```bash
curl -X DELETE "http://localhost:8000/products/del_id/1"
```

## 🏗️ Architecture

### File Descriptions

- **`main.py`**: Contains the FastAPI application, API endpoints, and business logic
- **`models.py`**: Pydantic models for data validation and serialization
- **`db_models.py`**: SQLAlchemy ORM models for database table definitions
- **`config.py`**: Database configuration, connection string, and session management

### Key Concepts

- **Dependency Injection**: Database sessions are injected into endpoints using FastAPI's dependency system
- **Model Separation**: Pydantic models handle API validation, SQLAlchemy models handle database operations
- **Transaction Management**: Automatic rollback on errors, proper session cleanup
- **CORS Configuration**: Enables frontend applications to communicate with the API

## 🔒 Security Notes

- Environment variables protect sensitive database credentials
- Database sessions are properly managed to prevent memory leaks
- Input validation through Pydantic models prevents invalid data

## 🧪 Testing

The application includes:
- Automatic database initialization with sample data
- Duplicate entry prevention
- Error handling and rollback mechanisms
- Proper session management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is for educational purposes and demonstrates FastAPI best practices.

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check your `.env` file configuration
   - Ensure MySQL/MariaDB server is running
   - Verify database credentials

2. **Import Errors**
   - Install all required dependencies: `pip install fastapi uvicorn sqlalchemy pymysql python-dotenv`

3. **Port Already in Use**
   - Use a different port: `uvicorn main:app --port 8001 --reload`

4. **CORS Issues**
   - Check the `allow_origins` setting in `main.py`
   - Add your frontend URL to the allowed origins

## 📚 Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
