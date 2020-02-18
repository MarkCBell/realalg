
''' A package for manipulating real algebraic numbers. '''

from importlib import import_module
import pkg_resources
__version__ = pkg_resources.get_distribution('realalg').version

# from .algebraic import RealNumberField, RealAlgebraic  # noqa: F401

INTERFACES = ['cypari', 'cypari2', 'sympy']
for interface in INTERFACES:
    try:
        module = import_module('realalg.{}_algebraic'.format(interface))
        RealNumberField = module.RealNumberField
        RealAlgebraic = module.RealAlgebraic
        eigenvectors = module.eigenvectors
        break
        # We could add some code here to find out which interface was loaded.
    except ImportError:
        pass
