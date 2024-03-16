import random
from math import ceil
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from db_connect import database
from functions.category import create_category, update_category, delete_category
from models.category import Categories
from models.laptop import Laptops
from models.planshet import Planshets
from models.telephone import Telephones
from routes.login import get_current_user
from schemas.category import Create_category, Update_category
from schemas.user import CreateUser

router_category = APIRouter(
    prefix="/categories",
    tags=["Categories operations"]
)


def pagination(form, page, limit):
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    elif page and limit:
        return {"current_page": page, "limit": limit, "pages": ceil(len(form) / limit),
                "data": form[(page - 1) * limit:page * limit]}
    else:
        return {"data": form}


@router_category.post("/create_categories")
def create(forms: List[Create_category], db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_user)):
    create_category(db, forms, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")


@router_category.get("/get_categories")
def get(db: Session = Depends(database)):
    categories = db.query(Categories).all()
    for category in categories:
        if category.name == "kompyuterlar":
            category.link = "/Laptops/get_filter_laptops"
        if category.name == "planshetlar":
            category.link = "/Planshets/get_filter_planshets"
        if category.name == "telefonlar":
            category.link = "/Phones/get_filter_phones"
    return categories


@router_category.get("/get_all_source")
def get_all_source(page: int = 1, limit: int = 25, db: Session = Depends(database)):
    laptops = db.query(Laptops).options(joinedload(Laptops.files)).order_by(func.random()).all()
    planshets = db.query(Planshets).options(joinedload(Planshets.files)).order_by(func.random()).all()
    phones = db.query(Telephones).options(joinedload(Telephones.files)).order_by(func.random()).all()
    items = laptops + planshets + phones
    random.shuffle(items)
    return pagination(items, page, limit)


@router_category.put("/update_categories")
def update(forms: List[Update_category], db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_user)):
    update_category(db, forms, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")


@router_category.delete("/delete_categories")
def delete(idents: List[int], db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_user)):
    delete_category(db, idents, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")

# laptops = [{"type": "laptop", "data": laptop} for laptop in db.query(Laptops).options(joinedload(Laptops.files)).order_by(func.random()).all()]
#     planshets = [{"type": "planshet", "data": planshet} for planshet in db.query(Planshets).options(joinedload(Planshets.files)).order_by(func.random()).all()]
#     phones = [{"type": "phone", "data": phone} for phone in db.query(Telephones).options(joinedload(Telephones.files)).order_by(func.random()).all()]
