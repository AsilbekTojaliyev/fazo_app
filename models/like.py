from sqlalchemy import Column, String, Integer, and_
from sqlalchemy.orm import relationship, backref
from db_connect import Base
from models.laptop import Laptops
from models.tablet import Tablets
from models.phone import Phones
from models.user import Users


class Likes(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    source = Column(String(255), nullable=False)
    source_id = Column(Integer, nullable=False)

    user = relationship(argument="Users", foreign_keys=[user_id], viewonly=True,
                        primaryjoin=lambda: Users.id == Likes.user_id)

    laptop = relationship(argument="Laptops", foreign_keys=[source_id], viewonly=True,
                          primaryjoin=lambda: and_(Laptops.id == Likes.source_id, Likes.source == "laptop"),
                          backref=backref("likes"))
    tablet = relationship(argument="Tablets", foreign_keys=[source_id], viewonly=True,
                            primaryjoin=lambda: and_(Tablets.id == Likes.source_id, Likes.source == "tablet"),
                            backref=backref("likes"))
    phone = relationship(argument="Phones", foreign_keys=[source_id], viewonly=True,
                            primaryjoin=lambda: and_(Phones.id == Likes.source_id, Likes.source == "phone"),
                            backref=backref("likes"))

