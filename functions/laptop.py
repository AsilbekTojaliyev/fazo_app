import random
from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from functions.universal_functions import get_in_db, new_item_db, pagination_search
from models.category import Categories
from models.laptop import Laptops


def get_laptop(price, brand, country, rom_size, ram_size, page, limit, db):

    if price > 0:
        price_filter = Laptops.discount_price <= price
    else:
        price_filter = Laptops.id > 0

    if brand:
        brand_formatted = "%{}%".format(brand)
        brand_filter = Laptops.brand.like(brand_formatted)
    else:
        brand_filter = Laptops.id > 0

    if country:
        country_formatted = "%{}%".format(country)
        country_filter = (Laptops.country.like(country_formatted))
    else:
        country_filter = Laptops.id > 0

    if rom_size > 0:
        rom_size_filter = Laptops.rom_size == rom_size
    else:
        rom_size_filter = Laptops.id > 0

    if ram_size > 0:
        ram_size_filter = Laptops.ram_size == ram_size
    else:
        ram_size_filter = Laptops.id > 0

    items = db.query(Laptops).options(joinedload(Laptops.files)).filter(
        price_filter, ram_size_filter, brand_filter, country_filter, rom_size_filter).order_by(desc(Laptops.id)).all()

    random.shuffle(items)
    return pagination_search(items, page, limit)


def create_laptop(db, forms, user):
    category = db.query(Categories).filter(Categories.name == "kompyuterlar").first()
    if user.role == "admin":
        for form in forms:
            discount_price = form.price - (form.discount * form.price)/100
            new_add = Laptops(
                description=form.description,
                name="laptop",
                category_id=category.id,
                price=form.price,
                color=form.color,
                weight=form.weight,
                country=form.country,
                year=form.year,
                rom_size=form.rom_size,
                ram_size=form.ram_size,
                brand=form.brand,
                screen_type=form.screen_type,
                display=form.display,
                videocard=form.videocard,
                processor=form.processor,
                rom_type=form.rom_type,
                discount=form.discount,
                discount_price=discount_price,
                count=form.count,
                discount_time=form.discount_time,
                see_num=0,
                favorite=0
            )
            new_item_db(db, new_add)
    else:
        raise HTTPException(400, "You can't !!!")


def update_laptop(db, forms, user):
    if user.role == "admin":
        for form in forms:
            get_in_db(db, Laptops, form.ident)
            discount_price = form.price - (form.discount * form.price)/100
            db.query(Laptops).filter(Laptops.id == form.ident).update({
                Laptops.description: form.description,
                Laptops.brand: form.brand,
                Laptops.screen_type: form.screen_type,
                Laptops.year: form.year,
                Laptops.price: form.price,
                Laptops.country: form.country,
                Laptops.weight: form.weight,
                Laptops.color: form.color,
                Laptops.ram_size: form.ram_size,
                Laptops.rom_size: form.rom_size,
                Laptops.display: form.display,
                Laptops.processor: form.processor,
                Laptops.videocard: form.videocard,
                Laptops.rom_type: form.rom_type,
                Laptops.discount: form.discount,
                Laptops.discount_price: discount_price,
                Laptops.count: form.count,
                Laptops.discount_time: form.discount_time
            })
        db.commit()
    else:
        raise HTTPException(400, "You can't upgrade !!!")


def delete_laptop(db, idents, user):
    if user.role == "admin":
        for ident in idents:
            get_in_db(db, Laptops, ident)
            db.query(Laptops).filter(Laptops.id == ident).delete()
        db.commit()
    else:
        raise HTTPException(400, "You can't !!!")
