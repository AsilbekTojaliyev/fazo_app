from sqlalchemy import Column, Integer, Date, Numeric
from sqlalchemy.orm import relationship
from db_connect import Base
from models.user import Users


class Incomes(Base):
    __tablename__ = "incomes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)
    date_receipt = Column(Date, nullable=False)

    user = relationship(argument="Users", foreign_keys=[user_id],
                        primaryjoin=lambda: Users.id == Incomes.user_id)
