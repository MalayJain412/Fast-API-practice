# def greet():
#     print("This is Malay")
    
# greet()

###############
# The above code will print in the console, but we want on web page........
###############

# Import necessary modules for FastAPI application
from fastapi import FastAPI, Depends  # FastAPI framework and dependency injection
from models import Product   # Import our Pydantic Product model for data validation
from config import session, engine  # Import database session and engine from config
import db_models  # Import SQLAlchemy database models
from sqlalchemy.orm import Session  # SQLAlchemy session type for dependency injection
from fastapi.middleware.cors import CORSMiddleware  # CORS middleware for frontend integration
# Create FastAPI application instance
# This is the main application object that will handle all HTTP requests
app = FastAPI()

# Add CORS middleware to allow frontend (React) to communicate with backend
# CORS (Cross-Origin Resource Sharing) allows requests from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow React development server
    allow_methods=["*"]  # Allow all HTTP methods (GET, POST, PUT, DELETE)
)

# Create all database tables based on SQLAlchemy models
# This line ensures that all tables defined in db_models are created in the database
# if they don't already exist. It's called at application startup.
db_models.Base.metadata.create_all(bind=engine)

# Define a simple GET endpoint at the root path "/"
# When someone visits the base URL, this function will be called
@app.get("/")
def greet():
    """
    Root endpoint that returns a simple greeting message.
    This is accessible at: http://localhost:8000/
    """
    return "This is Malay"
#run with uvicorn main

# Sample data for database initialization (commented out since now using database)
# These were Pydantic models that provided data validation and serialization  
# Note: Now we're using actual database operations instead of in-memory data
# products=[
#     Product(id=1,name='phone',description='samsung',price='54000.3',quantity=15),
#     Product(id=4,name='Laptop',description='samsung',price='740000',quantity=5),
#     Product(id=3,name="Charger",description="Mobile Charger",price=52,quantity=32)
# ]

# Database dependency injection function
# This function provides a database session to our API endpoints
def get_db():
    """
    Dependency function that provides database sessions to API endpoints.
    Uses dependency injection pattern to manage database connections.
    Automatically closes the session after use to prevent memory leaks.
    """
    db = session()  # Create new database session
    try:
        yield db  # Provide session to the endpoint
    finally:
        db.close()  # Always close session when done

def init_db():
    """
    Initialize the database with sample product data.
    This function adds sample data to the database if it's empty.
    Only runs on application startup to avoid duplicate entries.
    """
    db = session()  # Create a new SQLAlchemy session for database operations
    
    try:
        # Check if the table already has data to avoid duplicate entries
        existing_count = db.query(db_models.Product).count()
        
        if existing_count > 0:
            print(f"Database already has {existing_count} products. Skipping initialization.")
            db.close()
            return
        
        print("Initializing database with sample data...")
        
        # Sample data to initialize the database
        sample_products = [
            {"id": 1, "name": "phone", "description": "samsung", "price": 54000.3, "quantity": 15},
            {"id": 4, "name": "Laptop", "description": "samsung", "price": 740000, "quantity": 5},
            {"id": 3, "name": "Charger", "description": "Mobile Charger", "price": 52, "quantity": 32}
        ]
        
        for product_data in sample_products:
            # Create SQLAlchemy model instance directly from dictionary
            # ** unpacks the dictionary into keyword arguments
            db.add(db_models.Product(**product_data))  # Add the SQLAlchemy model to the database session
        
        db.commit()  # Commit all changes to the database
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()  # Rollback changes if there's an error
    finally:
        db.close()  # Always close the database session

init_db()

# GET endpoint to retrieve all products from database
# Uses dependency injection to get database session
# Accessible at: http://localhost:8000/products
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    """
    Retrieve all products from the database.
    Args:
        db (Session): Database session injected by FastAPI dependency system
    Returns:
        List of all products from database in JSON format
    """
    db_products = db.query(db_models.Product).all()  # Query all products from database
    return db_products

# GET endpoint with path parameter to retrieve a specific product by ID from database
# Path parameter {id} captures the ID from the URL
# Accessible at: http://localhost:8000/products/id/1 (where 1 is the product ID)
@app.get('/products/id/{id}')
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific product by its ID from database.
    Args:
        id (int): The unique identifier of the product (path parameter)
        db (Session): Database session injected by FastAPI dependency system
    Returns:
        Product object if found, error message if not found
    """
    # Query database for product with specific ID
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if db_product:
        return db_product
    return f'Product with id {id} not found, please verify the id, or try by name.'


# @app.get('/products/name/{name}')
# def get_product_by_id(name:str,db:Session=Depends(get_db)):
#     """
#     Retrieve a specific product by its Name.
#     Args:
#         name (str): The unique identifier of the product
#     Returns:
#         Product object if found, error message if not found
#     """
    
#     # for product in products:
#     #     if product.name == name:
#     #         return product
    
#     db_product = db.query(db_models.Product).filter(db_models.Product.name==name).first()
#     if db_product:
#         return db_product
#     return f'Product named {name} not found, please check the name again, or try with id.'


# POST endpoint to add a new product to database
# Uses Pydantic model for automatic request body validation
# Accessible at: http://localhost:8000/products/{id} (with POST method)
@app.post('/products/{id}')
def add_product(product: Product, db: Session = Depends(get_db)):
    """
    Add a new product to the database.
    Args:
        product (Product): Product data in request body, validated by Pydantic model
        db (Session): Database session injected by FastAPI dependency system
    Returns:
        The newly added product
    """
    # Convert Pydantic model to SQLAlchemy model and save to database
    db.add(db_models.Product(**product.model_dump()))
    db.commit()  # Commit the transaction to save changes
    return product

# PUT endpoint to update an existing product in database
# Requires both ID parameter and product data in request body
# Accessible at: http://localhost:8000/products/{id} (with PUT method)
@app.put('/products/{id}')
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    """
    Update an existing product in database by ID.
    Args:
        id (int): ID of the product to update (path parameter)
        product (Product): New product data (request body)
        db (Session): Database session injected by FastAPI dependency system
    Returns:
        Success message with updated product info, or error if not found
    """
    # Find the product in database by ID
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if db_product:
        # Update all fields with new data
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()  # Save changes to database
        return f"Information for product id: {id} and name: {product.name} updated"
    else:
        return f"No product with id {id} found"

# DELETE endpoint to remove a product by ID from database
# Uses path parameter to specify which product to delete
# Accessible at: http://localhost:8000/products/del_id/{id} (with DELETE method)
@app.delete('/products/del_id/{id}')
def delete_product_from_id(id: int, db: Session = Depends(get_db)):
    """
    Delete a product from database using its ID.
    Args:
        id (int): ID of the product to delete (path parameter)
        db (Session): Database session injected by FastAPI dependency system
    Returns:
        Success message if deleted, error message if not found
    """
    # Find the product in database by ID
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)  # Delete the product from database
        db.commit()  # Commit the transaction
        return f"Product with id {id} deleted successfully."
    else:
        return f"Product Not found, please check the {id} again"    
    
# # DELETE endpoint to remove a product by name
# # Uses query parameter to specify which product to delete by name
# # Accessible at: http://localhost:8000/product/del_name?name=phone (with DELETE method)
# @app.delete('/products/del_name/{name}')
# def delete_product_from_name(name:str,db:Session=Depends(get_db)):
#     """
#     Delete a product from inventory using its name.
#     Args:
#         name (str): Name of the product to delete (query parameter)
#     Returns:
#         Success message if deleted, error message if not found
#     """
#     # for i in range(len(products)):
#     #     if products[i].name==name:
#     #         del products[i]
#     #         return f"Item with named {name} deleted successfully."
#     #     return 'Product not found in the inventory, please check the name again.'
    
    
#     db_product = db.query(db_models.Product).filter(db_models.Product.name==name).first()
#     if db_product:
#         db.delete(db_product)
#         db.commit()
#         return f'Product named {name} deleted successfully'
#     else:
#         return f'There is no product named {name}, please try with id or check the name again.'
#     pass
    
