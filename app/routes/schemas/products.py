from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str
    price: float


class ProductGetResponse(ProductBase):
    id: int

class ProductUpdate(BaseModel):
    """
    Update a product. I don't want to allow the user to update the name.
    """
    description: str | None = None
    price: float | None = None