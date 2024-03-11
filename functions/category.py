from functions.universal_functions import get_in_db, new_item_db
from models.category import Categories
from fastapi import HTTPException


def create_category(db, forms, user):
    if user.role == "admin":
        for form in forms:
            new_db = Categories(
                name=form.name
            )
            new_item_db(db, new_db)
    else:
        raise HTTPException(400, "You can't !!!")


def update_category(db, forms, user):
    if user.role == "admin":
        for form in forms:
            get_in_db(db, Categories, form.ident)
            db.query(Categories).filter(Categories.id == form.ident).update({
                Categories.name: form.name
            })
        db.commit()
    else:
        raise HTTPException(400, "You can't !!!")


def delete_category(db, idents, user):
    if user.role == "admin":
        for ident in idents:
            get_in_db(db, Categories, ident)
            db.query(Categories).filter(Categories.id == ident).delete()
        db.commit()
    else:
        raise HTTPException(400, "You can't !!!")
