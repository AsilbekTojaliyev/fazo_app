from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_connect import database
from functions.universal_functions import new_item_db, get_in_db
from models.brand import Brands
from routes.login import get_current_user
from schemas.users import CreateUser

router_brands = APIRouter(prefix="/brands", tags=["Brands operations"])


@router_brands.post("/create_brands")
def create(name: str, db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    if current_user.role == "admin":
        new_item = Brands(name=name)
        new_item_db(db, new_item)
    else:
        raise HTTPException(400, "siz bunday qila olmaysiz")
    raise HTTPException(200, "amaliyot muvaffaqiyatli")


@router_brands.put("/update_brands")
def update(ident: int, name: str, db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    if current_user.role == "admin":
        get_in_db(db, Brands, ident)
        db.query(Brands).filter(Brands.id == ident).update({Brands.name: name})
        db.commit()
    else:
        raise HTTPException(400, "siz bunday qila olmaysiz")
    raise HTTPException(200, "amaliyot muvaffaqiyatli")


@router_brands.delete("/delete_brands")
def delete(ident: int, db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    if current_user.role == "admin":
        get_in_db(db, Brands, ident)
        db.query(Brands).filter(Brands.id == ident).delete()
        db.commit()
    else:
        raise HTTPException(400, "siz bunday qila olmaysiz")
    raise HTTPException(200, "amaliyot muvaffaqiyatli")
