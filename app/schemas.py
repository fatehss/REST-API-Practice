## schemas.py
## Purpose: Define Pydantic Models for API Schemas
## NOTE: this is not related to SQLAlchemy, it's just for the API and swagger UI docs

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):  # For a create user endpoint
    password: str

class UserGetResponse(UserBase):  # For a get user endpoint
    id: int

        

        