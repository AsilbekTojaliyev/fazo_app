from sqlalchemy import Column, Integer, String, and_
from sqlalchemy.orm import relationship, backref
from db_connect import Base
from models.laptop import Laptops
from models.planshet import Planshets
from models.telephone import Telephones


class Carts(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    buy_id = Column(Integer, nullable=False)
    source = Column(String(255), nullable=False)
    source_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    
    laptop = relationship(argument="Laptops", foreign_keys=[source_id],
                          primaryjoin=lambda: and_(Laptops.id == Carts.source_id, Carts.source == "laptop"),
                          backref=backref("carts"))
    planshet = relationship(argument="Planshets", foreign_keys=[source_id],
                            primaryjoin=lambda: and_(Planshets.id == Carts.source_id, Carts.source == "planshet"),
                            backref=backref("carts"))
    telephone = relationship(argument="Telephones", foreign_keys=[source_id],
                            primaryjoin=lambda: and_(Telephones.id == Carts.source_id, Carts.source == "telephone"),
                            backref=backref("carts"))
