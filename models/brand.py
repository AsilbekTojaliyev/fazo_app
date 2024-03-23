from sqlalchemy import Column, Integer, String, Text
from db_connect import Base


class Brands(Base):
    __tablename__ = "brands"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(20), nullable=False)
    img_file = Column(Text, nullable=False)