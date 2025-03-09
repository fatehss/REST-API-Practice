from fastapi import FastAPI
from .routes import api_router
app = FastAPI()

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}