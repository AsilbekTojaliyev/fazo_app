from pydantic import BaseModel, Field


class Create_category(BaseModel):
    name: str
    link: str


class Update_category(BaseModel):
    ident: int = Field(..., gt=0)
    name: str
    link: str
