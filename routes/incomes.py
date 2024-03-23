from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_connect import database
from models.incomit import Incomes
from routes.login import get_current_user
from schemas.users import CreateUser

router_incomes = APIRouter(prefix="/Incomes", tags=["Incomes operations"])


@router_incomes.get("/get_incomes")
def get_incomes(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    if current_user.role == "admin":
        return db.query(Incomes).all()
    else:
        raise HTTPException(400, "faqat admin kora oladi")


@router_incomes.delete("delete_incomes")
def delete_income(idents: List[int], db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    if current_user.role == "admin":
        for ident in idents:
            db.query(Incomes).filter(Incomes.id == ident).delete()
            db.commit()
    else:
        raise HTTPException(400, "siz admin emassiz")
