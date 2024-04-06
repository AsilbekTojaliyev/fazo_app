from functions.universal_functions import get_in_db, new_item_db, trade_create, most_viewed
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


def delete_trade(ident, user, db):
    get_in_db(db, Trades, ident)
    cart = db.query(Carts).filter(Carts.user_id == user.id).first()
    trades = db.query(Trades).filter(Trades.cart_id == cart.id).all()
    for trade in trades:
        if trade.id == ident:
            db.query(Trades).filter(Trades.id == ident).delete()
            db.commit()
