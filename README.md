# Flask Inventory Management System

A RESTful API built with Flask for managing product inventory with external API integration.

## Features

- **Full CRUD Operations**: Create, Read, Update, Delete products
- **Product Search**: Search products by name
- **Category Filtering**: Filter products by category
- **Product Statistics**: Get inventory statistics
- **External API Integration**: Fetch product data from OpenFoodFacts API
- **Comprehensive Testing**: Complete test suite with pytest
- **CLI Interface**: Command-line interface for easy interaction

## Project Structure

```
inventory-management-system/
├── app.py                    # Main Flask application
├── models/                   # Database models
│   └── inventory_model.py
├── controllers/              # Route controllers
│   └── inventory_controller.py
├── services/                 # External services
│   └── external_api_service.py
├── views/                    # User interfaces
│   └── cli_view.py
├── tests/                    # Test suite
│   └── test_app.py
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── .env                     # Environment variables
└── README.md               # This file
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd inventory-management-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (optional):
```bash
export DATABASE_URL="sqlite:///inventory.db"
export SECRET_KEY="your-secret-key"
```

## Running the Application

### Development Server
```bash
python app.py
```
The application will be available at `http://localhost:5000`

### CLI Interface
```bash
python -m views.cli_view
```

## API Documentation

### Base URL
```
http://localhost:5000/products
```

### Endpoints

#### GET /products
Retrieve all products
```bash
curl -X GET http://localhost:5000/products
```

#### GET /products/<id>
Retrieve a specific product by ID
```bash
curl -X GET http://localhost:5000/products/1
```

#### POST /products
Create a new product
```bash
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d &#x27;{
    "name": "Milk",
    "category": "Dairy",
    "price": 2.99,
    "quantity": 50,
    "barcode": "1234567890123"
  }&#x27;
```

#### PATCH /products/<id>
Update a product
```bash
curl -X PATCH http://localhost:5000/products/1 \
  -H "Content-Type: application/json" \
  -d &#x27;{
    "price": 3.49
  }&#x27;
```

#### DELETE /products/<id>
Delete a product
```bash
curl -X DELETE http://localhost:5000/products/1
```

#### GET /products/search?name=<query>
Search products by name
```bash
curl -X GET "http://localhost:5000/products/search?name=milk"
```

#### GET /products?category=<category>
Filter products by category
```bash
curl -X GET "http://localhost:5000/products?category=Dairy"
```

#### GET /products/stats
Get inventory statistics
```bash
curl -X GET http://localhost:5000/products/stats
```

#### GET /products/fetch/<barcode>
Fetch product data from external API
```bash
curl -X GET http://localhost:5000/products/fetch/1234567890123
```

#### POST /products/fetch
Save fetched product to database
```bash
curl -X POST http://localhost:5000/products/fetch \
  -H "Content-Type: application/json" \
  -d &#x27;{
    "barcode": "1234567890123"
  }&#x27;
```

## Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest tests/ --cov=app --cov=models --cov=controllers --cov=services
```

## Git Workflow

This project uses a feature branch workflow:

1. Create a new feature branch:
```bash
git checkout -b feature/crud
```

2. Make changes and commit:
```bash
git add .
git commit -m "Implement CRUD operations"
```

3. Push to remote:
```bash
git push origin feature/crud
```

4. Create a pull request and merge to main branch

## Dependencies

- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- Flask-Migrate: Database migrations
- requests: HTTP client for external API
- pytest: Testing framework
- python-dotenv: Environment variable management

## Environment Variables

- `DATABASE_URL`: Database connection string (default: sqlite:///inventory.db)
- `SECRET_KEY`: Flask secret key (default: dev-secret-key)

## License

This project is licensed under the MIT License.