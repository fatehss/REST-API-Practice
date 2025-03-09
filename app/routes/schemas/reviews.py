from pydantic import BaseModel

class ReviewBase(BaseModel):
    user_id: int
    product_id: int
    rating: int
    comment: str

class ReviewGetResponse(ReviewBase):
    id: int
    user_id: int
    product_id: int
    rating: int
    comment: str

class ReviewUpdate(ReviewBase):
    rating: int | None = None
    comment: str | None = None
