import logging
import os
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from inventory.database import db_path
from inventory.database.models import Base

logger = logging.getLogger(__file__)


class Database:

    def __init__(self, path: pathlib.Path):
        self._path = path
        self._engine = None
        self._session = None
        self._create_engine()
        self._make_session()

    def _create_engine(self):
        self._engine = create_engine(f'sqlite:///{self._path}', echo=True)
        # self._engine = create_engine(f'sqlite:///{self._path}', echo=False)

    def _make_session(self):
        self.Session = sessionmaker(bind=self._engine)

    def create_tables(self):
        Base.metadata.create_all(self._engine)

    def _open_session(self):
        self._session = self.Session()
        print('OPEN SESSION')

    @property
    def session(self):
        if not self._session:
            self._open_session()
        return self._session

    def commit(self):
        self._commit()

    def close_session(self):
        self._close_session()

    def _commit(self) -> None:
        self._session.commit()
        try:
            self._session.commit()
            print('try')
            print('COMMIT')
        except IntegrityError:
            self._session.rollback()
            print('except')
        finally:
            self._close_session()

    def _close_session(self):
        if self._session is None:
            print('SESSION IS NONE')
            return
        self._session.close()
        self._session = None
        print('SESSION CLOSED')


def delete_database(name: str = None, path: str | pathlib.Path = None) -> bool:
    path = db_path.get_database_path(name=name, path=path)
    if not path.exists():
        logger.info(f'Database does not exist: {path}')
        return False
    os.remove(path)
    logger.info(f'Database removed: {path}')
    return True


def get_database(name: str = None, path: str | pathlib.Path = None, delete_existing: bool = False):
    if delete_existing:
        delete_database(name=name, path=path)
    path = db_path.get_database_path(name=name, path=path)
    db = Database(path)
    # if delete_existing:
    #     db.create_tables()
    db.create_tables()
    return db


def get_table_names():
    return [cls.__tablename__ for cls in Base.__subclasses__()]


def _get_table_class(table_name: str) -> Base:
    for cls in Base.__subclasses__():
        if cls.__tablename__ == table_name:
            return cls


def add_to_table(database: Database, table_name: str, **kwargs):
    cls = _get_table_class(table_name)
    print('='*50)
    print('='*50)
    print('='*50)
    for key, value in kwargs.items():
        print(key, value, type(value))
    obj = cls(**kwargs)
    # database.close_session()
    database.session.add(obj)
    database.commit()
    # database.close_session()
    return obj


def update_table(database: Database, table_name: str, **kwargs):
    _id = kwargs.pop('id', None)
    if _id is None:
        return False
    cls = _get_table_class(table_name)
    obj = database.session.query(cls).filter(cls.id == _id).first()
    for key, value in kwargs.items():
        if key in get_table_names():
            continue
        setattr(obj, key, value)
    database.session.commit()
    return True


def delete_obj(database: Database, obj: Base):
    database.session.delete(obj)
    database.session.commit()


def get_data_from_object(obj):
    data = {}
    for key, value in obj.__dict__.items():
        if key.startswith('_'):
            continue
        data[key] = value
    return data


def get_objects(database: Database, table_name: str, **kwargs):
    cls = _get_table_class(table_name)
    query = database.session.query(cls)
    for key, value in kwargs.items():
        query = query.filter(getattr(cls, key) == value)
    return query.all()


