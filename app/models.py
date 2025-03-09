from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from .database import Base


from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin

@declarative_mixin
class TimestampMixin:
    time_now = datetime.now()
    created_at = Column(DateTime, default=time_now, nullable=False)
    updated_at = Column(DateTime, default=time_now, onupdate=time_now, nullable=False)

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(Enum("customer", "admin", name="user_role"), default="customer")
    password = Column(String, nullable=False)
    
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)

    reviews = relationship("Review", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")  # New relation


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(Enum("pending", "processing", "shipped", "delivered", "cancelled", name="order_status"), default="pending")

    user = relationship("User", back_populates="orders")
    payments = relationship("Payment", back_populates="order")
    order_items = relationship("OrderItem", back_populates="order")  # Fix: Now correctly references `OrderItem`


class OrderItem(Base, TimestampMixin):  # ✅ NEW TABLE for Many-to-Many relationship between Orders and Products
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False)  # Stores price at purchase time

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")


class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(Enum("credit_card", "paypal", "bank_transfer", name="payment_method"))
    status = Column(Enum("pending", "completed", "failed", name="payment_status"), default="pending")

    order = relationship("Order", back_populates="payments")


class Review(Base, TimestampMixin):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String)

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")


if __name__ == "__main__":
    print(Base.metadata)
