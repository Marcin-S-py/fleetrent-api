from fastapi import APIRouter, Depends
from sqlmodel import select
from app.database import SessionDep
from app.models import Driver
from app import crud, schemas
from app.authorization import check_api_key

router = APIRouter(
    prefix = "/drivers",
    tags = ["Driver"]
)

@router.post("/", response_model=schemas.DriverResponse)
def create_driver(driver: schemas.DriverCreate, db: SessionDep, _: str = Depends(check_api_key)):
    return crud.create_driver(db=db, driver_data=driver)

@router.get("/", response_model=list[schemas.DriverResponse])
def read_drivers(db: SessionDep):
    drivers = db.exec(select(Driver)).all()
    return drivers