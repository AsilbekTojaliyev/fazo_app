from sqlalchemy import Column, Integer, Numeric, String, and_
from sqlalchemy.orm import relationship, backref
from db_connect import Base
from models.laptop import Laptops
from models.tablet import Tablets
from models.phone import Phones


class Carts(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    buy_id = Column(Integer, nullable=False)
    source = Column(String(255), nullable=False)
    source_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    price_one = Column(Numeric, nullable=False)
    price_source = Column(Numeric, nullable=False)

    laptop = relationship(argument="Laptops", foreign_keys=[source_id],
                          primaryjoin=lambda: and_(Laptops.id == Carts.source_id, Carts.source == "laptop"),
                          backref=backref("carts"))
    planshet = relationship(argument="Tablets", foreign_keys=[source_id],
                            primaryjoin=lambda: and_(Tablets.id == Carts.source_id, Carts.source == "tablet"),
                            backref=backref("carts"))
    telephone = relationship(argument="Phones", foreign_keys=[source_id],
                            primaryjoin=lambda: and_(Phones.id == Carts.source_id, Carts.source == "phone"),
                            backref=backref("carts"))
