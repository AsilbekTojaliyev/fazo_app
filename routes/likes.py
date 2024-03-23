from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_connect import database
from functions.like import create_like, delete_like
from models.like import Likes
from routes.login import get_current_user
from schemas.likes import Create_like
from schemas.users import CreateUser

router_likes = APIRouter(
    prefix="/likes",
    tags=["Likes operations"]
)


@router_likes.get("/get_for_admin")
def get(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    if current_user.role == "admin":
        return db.query(Likes).all()
    else:
        raise HTTPException(400, "sizga mumkin emas")


@router_likes.get("/get_likes")
def get(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    return db.query(Likes).filter(Likes.user_id == current_user.id).all()


@router_likes.post("/create_likes")
def create(form: Create_like = Depends(Create_like), db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_user)):
    create_like(form.source, form.source_id, db, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_likes.delete("/delete_likes")
def delete(delete_all: bool = False, ident: int = 0, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_user)):
    delete_like(delete_all, ident, current_user, db)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi")
