from fastapi import APIRouter, HTTPException, status
from app.database import SessionDep
from app import crud, schemas
import logging

router = APIRouter(
    prefix = "/shifts",
    tags = ["Shift"]
)

logger = logging.getLogger("FleetRent")

@router.post("/start", response_model=schemas.ShiftResponse)
def shift_start(payload: schemas.ShiftStart, db: SessionDep):
    car = crud.get_car(db, payload.car_id)
    driver = crud.get_driver(db, payload.driver_id)

    if not driver:
        logger.warning(f"Failed to start shift: Driver ID {payload.driver_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The driver is not available")

    if not car:
        logger.warning(f"Failed to start shift: Car ID {payload.car_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The car is not available")
    if car.status == "active":
        logger.warning(f"Failed to start shift: Car ID {payload.car_id} is already in use.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The car is in use")
    
    car.status = "active"
    logger.info(f"Shift started successfully for Driver ID {payload.driver_id} using Car ID {payload.car_id}.")
    return crud.start_driver_shift(db, driver_id=payload.driver_id, car_id=payload.car_id, start_mileage=car.current_mileage)

@router.put("/{shift_id}/end", response_model=schemas.ShiftResponse)
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
