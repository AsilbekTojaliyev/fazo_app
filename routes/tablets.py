from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from db_connect import database
from typing import List
from routes.login import get_current_active_user
from schemas.tablets import Create_tablet, Update_tablet
from functions.tablet import create_tablet, update_tablet, delete_tablet, get_tablet
from schemas.users import CreateUser

router_planshets = APIRouter(prefix="/Tablets", tags=["Tablets operations"])


@router_planshets.post('/create_tablets')
def create(forms: List[Create_tablet],
           db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    create_tablet(db, forms, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")


@router_planshets.get('/get_tablets')
def get(page: int = 1, limit: int = 25, rom_size: int = 0, ram_size: int = 0,
        price: int = 0, country: str = None, db: Session = Depends(database)):
    return get_tablet(price, country, rom_size, ram_size, page, limit, db)


@router_planshets.put('/update_tablets')
def update(forms: List[Update_tablet],
           db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    update_tablet(db, forms, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")


@router_planshets.delete('/delete_tablets')
def delete(idents: List[int],
           db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    delete_tablet(db, idents, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")
