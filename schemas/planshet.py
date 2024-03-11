from datetime import date
from pydantic import BaseModel, Field


class Create_planshet(BaseModel):
    name: str
    category_id: int = Field(..., gt=0)
    brand: str
    screen_type: str
    color: str
    year: int = Field(..., gt=0)
    weight: float
    country: str
    price: int = Field(..., gt=0)
    ram_size: int = Field(..., gt=0)
    rom_size: int = Field(..., gt=0)
    display: float
    camera: int = Field(..., gt=0)
    self_camera: int = Field(..., gt=0)
    discount: int
    count: int = Field(..., gt=0)
    discount_time: date


class Update_planshet(BaseModel):
    ident: int = Field(..., gt=0)
    name: str
    category_id: int = Field(..., gt=0)
    brand: str
    screen_type: str
    year: int = Field(..., gt=0)
    weight: float
    country: str
    price: int = Field(..., gt=0)
    ram_size: int = Field(..., gt=0)
    rom_size: int = Field(..., gt=0)
    color: str
    display: float
    camera: int = Field(..., gt=0)
    self_camera: int = Field(..., gt=0)
    discount: int
    count: int = Field(..., gt=0)
    discount_time: date
