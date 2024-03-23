from functions.universal_functions import get_in_db, new_item_db
from models.laptop import Laptops
from models.like import Likes
from models.tablet import Tablets
from models.phone import Phones
from fastapi import HTTPException


def create_like(source, source_id, db, user):
    if (source == "laptop" and db.query(Laptops).filter(Laptops.id == source_id).first() is None) or \
            (source == "tablet" and db.query(Tablets).filter(
                Tablets.id == source_id).first() is None) or \
            (source == "phone" and db.query(Phones).filter(
                Phones.id == source_id).first() is None):
        raise HTTPException(400, "biriktirilgan ma'lumot topilmadi")

    x = db.query(Likes).filter(
        Likes.user_id == user.id,
        Likes.source == source,
        Likes.source_id == source_id).first()

    if x is not None:
        raise HTTPException(400, "bu ma'lumot saralanganlarda mavjud")

    new_db = Likes(
        user_id=user.id,
        source=source,
        source_id=source_id
    )
    new_item_db(db, new_db)


def delete_like(delete_all, ident, user, db):
    if delete_all:
        likes = db.query(Likes).filter(Likes.user_id == user.id).all()
        for like in likes:
            db.query(Likes).filter(Likes.id == like.id).delete()
            db.commit()

    like_user = db.query(Likes).filter(Likes.user_id == user.id).first()
    if like_user.id == ident:
        get_in_db(db, Likes, ident)
        db.query(Likes).filter(Likes.id == ident).delete()
        db.commit()
    else:
        raise HTTPException(400, "siz buni o'chirolmaysiz")
