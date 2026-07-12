from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CarBase(BaseModel):
    brand: str
    model: str
    license_plate: str
    fuel_card_number: str

    class Config:
        from_attributes = True

class CarCreate(CarBase):
    current_mileage: int

    class Config:
        from_attributes = True

class DriverBase(BaseModel):
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class DriverCreate(DriverBase):
    commission_rate: float

    class Config:
        from_attributes = True

class ShiftStart(BaseModel):
    driver_id: int
    car_id: int

    class Config:
        from_attributes = True

class DriverResponse(DriverBase):
    id: int
    commission_rate: float

    class Config:
        from_attributes = True

class CarResponse(CarBase):
    id: int
    status: str
    current_mileage: int

    class Config:
        from_attributes = True

class ShiftResponse(BaseModel):
    id: int
    driver_id: int
    car_id: int
    start_time: datetime
    start_mileage: int
    end_time: Optional[datetime] = None
    end_mileage: Optional[int] = None
    gross_earnings: Optional[float] = None
    fuel_cost: Optional[float] = None
    net_company_profit: Optional[float] = None

    class Config:
        from_attributes = True