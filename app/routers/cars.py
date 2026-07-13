from fastapi import APIRouter, Depends
from sqlmodel import select
from app.database import SessionDep
from app.models import Car
from app import crud, schemas
from app.authorization import check_api_key
import logging

router = APIRouter(
    prefix = "/cars",
    tags = ["Car"]
)

logger = logging.getLogger("FleetRent")

@router.post("/", response_model=schemas.CarResponse)
def create_car(car: schemas.CarCreate, db: SessionDep, _: str = Depends(check_api_key)):
    new_car = crud.create_car(db=db, car_data=car)
    logger.info(f"Car registered successfully: ID {new_car.id}, Plate {new_car.license_plate}")
    return new_car

@router.get("/", response_model=list[schemas.CarResponse])
def read_cars(db: SessionDep):
    cars = db.exec(select(Car)).all()
    logger.info("Car list checked successfully.")
    return cars