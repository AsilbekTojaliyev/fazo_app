from enum import Enum
from pydantic import BaseModel, Field


class Source_type(str, Enum):
    laptop = "laptop"
    tablet = "tablet"
    phone = "phone"


class Get_one_product(BaseModel):
    name: Source_type
    ident: int = Field(..., gt=0)
