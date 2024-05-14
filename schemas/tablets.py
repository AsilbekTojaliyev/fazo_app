from datetime import date
from pydantic import BaseModel, Field


class Create_tablet(BaseModel):
    description: str
    brand: str
    screen_type: str
    color: str
    year: int = Field(..., gt=0)
    weight: float
    country: str
    price: float = Field(..., gt=0)
    ram_size: int = Field(..., gt=0)
    rom_size: int = Field(..., gt=0)
    display: float
    camera: int = Field(..., gt=0)
    self_camera: int = Field(..., gt=0)
    discount: int
    count: int = Field(..., gt=0)
    discount_time: date


class Update_tablet(BaseModel):
    ident: int = Field(..., gt=0)
    description: str
    brand: str
    screen_type: str
    year: int = Field(..., gt=0)
    weight: float
    country: str
    price: float = Field(..., gt=0)
    ram_size: int = Field(..., gt=0)
    rom_size: int = Field(..., gt=0)
    color: str
    display: float
    camera: int = Field(..., gt=0)
    self_camera: int = Field(..., gt=0)
    discount: float
    count: int = Field(..., gt=0)
    discount_time: date
