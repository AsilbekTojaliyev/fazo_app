from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.universal_functions import get_in_db, new_item_db, pagination
from models.category import Categories
from models.laptop import Laptops


def get_laptop(price, country, year, display, rom_type,
               rom_size, ram_size, processor, videocard, brand, page, limit, db):
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

    if price > 0:
        price_filter = Laptops.price <= price
    else:
        price_filter = Laptops.id > 0

    if year > 0:
        year_filter = Laptops.year >= year
    else:
        year_filter = Laptops.id > 0

    if display > 0:
        display_filter = Laptops.display <= display
    else:
        display_filter = Laptops.id > 0

    if rom_type:
        rom_formatted = "%{}%".format(rom_type)
        rom_type_filter = (Laptops.rom_type.like(rom_formatted))
    else:
        rom_type_filter = Laptops.id > 0

    if processor:
        processor_formatted = "%{}%".format(processor)
        processor_filter = (Laptops.processor.like(processor_formatted))
    else:
        processor_filter = Laptops.id > 0

    if videocard:
        videocard_formatted = "%{}%".format(videocard)
        videocard_filter = (Laptops.videocard.like(videocard_formatted))
    else:
        videocard_filter = Laptops.id > 0

    if rom_size > 0:
        rom_size_filter = Laptops.rom_size == rom_size
    else:
        rom_size_filter = Laptops.id > 0

    if ram_size > 0:
        ram_size_filter = Laptops.ram_size == ram_size
    else:
        ram_size_filter = Laptops.id > 0

    items = (db.query(Laptops).options(joinedload(Laptops.files)).filter(
        brand_filter, rom_type_filter, processor_filter, videocard_filter, display_filter,
        price_filter, ram_size_filter, country_filter, year_filter,
        rom_size_filter).order_by(Laptops.id.desc()))

    return pagination(items, page, limit)


def create_laptop(db, forms, user):
    if user.role == "admin":
        for form in forms:
            get_in_db(db, Categories, form.category_id)
            discount_price = form.price - (form.discount * form.price)/100
            new_add = Laptops(
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
                videocard=form.videocard,
                processor=form.processor,
                rom_type=form.rom_type,
                discount=form.discount,
                discount_price=int(discount_price),
                count=form.count,
                discount_time=form.discount_time
            )
            new_item_db(db, new_add)
    else:
        raise HTTPException(400, "You can't !!!")


def update_laptop(db, forms, user):
    if user.role == "admin":
        for form in forms:
            get_in_db(db, Laptops, form.ident)
            get_in_db(db, Categories, form.category_id)
            discount_price = form.price - (form.discount * form.price)/100
            db.query(Laptops).filter(Laptops.id == form.ident).update({
                Laptops.category_id: form.category_id,
                Laptops.name: form.name,
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
                Laptops.discount_price: int(discount_price),
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
