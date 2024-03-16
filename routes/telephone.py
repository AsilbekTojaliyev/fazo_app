from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, Depends, HTTPException
from db_connect import database
from typing import List
from models.telephone import Telephones
from routes.login import get_current_active_user
from schemas.telephone import Create_phone, Update_phone
from functions.telephone import create_phone, update_phone, delete_phone, get_telephone
from schemas.user import CreateUser

router_phones = APIRouter(prefix="/Phones", tags=["phones operations"])


@router_phones.post('/create_phones')
def create(forms: List[Create_phone],
           db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    create_phone(db, forms, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")


@router_phones.get("/get_random_phones")
def get_random(db: Session = Depends(database)):
    return db.query(Telephones).options(joinedload(Telephones.files)).order_by(func.random()).all()


@router_phones.get('/get_filter_phones')
def get(country: str = None, brand: str = None, price: int = 0,
        ram_size: int = 0, rom_size: int = 0,
        page: int = 1, limit: int = 25, db: Session = Depends(database)):
    return get_telephone(country, price, rom_size, ram_size, brand, page, limit, db)


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
