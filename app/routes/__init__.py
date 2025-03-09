from .users import router as users_router
from .products import router as products_router
from .reviews import router as reviews_router
from .orders import router as orders_router
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(users_router)
api_router.include_router(products_router)
api_router.include_router(reviews_router)
api_router.include_router(orders_router)
