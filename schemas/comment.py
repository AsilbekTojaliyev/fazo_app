from fastapi import HTTPException
from pydantic import BaseModel, Field, validator


class Create_comment(BaseModel):
    text: str
    source: str
    source_id: int = Field(..., gt=0)

    @validator("source")
    def source_validate(cls, source):
        s = ["laptop", "planshet", "telephone"]
        if source.lower() not in s:
            raise HTTPException(400, "siz mavjud bo'lmagan categoriya tanladingiz!")
        return source
