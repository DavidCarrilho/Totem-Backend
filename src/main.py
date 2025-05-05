from fastapi import FastAPI

from src.core import database
from src.core.models import Base
from src.routes.stores import router as stores_router
from src.routes.products import router as products_router

Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="TotemPRO API"
)

app.include_router(stores_router)
app.include_router(products_router)