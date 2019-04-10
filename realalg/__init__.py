
''' A package for manipulating real algebraic numbers. '''

import pkg_resources
__version__ = pkg_resources.get_distribution('realalg').version

from .algebraic import RealNumberField, RealAlgebraic  # noqa: F401
from .interval import Interval  # noqa: F401

