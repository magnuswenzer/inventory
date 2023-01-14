import logging
import pathlib

from inventory.utils import ROOT_DIRECTORY

logger = logging.getLogger(__file__)


def get_default_database_path(name: str = None):
    file_name = name or 'inventory.db'
    return pathlib.Path(ROOT_DIRECTORY, 'inventory', file_name)


def check_database_path(path: pathlib.Path):
    if path.suffix != '.db':
        msg = f'Not a database path: {path}'
        logger.error(msg)
        raise Exception(msg)


def get_database_path(name: str = None, path: str | pathlib.Path = None) -> pathlib.Path:
    if path:
        path = pathlib.Path(path).absolute()
    else:
        path = get_default_database_path(name)
    check_database_path(path)
    return path
