from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database configuration for XAMPP MySQL
DATABASE_URL = "mysql+pymysql://root@localhost:3306/product_catalog"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=3600,   # Recycle connections after 1 hour
    echo=False           # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


# SQLAlchemy ORM Model
class ProductModel(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), default="General")
    in_stock = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)


# Pydantic Models for API
class Product(BaseModel):
    """Product response model"""
    id: int
    name: str
    price: float
    description: Optional[str] = None
    category: str = "General"
    in_stock: bool = True
    
    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy


class ProductCreate(BaseModel):
    """Product creation model"""
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=500)
    category: str = Field(default="General", max_length=50)
    in_stock: bool = True


class ProductUpdate(BaseModel):
    """Product update model"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, max_length=50)
    in_stock: Optional[bool] = None


# FastAPI app initialization
app = FastAPI(
    title="Product Catalog API with MySQL",
    description="AI-ready product catalog API with XAMPP MySQL database integration",
    version="2.0.0"
)


# Dependency to get database session
def get_db():
    """Create database session for each request"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["Root"])
async def root():
    """API root endpoint"""
    return {
        "message": "Product Catalog API with MySQL",
        "docs": "/docs",
        "database": "XAMPP MySQL"
    }


@app.get("/products", response_model=List[Product], tags=["Products"])
async def list_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    in_stock: Optional[bool] = Query(None, description="Filter by stock status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    db: Session = Depends(get_db)
) -> List[Product]:
    """Retrieve products with optional filters and pagination."""
    query = db.query(ProductModel)
    
    # Apply filters
    if category:
        query = query.filter(ProductModel.category == category)
    if in_stock is not None:
        query = query.filter(ProductModel.in_stock == in_stock)
    
    # Apply pagination
    products = query.offset(skip).limit(limit).all()
    return products


@app.get("/products/{product_id}", response_model=Product, tags=["Products"])
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
) -> Product:
    """Retrieve a specific product by its identifier."""
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    
    return product


@app.post("/products", response_model=Product, status_code=201, tags=["Products"])
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
) -> Product:
    """Add a new product to the catalog."""
    # Create new product instance
    db_product = ProductModel(
        name=product.name,
        price=product.price,
        description=product.description,
        category=product.category,
        in_stock=product.in_stock
    )
    
    # Add to database
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product


@app.put("/products/{product_id}", response_model=Product, tags=["Products"])
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
) -> Product:
    """Update an existing product."""
    # Find product
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    
    # Update fields if provided
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    
    return db_product


@app.delete("/products/{product_id}", status_code=204, tags=["Products"])
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Delete a product from the catalog."""
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    
    db.delete(db_product)
    db.commit()
    
    return None


@app.get("/categories", tags=["Categories"])
async def list_categories(db: Session = Depends(get_db)):
    """Get all unique product categories."""
    categories = db.query(ProductModel.category).distinct().all()
    return {"categories": [cat[0] for cat in categories]}


@app.get("/health", tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """Check API and database health."""
    try:
        # Test database connection
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {str(e)}")
