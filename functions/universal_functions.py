import math
from fastapi import HTTPException
from models.cart import Carts
from models.laptop import Laptops
from models.tablet import Tablets
from models.phone import Phones


def product_reduction(cart, db):
    if cart.source == "laptop" and db.query(Laptops).filter(Laptops.id == cart.source_id).first() is not None:
        db.query(Laptops).filter(Laptops.id == cart.source_id).update({
            Laptops.count: Laptops.count - cart.amount
        })
        db.commit()
    elif cart.source == "planshet" and db.query(Tablets).filter(Tablets.id == cart.source_id).first() is not None:
        db.query(Tablets).filter(Tablets.id == cart.source_id).update({
            Tablets.count: Tablets.count - cart.amount
        })
        db.commit()
    elif cart.source == "telephone" and db.query(Phones).filter(Phones.id == cart.source_id).first() is not None:
        db.query(Phones).filter(Phones.id == cart.source_id).update({
            Phones.count: Phones.count - cart.amount
        })
        db.commit()


def new_item_db(db, a):
    db.add(a)
    db.commit()
    db.refresh(a)


def get_in_db(db, model, ident=int):
    text = db.query(model).filter(model.id == ident).first()
    if text is None:
        raise HTTPException(400, f"No information found from {model}!")
    return text


def pagination(form, page, limit):
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    elif page and limit:
        return {"current_page": page, "limit": limit, "pages": math.ceil(form.count() / limit),
                "data": form.offset((page - 1) * limit).limit(limit).all()}
    else:
        return {"data": form.all()}


def pagination_search(form, page, limit):
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    elif page and limit:
        return {"current_page": page, "limit": limit, "pages": math.ceil(len(form) / limit),
                "data": form[(page - 1) * limit:page * limit]}
    else:
        return {"data": form}


def cart_buy_create(source, source_id, buy, db):
    if source == "laptop" and db.query(Laptops).filter(Laptops.id == source_id).first() is not None:
        x = db.query(Carts).filter(
            Carts.buy_id == buy.id,
            Carts.source == source,
            Carts.source_id == source_id).first()
        laptop = db.query(Laptops).filter(Laptops.id == source_id).first()

        if x is not None:
            db.query(Carts).filter(Carts.source_id == source_id, Carts.source == "laptop").update({
                Carts.amount: Carts.amount + 1,
                Carts.price_source: Carts.price_source + laptop.discount_price
            })
            db.commit()
        else:
            new_db = Carts(
                buy_id=buy.id,
                source=source,
                source_id=source_id,
                amount=1,
                price_one=laptop.discount_price,
                price_source=laptop.discount_price
            )
            new_item_db(db, new_db)

    elif source == "planshet" and db.query(Tablets).filter(Tablets.id == source_id).first() is not None:
        x = db.query(Carts).filter(
            Carts.buy_id == buy.id,
            Carts.source == source,
            Carts.source_id == source_id).first()
        planshet = db.query(Tablets).filter(Tablets.id == source_id).first()
        if x is not None:
            db.query(Carts).filter(Carts.source_id == source_id, Carts.source == "planshet").update({
                Carts.amount: Carts.amount + 1,
                Carts.price_source: Carts.price_source + planshet.discount_price
            })
            db.commit()
        else:
            new_db = Carts(
                buy_id=buy.id,
                source=source,
                source_id=source_id,
                amount=1,
                price_one=planshet.discount_price,
                price_source=planshet.discount_price
            )
            new_item_db(db, new_db)

    elif source == "telephone" and db.query(Phones).filter(Phones.id == source_id).first() is not None:
        x = db.query(Carts).filter(
            Carts.buy_id == buy.id,
            Carts.source == source,
            Carts.source_id == source_id).first()
        phone = db.query(Phones).filter(Phones.id == source_id).first()
        if x is not None:
            db.query(Carts).filter(Carts.source_id == source_id, Carts.source == "telephone").update({
                Carts.amount: Carts.amount + 1,
                Carts.price_source: Carts.price_source + phone.discount_price
            })
            db.commit()
        else:
            new_db = Carts(
                buy_id=buy.id,
                source=source,
                source_id=source_id,
                amount=1,
                price_one=phone.discount_price,
                price_source=phone.discount_price
            )
            new_item_db(db, new_db)
    else:
        raise HTTPException(400, "biriktirilgan malumot topilmadi")
