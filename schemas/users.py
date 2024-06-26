from pydantic import BaseModel, validator
from models.user import Users
from db_connect import SessionLocal
from fastapi import HTTPException

db = SessionLocal()


class CreateUser(BaseModel):
    name: str
    username: str
    password: str
    phone_number: str

    @validator('phone_number')
    def number_validate(cls, num):
        if len(num) < 9:
            raise HTTPException(400, "telefon raqam 9 ta belgidan kam bo'lmasligi kerak")
        return num

    @validator('username')
    def username_validate(cls, username):
        validate_my = db.query(Users).filter(
            Users.username == username,
        ).count()

        if validate_my != 0:
            raise HTTPException(400, 'This login has already been registered !!!')
        return username

    @validator('password')
    def password_validate(cls, password):
        if len(password) < 8:
            raise HTTPException(400, 'Password should not be less than 8 characters')
        return password
# 1


class UpdateUser(BaseModel):
    name: str
    username: str
    password: str
    phone_number: str

    @validator('phone_number')
    def number_validate(cls, num):
        if len(num) < 9:
            raise HTTPException(400, "telefon raqam 9 ta belgidan kam bo'lmasligi kerak")
        return num

    @validator('password')
    def password_validate(cls, password):
        if len(password) < 8:
            raise HTTPException(400, 'Password should not be less than 8 characters')
        return password


