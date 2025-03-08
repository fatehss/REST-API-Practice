## models.py
## Purpose: Define SQLAlchemy Database Models for Alembic Migrations
## 

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(Enum("customer", "admin", name="user_role"), default="customer")

    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

    reviews = relationship("Review", back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(Enum("pending", "shipped", "delivered", "cancelled", name="order_status"), default="pending")

    user = relationship("User", back_populates="orders")
    payments = relationship("Payment", back_populates="order")
    order_items = relationship("OrderItem", back_populates="order")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(Enum("credit_card", "paypal", "bank_transfer", name="payment_method"))
    status = Column(Enum("pending", "completed", "failed", name="payment_status"), default="pending")

    order = relationship("Order", back_populates="payments")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String)

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")


if __name__ == "__main__":
    # print(User.metadata)
    print(Base.metadata)