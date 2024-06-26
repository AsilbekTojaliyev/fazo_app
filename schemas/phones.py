from datetime import date
from pydantic import BaseModel, Field


class Create_phone(BaseModel):
    description: str
    brand: str
    year: int = Field(..., gt=0)
    country: str
    model: str
    price: float = Field(..., gt=0)
    discount: int
    count: int = Field(..., gt=0)
    discount_time: date
    weight: float
    ram_size: int = Field(..., gt=0)
    rom_size: int = Field(..., gt=0)
    color: str
    battery: int = Field(..., gt=0)
    display: float
    camera: int = Field(..., gt=0)
    self_camera: int = Field(..., gt=0)


class Update_phone(BaseModel):
    ident: int = Field(..., gt=0)
    year: int = Field(..., gt=0)
    weight: float
    country: str
    description: str
    price: float = Field(..., gt=0)
    brand: str
    model: str
    ram_size: int = Field(..., gt=0)
    rom_size: int = Field(..., gt=0)
    color: str
    battery: int = Field(..., gt=0)
    display: float
    camera: int = Field(..., gt=0)
    self_camera: int = Field(..., gt=0)
    discount: float
    count: int = Field(..., gt=0)
    discount_time: date
