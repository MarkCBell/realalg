
''' A package for manipulating real algebraic numbers. '''

from .algebraic import RealNumberField, RealAlgebraic  # noqa: F401

import pkg_resources
__version__ = pkg_resources.get_distribution('realalg').version

