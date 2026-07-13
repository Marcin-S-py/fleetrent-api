from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("FleetRent")

from app.database import create_db_and_tables
from app.routers import drivers, cars, shifts, reports

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="FleetRent API", lifespan=lifespan)
app.include_router(drivers.router)
app.include_router(cars.router)
app.include_router(shifts.router)
app.include_router(reports.router)

@app.get("/")
def home():
    return {"status": "FleetRent API is running successfully"}