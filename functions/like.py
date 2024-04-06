from functions.universal_functions import get_in_db, new_item_db, most_viewed
from models.laptop import Laptops
from models.like import Likes
from models.tablet import Tablets
from models.phone import Phones
from fastapi import HTTPException


def create_like(source, source_id, db, user):
    most_viewed(source, source_id, db)

    if ((source == "laptop" and db.query(Laptops).filter(Laptops.id == source_id).first() is None) or
            (source == "tablet" and db.query(Tablets).filter(Tablets.id == source_id).first() is None) or
            (source == "phone" and db.query(Phones).filter(Phones.id == source_id).first() is None)):
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


def delete_like(delete_all, source, source_id, user, db):
    likes = db.query(Likes).filter(Likes.user_id == user.id).all()
    if delete_all:
        for like in likes:
            db.query(Likes).filter(Likes.id == like.id).delete()
            db.commit()
    if db.query(Likes).filter(Likes.user_id == user.id, Likes.source == source, Likes.source_id == source_id).first():
        db.query(Likes).filter(Likes.user_id == user.id, Likes.source == source, Likes.source_id == source_id).delete()
        db.commit()
    else:
        raise HTTPException(400, "malumot topilmadi, yoki siz ozingizga tegishli bolmagan malumotni kiritdingiz")


