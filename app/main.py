from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Depends
from app.database import create_db_and_tables, SessionDep
from app.models import Driver, Car
from app import crud, schemas
from sqlmodel import select
from app.authorization import check_api_key

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="FleetRent API", lifespan=lifespan)

@app.get("/")
def home():
    return {"status": "FleetRent API is running successfully"}

@app.post("/drivers/", response_model=schemas.DriverResponse, tags=["Driver"])
def create_driver(driver: schemas.DriverCreate, db: SessionDep, _: str = Depends(check_api_key)):
    return crud.create_driver(db=db, driver_data=driver)

@app.get("/drivers/", response_model=list[schemas.DriverResponse], tags=["Driver"])
def read_drivers(db: SessionDep):
    drivers = db.exec(select(Driver)).all()
    return drivers

@app.post("/cars/", response_model=schemas.CarResponse, tags=["Car"])
def create_car(car: schemas.CarCreate, db: SessionDep, _: str = Depends(check_api_key)):
    return crud.create_car(db=db, car_data=car)

@app.get("/cars/", response_model=list[schemas.CarResponse], tags=["Car"])
def read_cars(db: SessionDep):
    cars = db.exec(select(Car)).all()
    return cars

@app.post("/shifts/start", response_model=schemas.ShiftResponse, tags=["Shift"])
def shift_start(payload: schemas.ShiftStart, db: SessionDep):
    car = crud.get_car(db, payload.car_id)
    driver = crud.get_driver(db, payload.driver_id)

    if not driver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The driver is not available")

    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The car is not available")
    if car.status == "active":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The car is in use")
    
    car.status = "active"
    return crud.start_driver_shift(db, driver_id=payload.driver_id, car_id=payload.car_id, start_mileage=car.current_mileage)

@app.put("/shifts/{shift_id}/end", response_model=schemas.ShiftResponse, tags=["Shift"])
def shift_end(shift_id: int, end_mileage: int, gross_earnings: float, fuel_cost: float, db: SessionDep):
    shift = crud.get_shift(db, shift_id)

    if not shift:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The shift doesn't exist")
    if shift.end_time is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Shift already ended")
    
    car = crud.get_car(db, shift.car_id)
    driver = crud.get_driver(db, shift.driver_id)
    
    if not driver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The driver is not available")
    
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The car is not available")
    if car.status != "active":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The car is not in use")
    
    if end_mileage < shift.start_mileage:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mileage can't be lower than before")
    
    net_profit = gross_earnings - (gross_earnings * driver.commission_rate) - fuel_cost

    return crud.end_driver_shift(
        db = db,
        shift = shift,
        car = car,
        end_mileage = end_mileage,
        gross_earnings = gross_earnings,
        fuel_cost = fuel_cost,
        net_profit = net_profit
    )
    
@app.get("/reports/monthly", response_model=schemas.MonthlyReportResponse, tags=["Report"])
def get_monthly_report(year: int, month: int, db: SessionDep, _: str = Depends(check_api_key)):
    return crud.get_monthly_report(db=db, year=year, month=month)