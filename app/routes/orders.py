from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Order, OrderItem, Product
from app.schemas import OrderPostRequest, OrderGetResponse, OrderUpdate

router = APIRouter()

@router.post("/orders")
async def create_order(order_data: OrderPostRequest, db: Session = Depends(get_db)):
    try:
        # Fetch all products in one query instead of multiple queries
        product_ids = order_data.product_ids
        products = db.query(Product).filter(Product.id.in_(product_ids)).all()
        
        # Check if all products exist
        found_product_ids = {product.id for product in products}
        missing_product_ids = set(product_ids) - found_product_ids
        if missing_product_ids:
            raise HTTPException(
                status_code=404, 
                detail=f"Products not found: {missing_product_ids}"
            )
        
        # Create a product lookup dictionary
        product_map = {product.id: product for product in products}
        
        # Calculate total price
        total_price = sum(product_map[product_id].price for product_id in product_ids)
        
        # Create order with correct total price from the start
        new_order = Order(
            user_id=order_data.user_id,
            total_price=total_price,
            status="pending"
        )
        db.add(new_order)
        db.flush()
        
        # Create order items
        for product_id in product_ids:
            product = product_map[product_id]
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product_id,
                quantity=1,
                price_at_purchase=product.price
            )
            db.add(order_item)
        
        # Commit everything at once
        db.commit()
        
        return OrderGetResponse(
            id=new_order.id,
            user_id=new_order.user_id,
            total_price=total_price,
            status=new_order.status
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/orders/{order_id}")
async def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderGetResponse(
        id=order.id,
        user_id=order.user_id,
        total_price=order.total_price,
        status=order.status
    )

@router.put("/orders/{order_id}")
async def update_order(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # delete order items for that order
    db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()

    # create new order items
    for product_id in order_data.product_ids:
        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=1,
            price_at_purchase=0
        )
        db.add(order_item)
    
