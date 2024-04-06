from sqlalchemy import Column, Integer, and_
from sqlalchemy.orm import relationship, backref

from db_connect import Base
from models.laptop import Laptops
from models.phone import Phones
from models.tablet import Tablets


class Trades(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, nullable=False)
    source = Column(Integer, nullable=False)
    source_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    price_one = Column(Integer, nullable=False)
    price_source = Column(Integer, nullable=False)

    laptop = relationship(argument="Laptops", foreign_keys=[source_id], viewonly=True,
                          primaryjoin=lambda: and_(Laptops.id == Trades.source_id, Trades.source == "laptop"),
                          backref=backref("trades"))
    tablet = relationship(argument="Tablets", foreign_keys=[source_id], viewonly=True,
                          primaryjoin=lambda: and_(Tablets.id == Trades.source_id, Trades.source == "tablet"),
                          backref=backref("trades"))
    phone = relationship(argument="Phones", foreign_keys=[source_id], viewonly=True,
                         primaryjoin=lambda: and_(Phones.id == Trades.source_id, Trades.source == "phone"),
                         backref=backref("trades"))


