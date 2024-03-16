from db_connect import Base
from sqlalchemy import String, Column, Integer, Numeric


class Telephones(Base):
    __tablename__ = "telephones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    category_id = Column(Integer)
    price = Column(Numeric)
    brand = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    color = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    ram_size = Column(Integer, nullable=False)
    rom_size = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    display = Column(Numeric, nullable=False)
    weight = Column(Numeric, nullable=False)
    battery = Column(Integer, nullable=False)
    camera = Column(Integer, nullable=False)
    self_camera = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False)
    discount_price = Column(Numeric, nullable=False)
    count = Column(Integer, nullable=False)
    discount_time = Column(Integer, nullable=False)
