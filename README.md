# Product Catalog API

A RESTful API for managing product catalogs with MySQL database integration, built with FastAPI and SQLAlchemy. This application includes both a REST API server and an MCP (Model Context Protocol) server for AI agent integration.

## Features

- ✅ Full CRUD operations for products
- ✅ MySQL database integration via XAMPP
- ✅ Category-based filtering
- ✅ Stock availability tracking
- ✅ Pagination support
- ✅ Data validation with Pydantic
- ✅ MCP server for AI assistant integration
- ✅ Interactive API documentation (Swagger UI)

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **Database**: MySQL (via XAMPP)
- **ORM**: SQLAlchemy 2.0.23
- **Server**: Uvicorn 0.24.0
- **Validation**: Pydantic 2.5.0
- **MCP Integration**: FastMCP 0.2.0

## Prerequisites

- Python 3.8+
- XAMPP with MySQL running
- MySQL database named `product_catalog`

## Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database**
   - Start XAMPP and ensure MySQL is running
   - Create a database named `product_catalog`
   - The application will create the necessary tables automatically

## Database Configuration

The application connects to MySQL with the following default settings:
- **Host**: localhost
- **Port**: 3306
- **User**: root
- **Password**: (empty)
- **Database**: product_catalog

To modify the connection, update the `DATABASE_URL` in `main.py`.

## Running the Application

### Start the FastAPI server:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at: `http://127.0.0.1:8000`

### Access Interactive Documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | List all products (with filters) |
| GET | `/products/{id}` | Get a specific product |
| POST | `/products` | Create a new product |
| PUT | `/products/{id}` | Update a product |
| DELETE | `/products/{id}` | Delete a product |

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | Get all unique categories |

### Health & Info

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check (API + DB) |

## Usage Examples

### Create a Product

```bash
curl -X POST "http://127.0.0.1:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "price": 999.99,
    "description": "High-performance laptop",
    "category": "Electronics",
    "in_stock": true
  }'
```

### List Products with Filters

```bash
# Get all electronics
curl "http://127.0.0.1:8000/products?category=Electronics"

# Get products in stock
curl "http://127.0.0.1:8000/products?in_stock=true"

# With pagination
curl "http://127.0.0.1:8000/products?skip=0&limit=10"
```

### Get Product by ID

```bash
curl "http://127.0.0.1:8000/products/1"
```

### Update a Product

```bash
curl -X PUT "http://127.0.0.1:8000/products/1" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 899.99,
    "in_stock": true
  }'
```

### Delete a Product

```bash
curl -X DELETE "http://127.0.0.1:8000/products/1"
```

### Get All Categories

```bash
curl "http://127.0.0.1:8000/categories"
```

## Product Schema

```json
{
  "id": 1,
  "name": "Product Name",
  "price": 99.99,
  "description": "Product description",
  "category": "General",
  "in_stock": true
}
```

## MCP Server

The project includes an MCP server (`mcp_server.py`) that allows AI assistants to interact with the product catalog. It provides tools for:

- Listing products with filters
- Getting product details
- Creating new products
- Updating existing products
- Deleting products
- Searching products by category

## Development

### Project Structure

```
.
├── main.py              # FastAPI application
├── mcp_server.py        # MCP server for AI integration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Run in Development Mode

The `--reload` flag enables auto-reload on code changes:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Successful GET/PUT requests
- `201`: Successful POST (creation)
- `204`: Successful DELETE
- `404`: Resource not found
- `422`: Validation error
- `503`: Database unavailable

## License

This project is for educational purposes (Lab 2 assignment).

## Author

DSI32 - Mobile Development with Flutter

---

**Last Updated**: October 15, 2025
