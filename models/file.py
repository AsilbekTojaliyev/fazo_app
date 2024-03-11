from sqlalchemy import Column, String, Integer, and_, Text
from sqlalchemy.orm import relationship, backref
from db_connect import Base
from models.laptop import Laptops
from models.planshet import Planshets
from models.telephone import Telephones


class Files(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    new_files = Column(Text, nullable=False)
    source = Column(String(255), nullable=False)
    source_id = Column(Integer, nullable=False)

    laptop = relationship(argument="Laptops", foreign_keys=[source_id],
                          primaryjoin=lambda: and_(Laptops.id == Files.source_id, Files.source == "laptop"),
                          backref=backref("files"))
    planshet = relationship(argument="Planshets", foreign_keys=[source_id],
                            primaryjoin=lambda: and_(Planshets.id == Files.source_id, Files.source == "planshet"),
                            backref=backref("files"))
    telephone = relationship(argument="Telephones", foreign_keys=[source_id],
                             primaryjoin=lambda: and_(Telephones.id == Files.source_id, Files.source == "telephone"),
                             backref=backref("files"))

