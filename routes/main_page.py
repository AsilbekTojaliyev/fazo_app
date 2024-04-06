import random
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from db_connect import database
from functions.universal_functions import pagination_search
from models.brand import Brands
from models.category import Categories
from models.laptop import Laptops
from models.tablet import Tablets
from models.phone import Phones

router_main = APIRouter(prefix="/main", tags=["main operations"])


@router_main.get("/get_all_source")
def get_source(word: str = None, page: int = 1, limit: int = 25, db: Session = Depends(database)):
    word_formatted = "%{}%".format(word)
    category = db.query(Categories).filter(Categories.name.like(word_formatted)).first()
    if word:
        items = db.query(Laptops).options(joinedload(Laptops.files)).filter(Laptops.category_id == category.id).all()
        items += db.query(Tablets).options(joinedload(Tablets.files)).filter(Tablets.category_id == category.id).all()
        items += db.query(Phones).options(joinedload(Phones.files)).filter(Phones.category_id == category.id).all()
        random.shuffle(items)
    else:
        items = db.query(Laptops).options(joinedload(Laptops.files)).all()
        items += db.query(Tablets).options(joinedload(Tablets.files)).all()
        items += db.query(Phones).options(joinedload(Phones.files)).all()
        random.shuffle(items)

    return pagination_search(items, page, limit)


@router_main.get("/get_brands_for_main")
def get(name: str = None, page: int = 1, limit: int = 25, db: Session = Depends(database)):
    name_formatted = "%{}%".format(name)
    brand = db.query(Brands).filter(Brands.name.like(name_formatted)).first()
    if name:
        items = db.query(Laptops).options(joinedload(Laptops.files)).filter(Laptops.brand_id == brand.id).all()
        items += db.query(Tablets).options(joinedload(Tablets.files)).filter(Tablets.brand_id == brand.id).all()
        items += db.query(Phones).options(joinedload(Phones.files)).filter(Phones.brand_id == brand.id).all()
        random.shuffle(items)
    else:
        items = db.query(Brands).options(joinedload(Brands.files)).all()

    return pagination_search(items, page, limit)


@router_main.get("/get_cheap_product")
def get_cheap_products(page: int = 1, limit: int = 25, db: Session = Depends(database)):
    laptop_price = db.query(func.avg(Laptops.discount_price)).scalar()
    tablet_price = db.query(func.avg(Tablets.discount_price)).scalar()
    phone_price = db.query(func.avg(Phones.discount_price)).scalar()
    result = db.query(Laptops).options(joinedload(Laptops.files)) \
            .filter((Laptops.discount_price is not None) and (Laptops.discount_price <= laptop_price)).all()
    result += db.query(Tablets).options(joinedload(Tablets.files)) \
            .filter((Tablets.discount_price is not None) and (Tablets.discount_price <= tablet_price)).all()
    result += db.query(Phones).options(joinedload(Phones.files)) \
            .filter((Phones.discount_price is not None) and (Phones.discount_price <= phone_price)).all()
    random.shuffle(result)
    return pagination_search(result, page, limit)


@router_main.get("/get_most_viewed")
def get_viewed(page: int = 1, limit: int = 25, db: Session = Depends(database)):
    see_laptops = db.query(func.avg(Laptops.see_num)).scalar()
    see_tablets = db.query(func.avg(Tablets.see_num)).scalar()
    see_phones = db.query(func.avg(Phones.see_num)).scalar()

    result = db.query(Laptops).options(joinedload(Laptops.files)).filter(Laptops.see_num >= see_laptops).all()
    result += db.query(Tablets).options(joinedload(Tablets.files)).filter(Tablets.see_num >= see_tablets).all()
    result += db.query(Phones).options(joinedload(Phones.files)).filter(Phones.see_num >= see_phones).all()
    random.shuffle(result)

    return pagination_search(result, page, limit)
