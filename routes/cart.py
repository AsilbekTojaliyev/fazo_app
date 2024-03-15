from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_connect import database
from functions.cart import create_cart, delete_cart
from models.buy import Buys
from models.cart import Carts
from routes.login import get_current_user
from schemas.cart import Create_cart
from schemas.user import CreateUser

router_carts = APIRouter(
    prefix="/carts",
    tags=["Carts operations"]
)


@router_carts.get("/get_carts_all")
def get_all(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    if current_user.role == "admin":
        return db.query(Carts).all()
    else:
        raise HTTPException(400, "siz buni ko'ra olmaysiz, chunki siz admin emassiz")
    

@router_carts.get("/get_carts")
def get(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    buy = db.query(Buys).filter(Buys.user_id == current_user.id).first()
    if buy is not None:
        return db.query(Carts).filter(Carts.buy_id == buy.id).all()
    raise HTTPException(400, "siz hali savatga malumot qowmadingiz")


@router_carts.post("/create_carts")
def create(form: Create_cart = Depends(Create_cart), db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_user)):
    create_cart(form.source, form.source_id, current_user, db)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_carts.delete("/delete_cart")
def delete(ident: int = 0, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_user)):
    delete_cart(ident, current_user, db)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi")
