from functions.universal_functions import get_in_db, new_item_db, cart_buy_create
from models.buy import Buys
from models.cart import Carts


def create_cart(source, source_id, user, db):
    buy = db.query(Buys).filter(
        Buys.user_id == user.id).first()
    if buy is None:
        new_buy = Buys(
            user_id=user.id,
            status=False
        )
        new_item_db(db, new_buy)

    buy = db.query(Buys).filter(Buys.user_id == user.id).first()
    item = cart_buy_create(source, source_id, buy, db)
    return item


def delete_cart(ident, user, db):
    get_in_db(db, Carts, ident)
    buy = db.query(Buys).filter(Buys.user_id == user.id).first()
    carts = db.query(Carts).filter(Carts.buy_id == buy.id).all()
    for cart in carts:
        if cart.id == ident:
            db.query(Carts).filter(Carts.id == ident).delete()
            db.commit()
