import math
from fastapi import HTTPException


def new_item_db(db, a):
    db.add(a)
    db.commit()
    db.refresh(a)


def get_in_db(db, model, ident=int):
    text = db.query(model).filter(model.id == ident).first()
    if text is None:
        raise HTTPException(400, f"No information found from {model}!")
    return text


def pagination(form, page, limit):
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    elif page and limit:
        return {"current_page": page, "limit": limit, "pages": math.ceil(form.count() / limit),
                "data": form.offset((page - 1) * limit).limit(limit).all()}
    else:
        return {"data": form.all()}
