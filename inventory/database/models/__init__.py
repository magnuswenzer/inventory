
from .location import Location
from .unit import Unit
from .item_type import ItemType
from .item import Item
from .item_info import ItemInfo

from .common import Base


TABLE_MAPPING = {
    Location.__tablename__: Location,
    Unit.__tablename__: Unit,
    ItemType.__tablename__: ItemType,
    Item.__tablename__: Item,
    ItemInfo.__tablename__: ItemInfo,

}

