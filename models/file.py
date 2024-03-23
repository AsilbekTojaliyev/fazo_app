from sqlalchemy import Column, String, Integer, and_, Text
from sqlalchemy.orm import relationship, backref
from db_connect import Base
from models.laptop import Laptops
from models.tablet import Tablets
from models.phone import Phones


class Files(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    new_files = Column(Text, nullable=False)
    source = Column(String(255), nullable=False)
    source_id = Column(Integer, nullable=False)

    laptop = relationship(argument="Laptops", foreign_keys=[source_id],
                          primaryjoin=lambda: and_(Laptops.id == Files.source_id, Files.source == "laptop"),
                          backref=backref("files"))
    planshet = relationship(argument="Tablets", foreign_keys=[source_id],
                            primaryjoin=lambda: and_(Tablets.id == Files.source_id, Files.source == "tablet"),
                            backref=backref("files"))
    telephone = relationship(argument="Phones", foreign_keys=[source_id],
                             primaryjoin=lambda: and_(Phones.id == Files.source_id, Files.source == "phone"),
                             backref=backref("files"))

