from sqlalchemy.orm import relationship
from db_connect import Base
from sqlalchemy import String, Column, Integer, Numeric, Date
from models.category import Categories


class Tablets(Base):
    __tablename__ = "planshets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    category_id = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)
    brand_id = Column(Integer, nullable=False)
    screen_type = Column(String(255), nullable=False)
    camera = Column(Integer, nullable=False)
    self_camera = Column(Integer, nullable=False)
    color = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    ram_size = Column(Integer, nullable=False)
    rom_size = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    display = Column(Numeric, nullable=False)
    weight = Column(Numeric, nullable=False)
    discount = Column(Numeric, nullable=False)
    discount_price = Column(Numeric, nullable=False)
    count = Column(Integer, nullable=False)
    discount_time = Column(Date)
    see_num = Column(Integer, nullable=True)

    category = relationship(argument="Categories", foreign_keys=[category_id],
                            primaryjoin=lambda: Categories.id == Tablets.category_id)
