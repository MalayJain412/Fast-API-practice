"""
Pydantic Models for Data Validation and Serialization

This file defines data models using Pydantic, which provides:
1. Automatic data validation for incoming HTTP requests
2. JSON serialization/deserialization for API responses
3. Type hints and automatic API documentation generation
4. Error handling for invalid data with detailed error messages
5. Integration with FastAPI for automatic request/response validation

Pydantic vs SQLAlchemy Models:
- Pydantic: API layer validation and serialization
- SQLAlchemy: Database layer operations and table definitions
"""

from pydantic import BaseModel  # Pydantic's BaseModel for data validation and serialization

class Product(BaseModel):
    """
    Pydantic model for Product data validation and API serialization.
    
    This model serves multiple purposes:
    - Validates incoming JSON data in API requests (automatic type checking)
    - Serializes Python objects to JSON responses (automatic conversion)
    - Provides type hints for better code completion and IDE support
    - Generates automatic API documentation in FastAPI
    - Converts between different data formats seamlessly
    
    Key Features:
    - All fields are required by default unless marked as Optional
    - Automatic type validation with clear error messages
    - JSON schema generation for API documentation
    - Integration with FastAPI request/response cycle
    
    Usage in FastAPI:
    - Request bodies: FastAPI automatically validates incoming JSON
    - Response models: Ensures consistent API response format
    - Documentation: Auto-generates OpenAPI/Swagger documentation
    """
    
    # Field definitions with type annotations
    # Pydantic uses these for validation and documentation
    id: int          # Product unique identifier (must be integer, required)
    name: str        # Product name (must be string, required)
    description: str # Product description (must be string, required)
    price: float     # Product price (must be float/number, required)
    quantity: int    # Available quantity (must be integer, required)
    
    ### Legacy approach without Pydantic (commented out for educational purposes)
    # Before using Pydantic BaseModel, we had to manually define __init__ method
    # and handle data validation ourselves. Pydantic automates all of this complexity.
    
    # def __init__(self, id: int, name: str, description: str, price: float, quantity: int):
    #     """
    #     Manual constructor that we used before adopting Pydantic.
    #     With BaseModel, this is automatically generated with built-in validation.
    #     The old approach required manual type checking and error handling.
    #     """
    #     self.id = id
    #     self.name = name
    #     self.description = description
    #     self.price = price
    #     self.quantity = quantity
    
    ### Benefits of using Pydantic BaseModel over manual class implementation:
    # 
    # 1. Automatic Type Validation:
    #    - Ensures id is int, name is str, etc. with clear error messages
    #    - Handles type conversion when possible (e.g., "123" -> 123)
    #
    # 2. JSON Serialization:
    #    - .model_dump() method converts object to dictionary
    #    - .model_dump_json() method converts object to JSON string
    #
    # 3. JSON Deserialization:
    #    - Product(**json_data) creates object from dictionary
    #    - Product.model_validate(json_data) validates and creates object
    #
    # 4. Better Error Messages:
    #    - Detailed validation errors with field names and expected types
    #    - Helps API users understand what went wrong
    #
    # 5. FastAPI Integration:
    #    - Automatic API documentation generation (OpenAPI/Swagger)
    #    - Request body validation without additional code
    #    - Response model validation ensures consistent API responses
    #
    # 6. Advanced Features:
    #    - Custom validators for complex business rules
    #    - Optional fields with default values
    #    - Nested models for complex data structures
    #    - Field aliases for different naming conventions

