from sqlalchemy.orm import Session
from db_connect import database
from functions.file import create_file, update_file, delete_file
from routes.login import get_current_user
from schemas.files import Create_file
from fastapi import APIRouter, Depends, HTTPException

from schemas.users import CreateUser

router_files = APIRouter(
    prefix="/files",
    tags=["Files operations"]
)


@router_files.post("/create_file")
def create(form: Create_file = Depends(Create_file), db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_user)):
    create_file(form.new_files, form.source, form.source_id, db, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")


@router_files.put("/update_file")
def update(form: Create_file = Depends(Create_file), db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_user)):
    update_file(form.new_files, form.source, form.source_id, db, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")


@router_files.delete("/delete_file")
def delete(ident: int, db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    delete_file(ident, db, current_user)
    raise HTTPException(200, "Amaliyot muvaffaqiyatli amalga oshirildi !!!")