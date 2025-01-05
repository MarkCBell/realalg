
''' A package for manipulating real algebraic numbers. '''

import importlib.metadata
__version__ = importlib.metadata.version('realalg')

from .cypari2_algebraic import RealNumberField, RealAlgebraic, eigenvectors  # noqa: F401
