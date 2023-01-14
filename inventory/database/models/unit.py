from sqlalchemy import Column, Date, String, Integer, Float, Boolean, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from .common import Repr, Base


class Unit(Base, Repr):
    __tablename__ = 'unit'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    location_id = Column(Integer, ForeignKey('location.id'))  # FK
    location = relationship("Location", backref="units")