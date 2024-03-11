from functions.universal_functions import get_in_db, new_item_db
from models.buy import Buys
from models.cart import Carts
from models.laptop import Laptops
from models.planshet import Planshets
from models.telephone import Telephones
from fastapi import HTTPException


def create_cart(source, source_id, user, db):
    buys = db.query(Buys).filter(Buys.user_id == user.id).first()
    if buys is None:
        new_buy = Buys(
            user_id=user.id,
            status=False
        )
        new_item_db(db, new_buy)

    elif source == "laptop" and db.query(Laptops).filter(Laptops.id == source_id).first() is not None:
        x = db.query(Carts).filter(
            Carts.buy_id == buys.id,
            Carts.source == source,
            Carts.source_id == source_id).first()
        if x is not None:
            db.query(Carts).filter(Carts.source_id == source_id, Carts.source == "laptop").update({
                Carts.amount: Carts.amount + 1
            })
            db.commit()
        else:
            new_db = Carts(
                buy_id=buys.id,
                source=source,
                source_id=source_id,
                amount=1,
            )
            new_item_db(db, new_db)

    elif source == "planshet" and db.query(Planshets).filter(Planshets.id == source_id).first() is not None:
        x = db.query(Carts).filter(
            Carts.buy_id == buys.id,
            Carts.source == source,
            Carts.source_id == source_id).first()
        if x is not None:
            db.query(Carts).filter(Carts.source_id == source_id, Carts.source == "planshet").update({
                Carts.amount: Carts.amount + 1
            })
            db.commit()
        else:
            new_db = Carts(
                buy_id=buys.id,
                source=source,
                source_id=source_id,
                amount=1,
            )
            new_item_db(db, new_db)

    elif source == "telephone" and db.query(Telephones).filter(Telephones.id == source_id).first() is not None:
        x = db.query(Carts).filter(
            Carts.buy_id == buys.id,
            Carts.source == source,
            Carts.source_id == source_id).first()
        if x is not None:
            db.query(Carts).filter(Carts.source_id == source_id, Carts.source == "telephone").update({
                Carts.amount: Carts.amount + 1
            })
            db.commit()
        else:
            new_db = Carts(
                buy_id=buys.id,
                source=source,
                source_id=source_id,
                amount=1,
            )
            new_item_db(db, new_db)
    else:
        raise HTTPException(400, "biriktirilgan malumot topilmadi")


def delete_cart(ident, user, db):
    get_in_db(db, Carts, ident)
    buy = db.query(Buys).filter(Buys.user_id == user.id).first()
    carts = db.query(Carts).filter(Carts.buy_id == buy.id).all()
    for cart in carts:
        if cart.id == ident:
            db.query(Carts).filter(Carts.id == ident).delete()
            db.commit()
