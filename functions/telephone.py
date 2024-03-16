from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from functions.universal_functions import get_in_db, new_item_db, pagination
from models.category import Categories
from models.telephone import Telephones


def get_telephone(country, price, rom_size, ram_size, brand, page, limit, db):

    if country:
        country_formatted = "%{}%".format(country)
        country_filter = Telephones.country.like(country_formatted)
    else:
        country_filter = Telephones.id > 0

    if price > 0:
        price_filter = Telephones.price <= price
    else:
        price_filter = Telephones.id > 0

    if brand:
        brand_formatted = "%{}%".format(brand)
        brand_filter = (Telephones.brand.like(brand_formatted))
    else:
        brand_filter = Telephones.id > 0

    if rom_size > 0:
        rom_size_filter = Telephones.rom_size == rom_size
    else:
        rom_size_filter = Telephones.id > 0

    if ram_size > 0:
        ram_size_filter = Telephones.ram_size == ram_size
    else:
        ram_size_filter = Telephones.id > 0

    items = db.query(Telephones).options(joinedload(Telephones.files)).filter(
        brand_filter, ram_size_filter,
        rom_size_filter, country_filter,
        price_filter).order_by(func.random())

    return pagination(items, page, limit)


def create_phone(db, forms, user):
    if user.role == "admin":
        for form in forms:
            get_in_db(db, Categories, form.category_id)
            discount_price = form.price - (form.price * form.discount)/100
            new_add = Telephones(
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
                model=form.model,
                display=form.display,
                battery=form.battery,
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


def update_phone(db, forms, user):
    if user.role == "admin":
        for form in forms:
            get_in_db(db, Telephones, form.ident)
            get_in_db(db, Categories, form.category_id)
            discount_price = form.price - (form.price * form.discount)/100
            db.query(Telephones).filter(Telephones.id == form.ident).update({
                Telephones.category_id: form.category_id,
                Telephones.name: form.name,
                Telephones.brand: form.brand,
                Telephones.model: form.model,
                Telephones.year: form.year,
                Telephones.price: form.price,
                Telephones.country: form.country,
                Telephones.weight: form.weight,
                Telephones.color: form.color,
                Telephones.ram_size: form.ram_size,
                Telephones.rom_size: form.rom_size,
                Telephones.display: form.display,
                Telephones.camera: form.camera,
                Telephones.self_camera: form.self_camera,
                Telephones.battery: form.battery,
                Telephones.discount: form.discount,
                Telephones.discount_price: discount_price,
                Telephones.discount_time: form.discount_time,
                Telephones.count: form.count
            })
        db.commit()
    else:
        raise HTTPException(400, "You can't upgrade !!!")


def delete_phone(db, idents, user):
    if user.role == "admin":
        for ident in idents:
            get_in_db(db, Telephones, ident)
            db.query(Telephones).filter(Telephones.id == ident).delete()
        db.commit()
    else:
        raise HTTPException(400, "You can't !!!")
