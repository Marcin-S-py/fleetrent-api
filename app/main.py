from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from app.database import create_db_and_tables, SessionDep
from app.models import Driver, Car, Shift
from sqlmodel import select
from datetime import datetime

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

@app.post("/shifts/start", response_model=Shift)
def shift_start(driver_id: int, car_id: int, db: SessionDep):
    start_time = datetime.now()

    car = db.get(Car, car_id)
    driver = db.get(Driver, driver_id)

    if not driver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The driver is not available")

    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The car is not available")
    if car.status == "active":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The car is in use")
    
    car.status = "active"
    new_shift = Shift(driver_id=driver_id, car_id=car_id, start_time=start_time, start_mileage=car.current_mileage)

    db.add(new_shift)
    db.commit()
    db.refresh(new_shift)
    return new_shift

@app.put("/shifts/{shift_id}/end", response_model=Shift)
def shift_end(shift_id: int, end_mileage: int, gross_earnings: float, fuel_cost: float, db: SessionDep):
    end_time = datetime.now()

    shift = db.get(Shift, shift_id)

    if not shift:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The shift doesn't exist")
    if shift.end_time is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Shift already ended")
    
    car = db.get(Car, shift.car_id)
    driver = db.get(Driver, shift.driver_id)
    
    if not driver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The driver is not available")
    
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The car is not available")
    if car.status != "active":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The car is not in use")
    
    if end_mileage < shift.start_mileage:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mileage can't be lower than before")
    
    car.status = "available"
    car.current_mileage = end_mileage

    shift.net_company_profit = gross_earnings - (gross_earnings * driver.commission_rate) - fuel_cost
    shift.end_time = end_time
    shift.end_mileage = end_mileage
    shift.gross_earnings = gross_earnings
    shift.fuel_cost = fuel_cost

    db.commit()
    db.refresh(shift)
    return shift
    
