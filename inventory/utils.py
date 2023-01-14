import sys
from pathlib import Path


if getattr(sys, 'frozen', False):
    ROOT_DIRECTORY = Path(sys.executable).parent.parent
else:
    ROOT_DIRECTORY = Path(__file__).parent.parent



