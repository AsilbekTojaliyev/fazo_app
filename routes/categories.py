from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_connect import database
from functions.category import create_category, update_category, delete_category
from models.category import Categories
from routes.login import get_current_user
from schemas.categories import Create_category, Update_category
from schemas.users import CreateUser

router_category = APIRouter(
    prefix="/categories",
    tags=["Categories operations"]
)


@router_category.post("/create_categories")
def create(forms: List[Create_category], db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_user)):
    create_category(db, forms, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")


@router_category.get("/get_categories")
def get(db: Session = Depends(database)):
    db.query(Categories).filter(Categories.name == "kompyuterlar").update({
        Categories.link: "/Laptops/get_filter_laptops"
    })
    db.query(Categories).filter(Categories.name == "planshetlar").update({
        Categories.link: "/Tablets/get_filter_planshets"
    })
    db.query(Categories).filter(Categories.name == "telefonlar").update({
        Categories.link: "/Phones/get_filter_telephones"
    })
    db.commit()
    return db.query(Categories).all()


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
