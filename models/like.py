from sqlalchemy import Column, String, Integer, and_
from sqlalchemy.orm import relationship, backref
from db_connect import Base
from models.laptop import Laptops
from models.planshet import Planshets
from models.telephone import Telephones
from models.user import Users


class Likes(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    source = Column(String(255), nullable=False)
    source_id = Column(Integer, nullable=False)
    user = relationship(argument="Users", foreign_keys=[user_id],
                        primaryjoin=lambda: Users.id == Likes.user_id)
    laptop = relationship(argument="Laptops", foreign_keys=[source_id],
                          primaryjoin=lambda: and_(Laptops.id == Likes.source_id, Likes.source == "laptop"),
                          backref=backref("likes"))
    planshet = relationship(argument="Planshets", foreign_keys=[source_id],
                            primaryjoin=lambda: and_(Planshets.id == Likes.source_id, Likes.source == "planshet"),
                            backref=backref("likes"))
    telephone = relationship(argument="Telephones", foreign_keys=[source_id],
                            primaryjoin=lambda: and_(Telephones.id == Likes.source_id, Likes.source == "telephones"),
                            backref=backref("likes"))

