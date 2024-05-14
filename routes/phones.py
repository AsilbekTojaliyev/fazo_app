from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from db_connect import database
from typing import List
from routes.login import get_current_active_user
from schemas.phones import Create_phone, Update_phone
from functions.phone import create_phone, update_phone, delete_phone, get_phone
from schemas.users import CreateUser

router_phones = APIRouter(prefix="/Phones", tags=["Phones operations"])


@router_phones.post('/create_phones')
def create(forms: List[Create_phone],
           db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    create_phone(db, forms, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")


@router_phones.get('/get_phones')
def get(country: str = None, price: int = 0, brand: str = None,
        ram_size: int = 0, rom_size: int = 0,
        page: int = 1, limit: int = 25, db: Session = Depends(database)):
    return get_phone(brand, country, price, rom_size, ram_size, page, limit, db)


@router_phones.put('/update_phones')
def update(forms: List[Update_phone],
           db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    update_phone(db, forms, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")


@router_phones.delete('/delete_phones')
def delete(idents: List[int],
           db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    delete_phone(db, idents, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")
