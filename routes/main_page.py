import random
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from db_connect import database
from functions.universal_functions import pagination_search
from models.category import Categories
from models.laptop import Laptops
from models.tablet import Tablets
from models.phone import Phones

router_main = APIRouter(prefix="/main", tags=["main operations"])


@router_main.get("/get_all_source")
def get_source(page: int = 1, limit: int = 25, word: str = None, db: Session = Depends(database)):
    word_formatted = "%{}%".format(word)
    category = db.query(Categories).filter(Categories.name.like(word_formatted)).first()
    if word:
        laptop = db.query(Laptops).options(joinedload(Laptops.files)).filter(Laptops.category_id == category.id).all()
        planshet = db.query(Tablets).options(joinedload(Tablets.files)).filter(Tablets.category_id == category.id).all()
        phone = db.query(Phones).options(joinedload(Phones.files)).filter(Phones.category_id == category.id).all()
        items = laptop + planshet + phone
        random.shuffle(items)
    else:
        items = db.query(Laptops).options(joinedload(Laptops.files)).all()
        items += db.query(Tablets).options(joinedload(Tablets.files)).all()
        items += db.query(Phones).options(joinedload(Phones.files)).all()
        random.shuffle(items)

    return pagination_search(items, page, limit)


@router_main.get("/get_cheap_product")
def get_cheap_products(page: int = 1, limit: int = 25, db: Session = Depends(database)):
    lap_price = db.query(func.avg(Laptops.discount_price)).scalar()
    tab_price = db.query(func.avg(Tablets.discount_price)).scalar()
    tel_price = db.query(func.avg(Phones.discount_price)).scalar()
    result = db.query(Laptops).options(joinedload(Laptops.files)).filter(Laptops.discount_price <= lap_price).all()
    result += db.query(Tablets).options(joinedload(Tablets.files)).filter(Tablets.discount_price <= tab_price).all()
    result += db.query(Phones).options(joinedload(Phones.files)).filter(Phones.discount_price <= tel_price).all()
    random.shuffle(result)
    return pagination_search(result, page, limit)
