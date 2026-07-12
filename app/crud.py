from sqlalchemy.orm import Session
from app.models import Driver, Car, Shift
from app.schemas import DriverCreate, CarCreate
from datetime import datetime
from sqlalchemy import func
from sqlmodel import select

def get_driver(db: Session, driver_id: int):
    return db.get(Driver, driver_id)

def create_driver(db: Session, driver_data: DriverCreate):
    db_driver = Driver(**driver_data.model_dump())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver

def get_car(db: Session, car_id: int):
    return db.get(Car, car_id)

def create_car(db: Session, car_data: CarCreate):
    db_car = Car(**car_data.model_dump())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

def get_shift(db: Session, shift_id: int):
    return db.get(Shift, shift_id)

def start_driver_shift(db: Session, driver_id: int, car_id: int, start_mileage: int):
    db_shift = Shift(
        driver_id = driver_id,
        car_id = car_id,
        start_time = datetime.now(),
        start_mileage = start_mileage
    )

    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    return db_shift

def end_driver_shift(db: Session, shift: Shift, car: Car, end_mileage: int, gross_earnings: float, fuel_cost: float, net_profit: float):
    car.status = "available"
    car.current_mileage = end_mileage

    shift.end_time = datetime.now()
    shift.end_mileage = end_mileage
    shift.gross_earnings = gross_earnings
    shift.fuel_cost = fuel_cost
    shift.net_company_profit = net_profit

    db.commit()
    db.refresh(shift)
    return shift

def get_monthly_report(db: Session, year: int, month: int):
    statement = select(
        func.sum(Shift.gross_earnings),
        func.sum(Shift.fuel_cost),
        func.sum(Shift.net_company_profit)
    ).where(
        func.extract("year", Shift.end_time) == year,
        func.extract("month", Shift.end_time) == month
    )

    result = db.exec(statement).first()

    gross = result[0] if result and result[0] is not None else 0.0
    fuel = result[1] if result and result[1] is not None else 0.0
    net = result[2] if result and result[2] is not None else 0.0

    return{
        "year": year,
        "month": month,
        "total_gross_earnings": gross,
        "total_fuel_cost": fuel,
        "net_company_profit": net
    }