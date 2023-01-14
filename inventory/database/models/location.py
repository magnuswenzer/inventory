from sqlalchemy import Column, Date, String, Integer, Float, Boolean, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from .common import Repr, Base


class Location(Base, Repr):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)