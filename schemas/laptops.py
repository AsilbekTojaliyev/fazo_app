from pydantic import BaseModel, Field
from datetime import date


class Create_laptop(BaseModel):
    description: str
    price: float
    year: int = Field(..., gt=0)
    brand: str
    screen_type: str
    weight: float
    country: str
    color: str
    ram_size: int
    rom_size: int
    display: float
    videocard: str
    rom_type: str
    processor: str
    discount: float
    count: int = Field(..., gt=0)
    discount_time: date


class Update_laptop(BaseModel):
    ident: int = Field(..., gt=0)
    description: str
    price: float
    year: int = Field(..., gt=0)
    brand: str
    screen_type: str
    weight: float
    country: str
    color: str
    ram_size: int
    rom_size: int
    display: float
    videocard: str
    rom_type: str
    processor: str
    discount: float
    count: int = Field(..., gt=0)
    discount_time: date
