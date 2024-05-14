import random

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload
from db_connect import database
from functions.like import create_like, delete_like
from models.laptop import Laptops
from models.like import Likes
from models.phone import Phones
from models.tablet import Tablets
from routes.login import get_current_user
from schemas.likes import Create_like
from schemas.users import CreateUser

router_likes = APIRouter(
    prefix="/likes",
    tags=["Likes operations"]
)


@router_likes.get("/get_likes")
def get_likes(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    return db.query(Likes).filter(Likes.user_id == current_user.id).order_by(desc(Likes.id)).all()


@router_likes.get("/get_likes_product")
def get(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    user_likes = db.query(Likes).filter(Likes.user_id == current_user.id).all()
    products = []
    for like in user_likes:
        products += db.query(Laptops).options(joinedload(Laptops.files)).filter(
            Laptops.name == like.source, Laptops.id == like.source_id).all()

        products += db.query(Tablets).options(joinedload(Tablets.files)).filter(
            Tablets.name == like.source, Tablets.id == like.source_id).all()

        products += db.query(Phones).options(joinedload(Phones.files)).filter(
            Phones.name == like.source, Phones.id == like.source_id).all()
    random.shuffle(products)
    return products


@router_likes.post("/create_likes")
def create(form: Create_like = Depends(Create_like), db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_user)):
    create_like(form.source, form.source_id, db, current_user)
    raise HTTPException(200, "amaliyot muvaffaqqiyatli")


@router_likes.delete("/delete_likes")
def delete(form: Create_like = Depends(Create_like), delete_all: bool = False, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_user)):
    delete_like(delete_all, form.source, form.source_id, current_user, db)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi")
