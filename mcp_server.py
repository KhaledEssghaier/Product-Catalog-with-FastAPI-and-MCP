from typing import List, Optional
import httpx
from fastmcp import FastMCP

# Base URL for FastAPI server
FASTAPI_BASE_URL = "http://127.0.0.1:8000"

mcp = FastMCP(name="Product Catalog MCP Server with MySQL")


@mcp.tool()
async def list_products(
    category: Optional[str] = None,
    in_stock: Optional[bool] = None,
    limit: int = 100
) -> List[dict]:
    """
    List all products from the MySQL database with optional filters.
    
    Args:
        category: Filter products by category (e.g., 'Electronics', 'Accessories')
        in_stock: Filter by stock availability (True/False)
        limit: Maximum number of products to return (default: 100)
    """
    params = {"limit": limit}
    if category:
        params["category"] = category
    if in_stock is not None:
        params["in_stock"] = str(in_stock).lower()
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(f"{FASTAPI_BASE_URL}/products", params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"Failed to fetch products: {str(e)}"}


@mcp.tool()
async def get_product(product_id: int) -> dict:
    """
    Retrieve a single product by its ID from the MySQL database.
    
    Args:
        product_id: The unique identifier of the product
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(f"{FASTAPI_BASE_URL}/products/{product_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {"error": f"Product {product_id} not found"}
            return {"error": f"Failed to fetch product: {str(e)}"}
        except httpx.HTTPError as e:
            return {"error": f"Connection error: {str(e)}"}


@mcp.tool()
async def create_product(
    name: str,
    price: float,
    description: Optional[str] = None,
    category: str = "General",
    in_stock: bool = True
) -> dict:
    """
    Add a new product to the catalog.
    
    Args:
        name: Product name (required)
        price: Product price (must be positive)
        description: Product description (optional)
        category: Product category (default: 'General')
        in_stock: Stock availability (default: True)
    """
    product_data = {
        "name": name,
        "price": price,
        "description": description,
        "category": category,
        "in_stock": in_stock
    }
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(
                f"{FASTAPI_BASE_URL}/products",
                json=product_data
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"Failed to create product: {str(e)}"}


@mcp.tool()
async def update_product(
    product_id: int,
    name: Optional[str] = None,
    price: Optional[float] = None,
    description: Optional[str] = None,
    category: Optional[str] = None,
    in_stock: Optional[bool] = None
) -> dict:
    """
    Update an existing product in the catalog.
    
    Args:
        product_id: ID of the product to update
        name: New product name (optional)
        price: New product price (optional)
        description: New product description (optional)
        category: New product category (optional)
        in_stock: New stock status (optional)
    """
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if price is not None:
        update_data["price"] = price
    if description is not None:
        update_data["description"] = description
    if category is not None:
        update_data["category"] = category
    if in_stock is not None:
        update_data["in_stock"] = in_stock
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.put(
                f"{FASTAPI_BASE_URL}/products/{product_id}",
                json=update_data
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {"error": f"Product {product_id} not found"}
            return {"error": f"Failed to update product: {str(e)}"}
        except httpx.HTTPError as e:
            return {"error": f"Connection error: {str(e)}"}


@mcp.tool()
async def delete_product(product_id: int) -> dict:
    """
    Delete a product from the catalog.
    
    Args:
        product_id: ID of the product to delete
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.delete(f"{FASTAPI_BASE_URL}/products/{product_id}")
            response.raise_for_status()
            return {"success": True, "message": f"Product {product_id} deleted"}
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {"error": f"Product {product_id} not found"}
            return {"error": f"Failed to delete product: {str(e)}"}
        except httpx.HTTPError as e:
            return {"error": f"Connection error: {str(e)}"}


@mcp.tool()
async def get_categories() -> dict:
    """
    Get all unique product categories from the database.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(f"{FASTAPI_BASE_URL}/categories")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"Failed to fetch categories: {str(e)}"}


if __name__ == "__main__":
    mcp.run()
