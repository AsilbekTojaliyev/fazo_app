from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from functions.universal_functions import get_in_db, new_item_db, pagination
from models.category import Categories
from models.planshet import Planshets


def get_planshet(price, country, rom_size, ram_size, brand, page, limit, db):
    if country:
        country_formatted = "%{}%".format(country)
        country_filter = (Planshets.country.like(country_formatted))
    else:
        country_filter = Planshets.id > 0

    if price > 0:
        price_filter = Planshets.price <= price
    else:
        price_filter = Planshets.id > 0

    if brand:
        brand_formatted = "%{}%".format(brand)
        brand_filter = (Planshets.brand.like(brand_formatted))
    else:
        brand_filter = Planshets.id > 0

    if rom_size > 0:
        rom_size_filter = Planshets.rom_size == rom_size
    else:
        rom_size_filter = Planshets.id > 0

    if ram_size > 0:
        ram_size_filter = Planshets.ram_size == ram_size
    else:
        ram_size_filter = Planshets.id > 0

    items = db.query(Planshets).options(joinedload(Planshets.files)).filter(
        brand_filter, country_filter, price_filter,
        ram_size_filter, rom_size_filter).order_by(func.random())

    return pagination(items, page, limit)


def create_planshet(db, forms, user):
    if user.role == "admin":
        for form in forms:
            get_in_db(db, Categories, form.category_id)
            discount_price = form.price - (form.price * form.discount)/100
            new_add = Planshets(
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


def update_planshet(db, forms, user):
    if user.role == "admin":
        for form in forms:
            get_in_db(db, Planshets, form.ident)
            get_in_db(db, Categories, form.category_id)
            discount_price = form.price - (form.price * form.discount)/100
            db.query(Planshets).filter(Planshets.id == form.ident).update({
                Planshets.category_id: form.category_id,
                Planshets.name: form.name,
                Planshets.brand: form.brand,
                Planshets.screen_type: form.screen_type,
                Planshets.year: form.year,
                Planshets.price: form.price,
                Planshets.country: form.country,
                Planshets.weight: form.weight,
                Planshets.color: form.color,
                Planshets.ram_size: form.ram_size,
                Planshets.rom_size: form.rom_size,
                Planshets.display: form.display,
                Planshets.camera: form.camera,
                Planshets.self_camera: form.self_camera,
                Planshets.discount: form.discount,
                Planshets.discount_price: discount_price,
                Planshets.discount_time: form.discount_time,
                Planshets.count: form.count
            })
        db.commit()
    else:
        raise HTTPException(400, "You can't upgrade !!!")


def delete_planshet(db, idents, user):
    if user.role == "admin":
        for ident in idents:
            get_in_db(db, Planshets, ident)
            db.query(Planshets).filter(Planshets.id == ident).delete()
        db.commit()
    else:
        raise HTTPException(400, "You can't !!!")
