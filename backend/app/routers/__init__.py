from fastapi import APIRouter
from app.routers import dashboard, fare, history, pulse, settings, tariff, trips

api = APIRouter(prefix="/api")
for r in (dashboard, trips, tariff, fare, history, settings, pulse):
    api.include_router(r.router)
