from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from functions.universal_functions import get_in_db, new_item_db, pagination
from models.category import Categories
from models.tablet import Tablets


def get_tablet(price, country, rom_size, ram_size, brand, page, limit, db):
    if country:
        country_formatted = "%{}%".format(country)
        country_filter = (Tablets.country.like(country_formatted))
    else:
        country_filter = Tablets.id > 0

    if price > 0:
        price_filter = Tablets.price <= price
    else:
        price_filter = Tablets.id > 0

    if brand:
        brand_formatted = "%{}%".format(brand)
        brand_filter = (Tablets.brand.like(brand_formatted))
    else:
        brand_filter = Tablets.id > 0

    if rom_size > 0:
        rom_size_filter = Tablets.rom_size == rom_size
    else:
        rom_size_filter = Tablets.id > 0

    if ram_size > 0:
        ram_size_filter = Tablets.ram_size == ram_size
    else:
        ram_size_filter = Tablets.id > 0

    items = db.query(Tablets).options(joinedload(Tablets.files)).filter(
        brand_filter, country_filter, price_filter,
        ram_size_filter, rom_size_filter).order_by(func.random())

    return pagination(items, page, limit)


def create_tablet(db, forms, user):
    if user.role == "admin":
        for form in forms:
            get_in_db(db, Categories, form.category_id)
            discount_price = form.price - (form.price * form.discount)/100
            new_add = Tablets(
                name=form.name,
                category_id=form.category_id,
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
                camera=form.camera,
                self_camera=form.self_camera,
                discount=form.discount,
                discount_price=discount_price,
                discount_time=form.discount_time,
                count=form.count
            )
            new_item_db(db, new_add)
    else:
        raise HTTPException(400, "You can't !!!")


def update_tablet(db, forms, user):
    if user.role == "admin":
        for form in forms:
            get_in_db(db, Tablets, form.ident)
            get_in_db(db, Categories, form.category_id)
            discount_price = form.price - (form.price * form.discount)/100
            db.query(Tablets).filter(Tablets.id == form.ident).update({
                Tablets.category_id: form.category_id,
                Tablets.name: form.name,
                Tablets.brand: form.brand,
                Tablets.screen_type: form.screen_type,
                Tablets.year: form.year,
                Tablets.price: form.price,
                Tablets.country: form.country,
                Tablets.weight: form.weight,
                Tablets.color: form.color,
                Tablets.ram_size: form.ram_size,
                Tablets.rom_size: form.rom_size,
                Tablets.display: form.display,
                Tablets.camera: form.camera,
                Tablets.self_camera: form.self_camera,
                Tablets.discount: form.discount,
                Tablets.discount_price: discount_price,
                Tablets.discount_time: form.discount_time,
                Tablets.count: form.count
            })
        db.commit()
    else:
        raise HTTPException(400, "You can't upgrade !!!")


def delete_tablet(db, idents, user):
    if user.role == "admin":
        for ident in idents:
            get_in_db(db, Tablets, ident)
            db.query(Tablets).filter(Tablets.id == ident).delete()
        db.commit()
    else:
        raise HTTPException(400, "You can't !!!")
