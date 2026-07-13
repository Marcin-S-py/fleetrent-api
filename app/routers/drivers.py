from fastapi import APIRouter, Depends
from sqlmodel import select
from app.database import SessionDep
from app.models import Driver
from app import crud, schemas
from app.authorization import check_api_key
import logging

router = APIRouter(
    prefix = "/drivers",
    tags = ["Driver"]
)

logger = logging.getLogger("FleetRent")

@router.post("/", response_model=schemas.DriverResponse)
def create_driver(driver: schemas.DriverCreate, db: SessionDep, _: str = Depends(check_api_key)):
    new_driver = crud.create_driver(db=db, driver_data=driver)
    logger.info(f"Driver registered successfully: ID {new_driver.id}, Name: {new_driver.first_name} {new_driver.last_name}")
    return new_driver

@router.get("/", response_model=list[schemas.DriverResponse])
def read_drivers(db: SessionDep):
    drivers = db.exec(select(Driver)).all()
    logger.info("Driver list checked successfully.")
    return drivers