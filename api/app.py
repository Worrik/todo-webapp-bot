from fastapi import FastAPI
from api.routers import todos


app = FastAPI()
app.include_router(todos.router, tags=["Todo"])
