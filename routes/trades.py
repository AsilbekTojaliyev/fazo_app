import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload
from db_connect import database
from functions.trade import create_trade, delete_trade
from models.cart import Carts
from models.trade import Trades
from models.laptop import Laptops
from models.phone import Phones
from models.tablet import Tablets
from routes.login import get_current_user
from schemas.trades import Create_trade
from schemas.users import CreateUser

router_trades = APIRouter(
    prefix="/trade",
    tags=["Trades operations"]
)


@router_trades.get("/get_trades")
def get_trades(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    cart = db.query(Carts).filter(Carts.user_id == current_user.id).first()
    return db.query(Trades).filter(Trades.cart_id == cart.id).order_by(desc(Trades.id)).all()


@router_trades.get("/get_trades_product")
def get(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    cart = db.query(Carts).filter(Carts.user_id == current_user.id).first()
    if cart is not None:
        user_trades = db.query(Trades).filter(Trades.cart_id == cart.id).all()
        products = []
        for trade in user_trades:
            products += db.query(Laptops).options(joinedload(Laptops.files)).filter(
                Laptops.name == trade.source, Laptops.id == trade.source_id).all()

            products += db.query(Tablets).options(joinedload(Tablets.files)).filter(
                Tablets.name == trade.source, Tablets.id == trade.source_id).all()

            products += db.query(Phones).options(joinedload(Phones.files)).filter(
                Phones.name == trade.source, Phones.id == trade.source_id).all()
        random.shuffle(products)
        return products
    raise HTTPException(400, "siz hali savatga malumot qowmadingiz")


@router_trades.post("/create_trades")
def create(form: Create_trade = Depends(Create_trade), db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_user)):
    create_trade(form.source, form.source_id, current_user, db)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_trades.delete("/delete_trades")
def delete(form: Create_trade = Depends(Create_trade), delete_all: bool = False, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_user)):
    delete_trade(delete_all, form.source, form.source_id, current_user, db)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi")
