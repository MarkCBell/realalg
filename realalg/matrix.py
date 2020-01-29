
''' A module for getting algebraic numbers from matrix eigenvectors. '''

from fractions import Fraction

import cypari as cp
import numpy as np

from .algebraic import RealNumberField

cp_x = cp.pari('x')

def rational(x):
    ''' Return the cypari rational as a Python rational. '''
    
    return Fraction(int(x.numerator()), int(x.denominator()))

def eigenvectors(matrix):
    ''' Return the `interesting` (eigenvalue, eigenvector) pairs of a given matrix.
    
    A pair is interesting if:
      - the eigenvalue is: real, greater than 1, has degree greater than 1 and has multiplicity 1.
      - all entries of the eigenvector are positive. '''
    
    M = cp.pari.matrix(*matrix.shape, entries=matrix.flatten())  # pylint: disable=not-an-iterable
    
    for polynomial, multiplicity in zip(*M.charpoly().factor()):
        if multiplicity > 1: continue
        
        degree = int(polynomial.poldegree())
        if degree == 1: continue
        
        try:
            K = RealNumberField([int(polynomial.polcoeff(i)) for i in range(degree+1)])  # It must be real to be interesting.
        except ValueError:  # No real roots.
            continue
        
        if K.lmbda <= 1: continue
        
        # Compute the kernel:
        a = cp_x.Mod(polynomial)
        kernel_basis = (M - a).matker()
        
        eigenvalue = K.lmbda
        eigenvector = np.array([K([rational(entry.lift().polcoeff(i)) for i in range(degree)]) for entry in kernel_basis[0]], dtype=object)
        assert np.array_equal(matrix.dot(eigenvector), eigenvalue * eigenvector)
        
        # Rescale to clear denominators for performance.
        scale = cp.pari.one()
        for entry in eigenvector:
            for coefficient in entry.coefficients:
                scale = scale.lcm(coefficient.denominator)
        scaled_eigenvector = eigenvector * int(scale)
        
        yield eigenvalue, scaled_eigenvector

