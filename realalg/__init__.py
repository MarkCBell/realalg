
''' A package for manipulating real algebraic numbers. '''

from importlib import import_module
import importlib.metadata
__version__ = importlib.metadata.version('realalg')

# from .algebraic import RealNumberField, RealAlgebraic  # noqa: F401

INTERFACES = ['cypari', 'cypari2', 'sympy']
for interface in INTERFACES:
    try:
        module = import_module(f'realalg.{interface}_algebraic')
        RealNumberField = module.RealNumberField
        RealAlgebraic = module.RealAlgebraic
        eigenvectors = module.eigenvectors
        break
        # We could add some code here to find out which interface was loaded.
    except ImportError:
        pass
