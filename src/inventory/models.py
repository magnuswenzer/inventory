import datetime

from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select


class CategoryBase(SQLModel):
    name: str = Field(unique=True)


class Category(CategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    itemtypes: list["ItemType"] = Relationship(back_populates="category")


class CategoryCreate(CategoryBase):
    pass


class CategoryPublic(CategoryBase):
    id: int


class CategoryUpdate(SQLModel):
    name: str = None


class ItemTypeBase(SQLModel):
    name: str = Field(index=True)
    manufacturer: str | None
    barcode: int | None = Field(unique=True)
    weight: float | None

    category_id: int | None = Field(default=None, foreign_key="category.id")


class ItemType(ItemTypeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # name: str = Field(index=True)
    #manufacturer: str | None
    #barcode: int | None = Field(unique=True)
    #weight: float | None

    #category_id: int | None = Field(default=None, foreign_key="category.id")
    category: Category | None = Relationship(back_populates="itemtypes")
    #
    items: list["Item"] = Relationship(back_populates="itemtype")


class ItemTypePublic(ItemTypeBase):
    id: int


class ItemTypeCreate(ItemTypeBase):
    pass


class ItemTypeUpdate(ItemTypeBase):
    name: str | None
    manufacturer: str | None
    barcode: int | None
    weight: float | None


class LocationBase(SQLModel):
    name: str

class Location(LocationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # name: str
    units: list["Unit"] = Relationship(back_populates="location")


class LocationPublic(LocationBase):
    id: int


class LocationCreate(LocationBase):
    pass


class LocationUpdate(LocationBase):
    name: str | None








class UnitBase(SQLModel):
    # id: int | None = Field(default=None, primary_key=True)
    name: str

    location_id: int | None = Field(default=None, foreign_key="location.id")
    # location: Location | None = Relationship(back_populates="units")
    #
    # items: list["Item"] = Relationship(back_populates="unit")


class Unit(UnitBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # name: str

    # location_id: int | None = Field(default=None, foreign_key="location.id")
    location: Location | None = Relationship(back_populates="units")
    #
    items: list["Item"] = Relationship(back_populates="unit")

class UnitPublic(UnitBase):
    id: int


class UnitCreate(UnitBase):
    pass


class UnitUpdate(UnitBase):
    name: str | None

class ItemBase(SQLModel):
    date_added: datetime.datetime
    date_removed: datetime.datetime

    itemtype_id: int = Field(foreign_key="itemtype.id")
    # itemtype: ItemType | None = Relationship(back_populates="items")
    #
    unit_id: int = Field(foreign_key="unit.id")
    # unit: Unit | None = Relationship(back_populates="items")


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # itemtype_id: int = Field(foreign_key="itemtype.id")
    itemtype: ItemType | None = Relationship(back_populates="items")
    #
    # unit_id: int = Field(foreign_key="unit.id")
    unit: Unit | None = Relationship(back_populates="items")


class ItemPublic(ItemBase):
    id: int

    # itemtype_id: int = Field(foreign_key="itemtype.id")
    # itemtype: ItemType | None = Relationship(back_populates="items")
    #
    # unit_id: int = Field(foreign_key="unit.id")
    # unit: Unit | None = Relationship(back_populates="items")


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    date_added: datetime.datetime | None
    date_removed: datetime.datetime | None
    #
    # itemtype_id: int = Field(foreign_key="itemtype.id")
    # itemtype: ItemType | None = Relationship(back_populates="items")
    #
    # unit_id: int = Field(foreign_key="unit.id")
    # unit: Unit | None = Relationship(back_populates="items")




class CategoryPublicWithRelations(CategoryPublic):
    itemtypes: list[ItemTypePublic] = []


class ItemTypePublicWithRelations(ItemTypePublic):
    category: CategoryPublic | None = None
    items: list[ItemPublic] = []


class LocationPublicWithRelations(LocationPublic):
    units: list[UnitPublic] = []


class UnitPublicWithRelations(UnitPublic):
    location: LocationPublic | None = None
    items: list[ItemPublic] = []


class ItemPublicWithRelations(ItemPublic):
    itemtype: ItemTypePublic | None = None
    unit: UnitPublic | None = None



sqlite_file_name = "inventory.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


