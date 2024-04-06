from fastapi import APIRouter, Depends, HTTPException
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


@router_trades.get("/get_all_trades")
def get_all(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    if current_user.role == "admin":
        return db.query(Trades).all()
    else:
        raise HTTPException(400, "siz buni ko'ra olmaysiz, chunki siz admin emassiz")
    

@router_trades.get("/get_trades")
def get(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    cart = db.query(Carts).filter(Carts.user_id == current_user.id).first()
    if cart is not None:
        result = db.query(Laptops).options(joinedload(Laptops.files)).all()
        result += db.query(Tablets).options(joinedload(Tablets.files)).all()
        result += db.query(Phones).options(joinedload(Phones.files)).all()
        return db.query(Trades).options(
            joinedload(Trades.laptop), joinedload(Trades.phone), joinedload(Trades.tablet)).filter(
            Trades.cart_id == cart.id).all()
    raise HTTPException(400, "siz hali savatga malumot qowmadingiz")


@router_trades.post("/create_trades")
def create(form: Create_trade = Depends(Create_trade), db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_user)):
    create_trade(form.source, form.source_id, current_user, db)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_trades.delete("/delete_trades")
def delete(ident: int = 0, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_user)):
    delete_trade(ident, current_user, db)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi")
