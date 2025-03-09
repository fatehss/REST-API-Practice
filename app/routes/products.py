from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product
from .schemas.products import ProductBase, ProductGetResponse, ProductUpdate

router = APIRouter()

def validate_product_name(name: str):
    if len(name) <= 3:
        raise ValueError("Name must be at least 3 characters")
def validate_product_price(price: float):
    if price <= 0:
        raise ValueError("Price must be greater than 0")
def validate_product_description(description: str):
    if len(description) <= 10:
        raise ValueError("Description must be at least 10 characters")


@router.post("/products", response_model=ProductGetResponse)
async def create_product(product: ProductBase, db: Session = Depends(get_db)):
    validate_product_name(product.name)
    validate_product_price(product.price)
    validate_product_description(product.description)
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return ProductGetResponse(id=db_product.id, name=db_product.name, price=db_product.price, description=db_product.description)


@router.get("/products/{product_id}", response_model=ProductGetResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductGetResponse(id=db_product.id, name=db_product.name, price=db_product.price, description=db_product.description)


@router.put("/products/{product_id}", response_model=ProductGetResponse)
async def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.description:
        validate_product_description(product.description)
    if product.price:
        validate_product_price(product.price)
    db_product.description = product.description
    db_product.price = product.price
    db.commit()
    db.refresh(db_product)
    return ProductGetResponse(id=db_product.id, name=db_product.name, price=db_product.price, description=db_product.description)


@router.delete("/products/{product_id}", status_code=200)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
