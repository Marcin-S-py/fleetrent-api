from fastapi import APIRouter, Depends
from sqlmodel import select
from app.database import SessionDep
from app.models import Car
from app import crud, schemas
from app.authorization import check_api_key

router = APIRouter(
    prefix = "/cars",
    tags = ["Car"]
)

@router.post("/", response_model=schemas.CarResponse)
def create_car(car: schemas.CarCreate, db: SessionDep, _: str = Depends(check_api_key)):
    return crud.create_car(db=db, car_data=car)

@router.get("/", response_model=list[schemas.CarResponse])
def read_cars(db: SessionDep):
    cars = db.exec(select(Car)).all()
    return cars