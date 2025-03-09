from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Review
from app.schemas import ReviewPostRequest, ReviewGetResponse, ReviewUpdate

router = APIRouter()

def validate_rating(rating: int):
    if rating < 1 or rating > 5:
        raise ValueError("Rating must be between 1 and 5")
    
def validate_comment(comment: str):
    if len(comment) > 1000:
        raise ValueError("Comment must be less than 1000 characters")

@router.post("/reviews")
async def create_review(review: ReviewPostRequest, db: Session = Depends(get_db)):
    try:
        validate_rating(review.rating)
        validate_comment(review.comment)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    # TODO: Check if the user has ever bought the product
    # user_purchased_product = db.query(OrderItem).join(Order).filter(
    #     Order.user_id == review.user_id,
    #     OrderItem.product_id == review.product_id,
    #     Order.status.in_(["delivered", "shipped"])  # Only count completed orders
    # ).first()    
    # if not user_purchased_product:
    #     raise HTTPException(
    #         status_code=403, 
    #         detail="You can only review products you have purchased"
    #     )
    # TODO: Check if the user has already reviewed the product
    # user_reviewed_product = db.query(Review).filter(
    #     Review.user_id == review.user_id,
    #     Review.product_id == review.product_id
    # ).first()
    # if user_reviewed_product:
    #     raise HTTPException(status_code=403, detail="You can only review a product once")
    new_review = Review(
        user_id=review.user_id,
        product_id=review.product_id,
        rating=review.rating,
        comment=review.comment
    )
    db.add(new_review)
    db.commit()
    return ReviewGetResponse(
        id=new_review.id,
        user_id=new_review.user_id,
        product_id=new_review.product_id,
        rating=new_review.rating,
        comment=new_review.comment
    )


@router.get("/reviews/{review_id}")
async def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return ReviewGetResponse(
        id=review.id,
        user_id=review.user_id,
        product_id=review.product_id,
        rating=review.rating,
        comment=review.comment
    )
    
@router.put("/reviews/{review_id}")
async def update_review(review_id: int, review: ReviewUpdate, db: Session = Depends(get_db)):
    if not review.rating and not review.comment:
        raise HTTPException(status_code=422, detail="At least one field must be provided")
    
    try:
        if review.rating:
            validate_rating(review.rating)
        if review.comment:
            validate_comment(review.comment)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return ReviewGetResponse(review.id, review.user_id, review.product_id, review.rating, review.comment)

