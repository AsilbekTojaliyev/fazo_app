import os
from functions.universal_functions import get_in_db
from models.file import Files
from models.laptop import Laptops
from models.tablet import Tablets
from models.phone import Phones
from fastapi import HTTPException


def create_file(new_files, source, source_id, db, user):
    if user.role == "admin":
        if (source == "laptop" and db.query(Laptops).filter(Laptops.id == source_id).first() is None) or \
                (source == "tablet" and db.query(Tablets).filter(Tablets.id == source_id).first() is None) or \
                (source == "phone" and db.query(Phones).filter(Phones.id == source_id).first() is None):
            raise HTTPException(400, "Fayl biriktiriladigan ma'lumot topilmadi !!!")
        uploaded_file_objects = []
        for new_file in new_files:
            ext = os.path.splitext(new_file.filename)[-1].lower()
            if ext not in [".jpg", ".png", ".mp3", ".mp4", ".gif", ".jpeg"]:
                raise HTTPException(400, "Fayl formati mos kelmadi !!!")
            file_location = f"files/{new_file.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(new_file.file.read())

            new_db = Files(
                new_files=new_file.filename,
                source=source,
                source_id=source_id
            )
            uploaded_file_objects.append(new_db)
        db.add_all(uploaded_file_objects)
        db.commit()
    else:
        raise HTTPException(400, "Siz ma'lumot qo'sholmaysiz !!!")


def delete_file(ident, db, user):
    if user.role == "admin":
        get_in_db(db, Files, ident)
        db.query(Files).filter(Files.id == ident).delete()
        db.commit()
    else:
        raise HTTPException(400, "Siz o'chirolmaysiz !!!")


def update_file(new_files, source, source_id, db, user):
    if user.role == "admin":
        items = db.query(Files).filter(Files.source == source,
                                       Files.source_id == source_id).all()
        for item in items:
            delete_file(item.id, db)
        create_file(new_files, source, source_id, db)
    else:
        raise HTTPException(400, "Siz yangilayolmaysiz !!!")
