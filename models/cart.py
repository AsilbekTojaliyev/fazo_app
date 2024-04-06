from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship
from db_connect import Base
from models.user import Users


class Carts(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    status = Column(Boolean, nullable=False)

    user = relationship(argument="Users", foreign_keys=[user_id],
                        primaryjoin=lambda: Users.id == Carts.user_id)
