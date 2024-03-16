from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, Depends, HTTPException
from db_connect import database
from models.planshet import Planshets
from typing import List
from routes.login import get_current_active_user
from schemas.planshet import Create_planshet, Update_planshet
from functions.planshet import create_planshet, update_planshet, delete_planshet, get_planshet
from schemas.user import CreateUser

router_planshets = APIRouter(prefix="/Planshets", tags=["Planshets operations"])


@router_planshets.post('/create_planshets')
def create(forms: List[Create_planshet],
           db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    create_planshet(db, forms, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")


@router_planshets.get("/get_random_planshets")
def get_random(db: Session = Depends(database)):
    return db.query(Planshets).options(joinedload(Planshets.files)).order_by(func.random()).all()


@router_planshets.get('/get_filter_planshets')
def get(page: int = 1, limit: int = 25, rom_size: int = 0, ram_size: int = 0,
        price: int = 0, brand: str = None, country: str = None, db: Session = Depends(database)):
    return get_planshet(price, country, rom_size, ram_size, brand, page, limit, db)


@router_planshets.put('/update_planshets')
def update(forms: List[Update_planshet],
           db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    update_planshet(db, forms, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")


@router_planshets.delete('/delete_planshets')
def delete(idents: List[int],
           db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    delete_planshet(db, idents, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")
