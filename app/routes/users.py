from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.models import User, Review, Order
from sqlalchemy.orm import Session
from .schemas.users import UserBase, UserCreate, UserGetResponse, UserUpdate
import bcrypt
router = APIRouter()


@router.post("/users")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")
    
    # Hash the password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Create a new user
    new_user = User(name=user.name, email=user.email, password=hashed_password)
    
    # Add the user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # reload the user with the ID
    
    return UserGetResponse(id=new_user.id, name=new_user.name, email=new_user.email)
    
@router.get("/users/{user_id}", response_model=UserGetResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserGetResponse(id=user.id, name=user.name, email=user.email)

@router.put("/users/{user_id}", response_model=UserGetResponse)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the user
    if user.name:
        db_user.name = user.name
    if user.password:
        db_user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.commit()
    db.refresh(db_user)
    
    return UserGetResponse(id=db_user.id, name=db_user.name, email=db_user.email)

@router.delete("/users/{user_id}", status_code=200)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}


# @router.get("/users/{user_id}/reviews", response_model=list[Review])
# async def get_user_reviews(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user.reviews

# @router.get("/users/{user_id}/orders", response_model=list[Order])
# async def get_user_orders(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user.orders
