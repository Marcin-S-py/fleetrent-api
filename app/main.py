from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import create_db_and_tables, SessionDep
from app.models import Driver, Car
from sqlmodel import select

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="FleetRent API", lifespan=lifespan)

@app.get("/")
def home():
    return {"status": "FleetRent API is running successfully"}

@app.post("/drivers/", response_model=Driver)
def create_driver(driver: Driver, db: SessionDep):
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver

@app.get("/drivers/", response_model=list[Driver])
def read_drivers(db: SessionDep):
    drivers = db.exec(select(Driver)).all()
    return drivers

@app.post("/cars/", response_model=Car)
def create_car(car: Car, db: SessionDep):
    db.add(car)
    db.commit()
    db.refresh(car)
    return car

@app.get("/cars/", response_model=list[Car])
def read_cars(db: SessionDep):
    cars = db.exec(select(Car)).all()
    return cars