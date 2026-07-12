from sqlmodel import SQLModel, Field
from datetime import datetime

class Driver(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    commission_rate: float
    is_active: bool = Field(default=True)

class Car(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    brand: str
    model: str
    license_plate: str
    fuel_card_number: str
    current_mileage: int
    status: str = Field(default="available")

class Shift(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    driver_id: int = Field(foreign_key="driver.id")
    car_id: int = Field(foreign_key="car.id")
    start_time: datetime
    start_mileage: int
    end_time: datetime | None = None
    end_mileage: int | None = None
    gross_earnings: float | None = None
    fuel_cost: float | None = None
    net_company_profit: float | None = None