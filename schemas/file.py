from enum import Enum
from typing import List
from fastapi import UploadFile
from pydantic import BaseModel, Field


class Source_type(str, Enum):
    laptop = "laptop"
    planshet = "planshet"
    telephone = "telephone"


class Create_file(BaseModel):
    new_files: List[UploadFile]
    source: Source_type
    source_id: int = Field(..., gt=0)
