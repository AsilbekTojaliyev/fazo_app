from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_connect import database
from functions.universal_functions import get_in_db, new_item_db, product_reduction
from models.buy import Buys
from models.cart import Carts
from models.incomit import Incomes
from routes.login import get_current_user
from schemas.user import CreateUser

router_buy = APIRouter(prefix="/buys", tags=["Buys, operations"])


@router_buy.get("get_buys")
def get(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    if current_user.role == "admin":
        return db.query(Buys).all()
    raise HTTPException(400, "buni faqat admin ko'ra oladi !!!")


@router_buy.put("/confirmation_buys")
def confirmation(ident: int, status: bool, db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    if current_user.role == "admin":
        get_in_db(db, Buys, ident)
        db.query(Buys).filter(Buys.id == ident).update({
            Buys.status: status
        })
        db.commit()
        buy = db.query(Buys).filter(Buys.id == ident).first()
        price_all = 0
        carts = db.query(Carts).filter(Carts.buy_id == buy.id).all()
        if buy.status:
            for cart in carts:
                price_all += cart.price_source
                product_reduction(cart, db)
                db.query(Carts).filter(Carts.id == cart.id).delete()
                db.commit()
            
            new_incomit = Incomes(
                    user_id=buy.user_id,
                    price=price_all,
                    date_receipt=date.today()
                )
            new_item_db(db, new_incomit)

        raise HTTPException(200, "amaliyot muvaffaqiyatli")

    raise HTTPException(400, "faqat admin yangilay oladi !!!")
