from importlib.metadata import metadata

from . import filesystem
from . import module
from . import parser

m = metadata('cohesion')

__name__ = m['Name']
__version__ = m['Version']
__description__ = m['Summary']
__url__ = m['Home-page']
__license__ = m['License']
__all__ = [
    'filesystem',
    'module',
    'parser',
]
