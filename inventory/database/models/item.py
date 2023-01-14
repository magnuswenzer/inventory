from sqlalchemy import Column, Date, String, Integer, Float, Boolean, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from .common import Repr, Base


class Item(Base, Repr):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    manufacturer = Column(String)
    barcode = Column(Integer, unique=True)
    weight = Column(Float)
    item_type_id = Column(Integer, ForeignKey('item_type.id'), nullable=False)  # FK
    item_type = relationship("ItemType", backref="items")
    uix_1 = UniqueConstraint(name, manufacturer, weight)