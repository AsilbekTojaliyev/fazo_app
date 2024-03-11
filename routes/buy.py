from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_connect import database
from models.buy import Buys
from routes.login import get_current_user
from schemas.user import CreateUser

router_buy = APIRouter(prefix="/buys", tags=["buys, operations"])


@router_buy.get("get_buys")
def get(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    if current_user.role == "admin":
        return db.query(Buys).all()
    raise HTTPException(400, "buni faqat admin ko'ra oladi !!!")


@router_buy.put("/confirmation_buys")
def confirmation(ident: int, status: bool, db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    if current_user.role == "admin":
        db.query(Buys).filter(Buys.id == ident).update({
            Buys.status: status
        })
        db.commit()
        raise HTTPException(200, "amaliyot muvaffaqiyatli")
    raise HTTPException(400, "faqat admin yangilay oladi !!!")
