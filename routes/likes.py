from fastapi import APIRouter, Depends, HTTPException
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


@router_likes.get("/get_for_admin")
def get(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    if current_user.role == "admin":
        return db.query(Likes).all()
    else:
        raise HTTPException(400, "sizga mumkin emas")


@router_likes.get("/get_likes")
def get(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    result = db.query(Laptops).options(joinedload(Laptops.files)).filter(
        current_user.id == Likes.user_id, Laptops.id == Likes.source_id, Likes.source == "laptop").all()
    result += db.query(Tablets).options(joinedload(Tablets.files)).filter(
        current_user.id == Likes.user_id, Tablets.id == Likes.source_id, Likes.source == "tablet").all()
    result += db.query(Phones).options(joinedload(Phones.files)).filter(
        current_user.id == Likes.user_id, Phones.id == Likes.source_id, Likes.source == "phone").all()
    return result


@router_likes.post("/create_likes")
def create(form: Create_like = Depends(Create_like), db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_user)):
    create_like(form.source, form.source_id, db, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_likes.delete("/delete_likes")
def delete(form: Create_like = Depends(Create_like), delete_all: bool = False, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_user)):
    delete_like(delete_all, form.source, form.source_id, current_user, db)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi")
