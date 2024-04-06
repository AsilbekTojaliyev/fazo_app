import random
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.universal_functions import get_in_db, new_item_db, pagination_search
from models.category import Categories
from models.phone import Phones


def get_phone(country, price, rom_size, ram_size, page, limit, db):

    if country:
        country_formatted = "%{}%".format(country)
        country_filter = Phones.country.like(country_formatted)
    else:
        country_filter = Phones.id > 0

    if price > 0:
        price_filter = Phones.price <= price
    else:
        price_filter = Phones.id > 0

    if rom_size > 0:
        rom_size_filter = Phones.rom_size == rom_size
    else:
        rom_size_filter = Phones.id > 0

    if ram_size > 0:
        ram_size_filter = Phones.ram_size == ram_size
    else:
        ram_size_filter = Phones.id > 0

    items = db.query(Phones).options(
        joinedload(Phones.files), joinedload(Phones.category)).filter(
        ram_size_filter, rom_size_filter, country_filter,
        price_filter).all()
    random.shuffle(items)
    return pagination_search(items, page, limit)


def create_phone(db, forms, user):
    if user.role == "admin":
        for form in forms:
            get_in_db(db, Categories, form.category_id)
            discount_price = form.price - (form.price * form.discount)/100
            new_add = Phones(
                name=form.name,
                description="phone",
                category_id=form.category_id,
                price=form.price,
                color=form.color,
                weight=form.weight,
                country=form.country,
                year=form.year,
                rom_size=form.rom_size,
                ram_size=form.ram_size,
                brand_id=form.brand_id,
                model=form.model,
                display=form.display,
                battery=form.battery,
                camera=form.camera,
                self_camera=form.self_camera,
                discount=form.discount,
                discount_price=discount_price,
                discount_time=form.discount_time,
                count=form.count,
                see_num=0
            )
            new_item_db(db, new_add)
    else:
        raise HTTPException(400, "You can't !!!")


def update_phone(db, forms, user):
    if user.role == "admin":
        for form in forms:
            get_in_db(db, Phones, form.ident)
            get_in_db(db, Categories, form.category_id)
            discount_price = form.price - (form.price * form.discount)/100
            db.query(Phones).filter(Phones.id == form.ident).update({
                Phones.category_id: form.category_id,
                Phones.name: form.name,
                Phones.description: form.description,
                Phones.brand_id: form.brand_id,
                Phones.model: form.model,
                Phones.year: form.year,
                Phones.price: form.price,
                Phones.country: form.country,
                Phones.weight: form.weight,
                Phones.color: form.color,
                Phones.ram_size: form.ram_size,
                Phones.rom_size: form.rom_size,
                Phones.display: form.display,
                Phones.camera: form.camera,
                Phones.self_camera: form.self_camera,
                Phones.battery: form.battery,
                Phones.discount: form.discount,
                Phones.discount_price: discount_price,
                Phones.discount_time: form.discount_time,
                Phones.count: form.count
            })
        db.commit()
    else:
        raise HTTPException(400, "You can't upgrade !!!")


def delete_phone(db, idents, user):
    if user.role == "admin":
        for ident in idents:
            get_in_db(db, Phones, ident)
            db.query(Phones).filter(Phones.id == ident).delete()
        db.commit()
    else:
        raise HTTPException(400, "You can't !!!")
