from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, Depends, HTTPException
from db_connect import database
from models.laptop import Laptops
from typing import List
from routes.login import get_current_active_user
from schemas.laptop import Create_laptop, Update_laptop
from functions.laptop import create_laptop, update_laptop, delete_laptop, get_laptop
from schemas.user import CreateUser
from sqlalchemy.sql.expression import func

router_laptop = APIRouter(prefix="/Laptops", tags=["laptops operations"])


@router_laptop.post('/create_laptops')
def create(forms: List[Create_laptop],
           db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    create_laptop(db, forms, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")


@router_laptop.get("/get_random_laptop")
def get_random_all(db: Session = Depends(database)):
    return db.query(Laptops).options(joinedload(Laptops.files)).order_by(func.random()).all()


@router_laptop.get('/get_laptops')
def get_filter(page: int = 1, limit: int = 25, rom_size: int = 0, year: int = 0,
               ram_size: int = 0, rom_type: str = None, price: int = 0, display: float = 0,
               processor: str = None, videocard: str = None, brand: str = None,
               country: str = None, db: Session = Depends(database)):
    return get_laptop(price, country, year, display, rom_type, rom_size, ram_size, processor, videocard, brand, page, limit, db)


@router_laptop.put('/update_laptops')
def update(forms: List[Update_laptop],
           db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    update_laptop(db, forms, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")


@router_laptop.delete('/delete_laptops')
def delete(idents: List[int],
           db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    delete_laptop(db, idents, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")
