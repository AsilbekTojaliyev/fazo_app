from fastapi import HTTPException
from functions.universal_functions import new_item_db, trade_create, most_viewed
from models.cart import Carts
from models.trade import Trades


def create_trade(source, source_id, user, db):
    cart = db.query(Carts).filter(Carts.user_id == user.id).first()
    if cart is None:
        new_cart = Carts(
            user_id=user.id,
            status=False
        )
        new_item_db(db, new_cart)

    cart = db.query(Carts).filter(Carts.user_id == user.id).first()
    item = trade_create(source, source_id, cart, db)
    most_viewed(source, source_id, db)
    return item


def delete_trade(delete_all, source, source_id, user, db):
    cart = db.query(Carts).filter(Carts.user_id == user.id).first()
    likes = db.query(Trades).filter(Trades.cart_id == cart.id).all()
    if delete_all:
        for like in likes:
            db.query(Trades).filter(Trades.id == like.id).delete()
            db.commit()
    if db.query(Trades).filter(Trades.cart_id == cart.id, Trades.source == source, Trades.source_id == source_id).first():
        db.query(Trades).filter(Trades.cart_id == cart.id, Trades.source == source, Trades.source_id == source_id).delete()
        db.commit()
    else:
        raise HTTPException(400, "malumot topilmadi, yoki siz ozingizga tegishli bolmagan malumotni kiritdingiz")
