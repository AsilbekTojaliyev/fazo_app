import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from db_connect import database
from functions.universal_functions import pagination_search, get_in_db, most_viewed
from models.cart import Carts
from models.laptop import Laptops
from models.like import Likes
from models.tablet import Tablets
from models.phone import Phones
from models.trade import Trades
from routes.login import get_current_user
from schemas.get_one_source import Get_one_product
from schemas.users import CreateUser

router_main = APIRouter(prefix="/main", tags=["main operations"])


@router_main.get("/get_likes_count")
def get(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    count_like = len(db.query(Likes).filter(Likes.user_id == current_user.id).all())
    return count_like


@router_main.get("/get_count_trades")
def count_trades(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    carts = db.query(Carts).filter(Carts.user_id == current_user.id).all()
    for cart in carts:
        return len(db.query(Trades).filter(Trades.cart_id == cart.id).all())


@router_main.get("/get_one_source")
def get_one_source(form: Get_one_product = Depends(Get_one_product), db: Session = Depends(database)):
    most_viewed(form.name, form.ident, db)
    if form.name == "laptop":
        get_in_db(db, Laptops, form.ident)
        return db.query(Laptops).filter(Laptops.id == form.ident).all()
    if form.name == "tablet":
        get_in_db(db, Tablets, form.ident)
        return db.query(Tablets).filter(Tablets.id == form.ident).all()
    if form.name == "phone":
        get_in_db(db, Phones, form.ident)
        return db.query(Phones).filter(Phones.id == form.ident).all()


@router_main.get("/get_all_source")
def get__all_source(word: str = None, page: int = 1, limit: int = 25, db: Session = Depends(database)):
    word_formatted = "%{}%".format(word)
    if word:
        items = db.query(Laptops).options(joinedload(Laptops.files)).filter(
            Laptops.description.like(word_formatted)).all()
        items += db.query(Tablets).options(joinedload(Tablets.files)).filter(
            Tablets.description.like(word_formatted)).all()
        items += db.query(Phones).options(joinedload(Phones.files)).filter(
            Phones.description.like(word_formatted)).all()
        random.shuffle(items)
    else:
        items = db.query(Laptops).options(joinedload(Laptops.files)).all()
        items += db.query(Tablets).options(joinedload(Tablets.files)).all()
        items += db.query(Phones).options(joinedload(Phones.files)).all()
        random.shuffle(items)

    return pagination_search(items, page, limit)


@router_main.get("/get_cheap_product")
def get_cheap_products(page: int = 1, limit: int = 25, db: Session = Depends(database)):
    result = []
    if db.query(Laptops).all() is None and db.query(Tablets).all() is None and db.query(Phones).all() is None:
        raise HTTPException(400, "bazaga malumotlar qo'shilmagan")

    if db.query(Laptops).all():
        laptop_price = db.query(func.avg(Laptops.discount_price)).scalar()
        result += db.query(Laptops).options(joinedload(Laptops.files)).filter(
            Laptops.discount_price <= laptop_price).all()

    if db.query(Tablets).all():
        tablet_price = db.query(func.avg(Tablets.discount_price)).scalar()
        result += db.query(Tablets).options(joinedload(Tablets.files)).filter(
            Tablets.discount_price <= tablet_price).all()

    if db.query(Phones).all():
        phone_price = db.query(func.avg(Phones.discount_price)).scalar()
        result += db.query(Phones).options(joinedload(Phones.files)).filter(
            Phones.discount_price <= phone_price).all()

    random.shuffle(result)
    return pagination_search(result, page, limit)


@router_main.get("/get_most_viewed")
def get_viewed(page: int = 1, limit: int = 25, db: Session = Depends(database)):
    result = []
    if db.query(Laptops).all() is None and db.query(Tablets).all() is None and db.query(Phones).all() is None:
        raise HTTPException(400, "bazaga malumotlar qo'shilmagan")

    if db.query(Laptops).all():
        see_laptops = db.query(func.avg(Laptops.see_num)).scalar()
        result += db.query(Laptops).options(joinedload(Laptops.files)).filter(
            Laptops.see_num <= see_laptops).all()

    if db.query(Tablets).all():
        see_tablets = db.query(func.avg(Tablets.see_num)).scalar()
        result += db.query(Tablets).options(joinedload(Tablets.files)).filter(
            Tablets.see_num <= see_tablets).all()

    if db.query(Phones).all():
        see_phones = db.query(func.avg(Phones.see_num)).scalar()
        result += db.query(Phones).options(joinedload(Phones.files)).filter(
            Phones.see_num <= see_phones).all()

    random.shuffle(result)
    return pagination_search(result, page, limit)


@router_main.get("/get_most_product_likes")
def get_favorite(page: int = 1, limit: int = 25, db: Session = Depends(database)):
    result = []
    if db.query(Laptops).all() is None and db.query(Tablets).all() is None and db.query(Phones).all() is None:
        raise HTTPException(400, "bazaga malumotlar qo'shilmagan")

    if db.query(Laptops).all():
        like_laptops = db.query(func.avg(Laptops.favorite)).scalar()
        result += db.query(Laptops).options(joinedload(Laptops.files)).filter(
            Laptops.favorite <= like_laptops).all()

    if db.query(Tablets).all():
        like_tablets = db.query(func.avg(Tablets.favorite)).scalar()
        result += db.query(Tablets).options(joinedload(Tablets.files)).filter(
            Tablets.favorite <= like_tablets).all()

    if db.query(Phones).all():
        like_phones = db.query(func.avg(Phones.favorite)).scalar()
        result += db.query(Phones).options(joinedload(Phones.files)).filter(
            Phones.favorite <= like_phones).all()

    random.shuffle(result)
    return pagination_search(result, page, limit)


@router_main.get("/get_discount")
def get_discount(page: int = 1, limit: int = 25, db: Session = Depends(database)):
    result = []
    if db.query(Laptops).all() is None and db.query(Tablets).all() is None and db.query(Phones).all() is None:
        raise HTTPException(400, "bazaga malumotlar qo'shilmagan")

    if db.query(Laptops).all():
        dc_laptops = db.query(func.avg(Laptops.discount)).scalar()
        result += db.query(Laptops).options(joinedload(Laptops.files)).filter(
            Laptops.discount <= dc_laptops).all()

    if db.query(Tablets).all():
        dc_tablets = db.query(func.avg(Tablets.discount)).scalar()
        result += db.query(Tablets).options(joinedload(Tablets.files)).filter(
            Tablets.discount <= dc_tablets).all()

    if db.query(Phones).all():
        dc_phones = db.query(func.avg(Phones.discount)).scalar()
        result += db.query(Phones).options(joinedload(Phones.files)).filter(
            Phones.discount <= dc_phones).all()

    random.shuffle(result)
    return pagination_search(result, page, limit)
