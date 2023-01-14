import datetime

from inventory import database


class Controller:

    def __init__(self, database_name=None):
        self._db = None
        self._db_name = database_name or 'inventory.db'
        if not self._db_name.endswith('.db'):
            self._db_name = f'{self._db_name}.db'

    def initiate_database(self, delete_existing=False):
        self._db = database.get_database(name=self._db_name, delete_existing=delete_existing)

    @property
    def database(self):
        return self._db

    def add_location(self, **kwargs):
        database.interact.add_to_table(self.database, table_name='location', **kwargs)

    def add_unit(self, **kwargs):
        loc = kwargs.get('location')
        if loc:
            kwargs['location'] = database.interact.get_objects(database=self.database, table_name='location', name=loc)[0]
        database.interact.add_to_table(self.database, table_name='unit', **kwargs)

    def add_item_type(self, **kwargs):
        database.interact.add_to_table(self.database, table_name='item_type', **kwargs)

    def add_item(self, **kwargs):
        item_type = kwargs.get('item_type')
        if item_type:
            kwargs['item_type'] = database.interact.get_objects(database=self.database, table_name='item_type',
                                                                name=item_type)[0]
        database.interact.add_to_table(self.database, table_name='item', **kwargs)

    def add_item_info(self, **kwargs):
        item_type = kwargs.get('item')
        if item_type:
            kwargs['item'] = database.interact.get_objects(database=self.database, table_name='item',
                                                           name=item_type)[0]
        unit = kwargs.get('unit')
        if unit:
            kwargs['unit'] = database.interact.get_objects(database=self.database, table_name='unit',
                                                           name=unit)[0]

        kwargs['added_date'] = datetime.datetime.now()
        database.interact.add_to_table(self.database, table_name='item_info', **kwargs)

    def get_objects_data(self, table_name: str = None, **kwargs):
        objs = database.interact.get_objects(database=self.database, table_name=table_name, **kwargs)
        return [database.interact.get_data_from_object(obj) for obj in objs]


if __name__ == '__main__':
    c = Controller()
    c.initiate_database(delete_existing=True)
    c.add_location(name='hall')
    c.add_unit(name='städskåp', location='hall')
    c.add_item_type(name='pasta')
    c.add_item(name='spagetti', item_type='pasta')
    c.add_item(name='penne', item_type='pasta')
    c.add_item_info(item='spagetti', unit='städskåp')

    item_data = c.get_objects_data(table_name='item')

