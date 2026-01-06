from fastapi import FastAPI
from app.core.database import engine, Base
from app.auth.models import User

from app.auth.routes import router
from app.catalog.routes import router as catalog_router
from app.orders.routes import router as orders_router
from app.payments.routes import router as payments_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce Backend")

app.include_router(router)
app.include_router(catalog_router)
app.include_router(orders_router)
app.include_router(payments_router)
