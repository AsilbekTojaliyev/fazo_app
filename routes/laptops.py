from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from db_connect import database
from typing import List
from routes.login import get_current_active_user
from schemas.laptops import Create_laptop, Update_laptop
from functions.laptop import create_laptop, update_laptop, delete_laptop, get_laptop
from schemas.users import CreateUser

router_laptops = APIRouter(prefix="/Laptops", tags=["Laptops operations"])


@router_laptops.post('/create_laptops')
def create(forms: List[Create_laptop],
           db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    create_laptop(db, forms, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")


@router_laptops.get('/get_laptops')
def get_filter(page: int = 1, limit: int = 25, rom_size: int = 0,
               ram_size: int = 0, price: float = 0, brand: str = None,
               country: str = None, db: Session = Depends(database)):
    return get_laptop(price, brand, country, rom_size, ram_size, page, limit, db)


@router_laptops.put('/update_laptops')
def update(forms: List[Update_laptop],
           db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    update_laptop(db, forms, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")


@router_laptops.delete('/delete_laptops')
def delete(idents: List[int],
           db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    delete_laptop(db, idents, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")
