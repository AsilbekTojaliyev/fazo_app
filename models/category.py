from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db_connect import Base


class Categories(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    link = Column(String(255), nullable=False)
