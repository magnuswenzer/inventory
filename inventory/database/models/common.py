from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Repr:

    def __str__(self):
        return f'Model: {self.__tablename__}: {self.id}'

    def __repr__(self) -> str:
        return f'Model: {self.__tablename__}: {self.id}'