from routes.login import get_password_hash
from functions.universal_functions import new_item_db
from models.user import Users
from fastapi import HTTPException


def get_users(db, user):
    if user.role == "admin":
        items = db.query(Users).all()
        return items
    else:
        raise HTTPException(400, "You can't!!!")


def create_user_f(form, db):
    new_add = Users(
        name=form.name,
        username=form.username,
        role="user",
        phone_number=form.phone_number,
        password=get_password_hash(form.password))
    new_item_db(db, new_add)


def update_user_f(form, db, user):
    if user.role == "user":
        db.query(Users).filter(Users.id == user.id).update({
            Users.name: form.name,
            Users.username: form.username,
            Users.phone_number: form.phone_number,
            Users.password: get_password_hash(form.password),
            Users.role: "user"
        })

        db.commit()

    elif user.role == "admin":
        db.query(Users).filter(Users.id == user.id).update({
            Users.name: form.name,
            Users.username: form.username,
            Users.password: get_password_hash(form.password),
            Users.role: "admin"
        })
        db.commit()


def delete_user_f(db, user):
    db.query(Users).filter(Users.id == user.id).delete()
    db.commit()


def get_admin(ident, db):

    if ident > 0:
        ident_filter = Users.id == ident
    else:
        ident_filter = Users.id > 0

    items = db.query(Users).filter(ident_filter).order_by(Users.id.desc()).all()
    return items


def create_admin_f(form, db, user):
    if user.role == "admin":
        new_add = Users(
            name=form.name,
            username=form.username,
            phone_number=form.phone_number,
            role="admin",
            password=get_password_hash(form.password)
        )
        new_item_db(db, new_add)
    else:
        raise HTTPException(400, "You can't !!!")
