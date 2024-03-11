from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db_connect import Base
from models.user import Users


class Comments(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    source = Column(String(255), nullable=False)
    source_id = Column(Integer, nullable=False)
    text = Column(String(255), nullable=False)

    user = relationship(argument="Users", foreign_keys=[user_id],
                        primaryjoin=lambda: Users.id == Comments.user_id)
