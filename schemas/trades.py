from enum import Enum
from pydantic import BaseModel, Field


class Source_type(str, Enum):
    laptop = "laptop"
    tablet = "tablet"
    phone = "phone"


class Create_trade(BaseModel):
    source: Source_type
    source_id: int = Field(..., gt=0)


