import math
from fastapi import HTTPException
from models.trade import Trades
from models.laptop import Laptops
from models.tablet import Tablets
from models.phone import Phones


def most_viewed(source, source_id, db):
    if source == "laptop" and db.query(Laptops).filter(Laptops.id == source_id).first() is not None:
        db.query(Laptops).filter(Laptops.id == source_id).update({
            Laptops.see_num: Laptops.see_num + 1})
        db.commit()
    elif source == "tablet" and db.query(Tablets).filter(Tablets.id == source_id).first() is not None:
        db.query(Tablets).filter(Tablets.id == source_id).update({
            Tablets.see_num: Tablets.see_num + 1})
        db.commit()
    elif source == "phone" and db.query(Phones).filter(Phones.id == source_id).first() is not None:
        db.query(Phones).filter(Phones.id == source_id).update({
            Phones.see_num: Phones.see_num + 1})
        db.commit()


def product_reduction(trade, db):
    if trade.source == "laptop" and db.query(Laptops).filter(Laptops.id == trade.source_id).first() is not None:
        db.query(Laptops).filter(Laptops.id == trade.source_id).update({
            Laptops.count: Laptops.count - trade.amount})
        db.commit()
    elif trade.source == "tablet" and db.query(Tablets).filter(Tablets.id == trade.source_id).first() is not None:
        db.query(Tablets).filter(Tablets.id == trade.source_id).update({
            Tablets.count: Tablets.count - trade.amount})
        db.commit()
    elif trade.source == "phone" and db.query(Phones).filter(Phones.id == trade.source_id).first() is not None:
        db.query(Phones).filter(Phones.id == trade.source_id).update({
            Phones.count: Phones.count - trade.amount})
        db.commit()


def new_item_db(db, a):
    db.add(a)
    db.commit()
    db.refresh(a)


def get_in_db(db, model, ident=int):
    text = db.query(model).filter(model.id == ident).first()
    if text is None:
        raise HTTPException(400, f"{model} dan ma'lumot topilmadi!")
    return text


def pagination_search(form, page, limit):
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    elif page and limit:
        return {"current_page": page, "limit": limit, "pages": math.ceil(len(form) / limit),
                "data": form[(page - 1) * limit:page * limit]}
    else:
        return {"data": form}


def trade_create(source, source_id, cart, db):
    x = db.query(Trades).filter(
        Trades.cart_id == cart.id,
        Trades.source == source,
        Trades.source_id == source_id).first()

    if source == "laptop" and db.query(Laptops).filter(Laptops.id == source_id).first() is not None:
        laptop = db.query(Laptops).filter(Laptops.id == source_id).first()
        if x is not None:
            db.query(Trades).filter(Trades.source_id == source_id, Trades.source == "laptop").update({
                Trades.amount: Trades.amount + 1,
                Trades.price_source: Trades.price_source + laptop.discount_price
            })
            db.commit()
            raise HTTPException(200, "siz bu mahsulotni qayta qo'shdingiz")
        else:
            new_db = Trades(
                cart_id=cart.id,
                source=source,
                source_id=source_id,
                amount=1,
                price_one=laptop.discount_price,
                price_source=laptop.discount_price
            )
            new_item_db(db, new_db)

    elif source == "tablet" and db.query(Tablets).filter(Tablets.id == source_id).first() is not None:
        tablet = db.query(Tablets).filter(Tablets.id == source_id).first()
        if x is not None:
            db.query(Trades).filter(Trades.source_id == source_id, Trades.source == "tablet").update({
                Trades.amount: Trades.amount + 1,
                Trades.price_source: Trades.price_source + tablet.discount_price
            })
            db.commit()
            raise HTTPException(200, "siz bu mahsulotni qayta qo'shdingiz")
        else:
            new_db = Trades(
                cart_id=cart.id,
                source=source,
                source_id=source_id,
                amount=1,
                price_one=tablet.discount_price,
                price_source=tablet.discount_price
            )
            new_item_db(db, new_db)

    elif source == "phone" and db.query(Phones).filter(Phones.id == source_id).first() is not None:
        phone = db.query(Phones).filter(Phones.id == source_id).first()
        if x is not None:
            db.query(Trades).filter(Trades.source_id == source_id, Trades.source == "phone").update({
                Trades.amount: Trades.amount + 1,
                Trades.price_source: Trades.price_source + phone.discount_price
            })
            db.commit()
            raise HTTPException(200, "siz bu mahsulotni qayta qo'shdingiz")
        else:
            new_db = Trades(
                cart_id=cart.id,
                source=source,
                source_id=source_id,
                amount=1,
                price_one=phone.discount_price,
                price_source=phone.discount_price
            )
            new_item_db(db, new_db)
    else:
        raise HTTPException(400, "biriktirilgan malumot topilmadi")


# def pagination(form, page, limit):
#     if page < 0 or limit < 0:
#         raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
#     elif page and limit:
#         return {"current_page": page, "limit": limit, "pages": math.ceil(form.count() / limit),
#                 "data": form.offset((page - 1) * limit).limit(limit).all()}
#     else:
#         return {"data": form.all()}
