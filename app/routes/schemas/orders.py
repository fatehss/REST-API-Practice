from pydantic import BaseModel
from typing import List
from .products import ProductGetResponse
class OrderPostRequest(BaseModel):
    user_id: int
    product_ids: list[int]


class OrderGetResponse(BaseModel):
    id: int
    user_id: int
    total_price: int
    status: str
    products: List[ProductGetResponse] | None = None

 # try and update the products in the order if possible
class OrderUpdate(BaseModel):
    product_ids: list[int]