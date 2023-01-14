from sqlalchemy import Column, Date, String, Integer, Float, Boolean, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from .common import Repr, Base


class ItemInfo(Base, Repr):
    __tablename__ = 'item_info'
    id = Column(Integer, primary_key=True)
    added_date = Column(Date, nullable=False)
    removed_date = Column(Date)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)  # FK
    item = relationship("Item", backref="item_infos")
    unit_id = Column(Integer, ForeignKey('unit.id'), nullable=False)  # FK
    unit = relationship("Unit", backref="item_infos")
