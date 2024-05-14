from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from db_connect import database
from functions.universal_functions import get_in_db, new_item_db, product_reduction
from models.cart import Carts
from models.trade import Trades
from models.incomit import Incomes
from routes.login import get_current_user
from schemas.users import CreateUser

router_carts = APIRouter(prefix="/cart", tags=["Carts operations"])


@router_carts.get("/get_carts")
def get(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    if current_user.role == "admin":
        return db.query(Carts).options(joinedload(Carts.user)).all()
    raise HTTPException(400, "buni faqat admin ko'ra oladi !!!")


@router_carts.put("/confirmation_carts")
def confirmation(ident: int, status: bool,
                 db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    if current_user.role == "admin":
        get_in_db(db, Carts, ident)
        db.query(Carts).filter(Carts.id == ident).update({
            Carts.status: status
        })
        db.commit()
        cart = db.query(Carts).filter(Carts.id == ident).first()
        price_all = 0
        trades = db.query(Trades).filter(Trades.cart_id == Carts.id).all()
        if cart.status:
            for trade in trades:
                price_all += trade.price_source
                product_reduction(trade, db)
                db.query(Trades).filter(Trades.id == trade.id).delete()
                db.commit()
            
            new_incomit = Incomes(
                    user_id=cart.user_id,
                    price=price_all,
                    date_receipt=date.today()
                )
            new_item_db(db, new_incomit)

        raise HTTPException(200, "amaliyot muvaffaqiyatli")

    raise HTTPException(400, "faqat admin yangilay oladi !!!")
