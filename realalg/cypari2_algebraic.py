
''' A module for representing and manipulating real algebraic numbers and the fields that they live in using cypari2. '''

from fractions import Fraction
import numpy as np
import cypari2  # pylint: disable=import-error
from .base_algebraic import BaseRealNumberField, BaseRealAlgebraic

cp = cypari2.Pari()
cp_x = cp('x')

def cp_polynomial(coefficients):
    ''' Return a cypari2 polynomial from its coefficients. '''
    return cp(' + '.join('{}*x^{}'.format(coefficient, index) for index, coefficient in enumerate(coefficients)))

class RealNumberField(BaseRealNumberField):
    ''' Represents the NumberField QQ(lmbda) = QQ[x] / << f(x) >> where lmbda is a real root of f(x). '''
    __engine = 'cypari2'
    
    def __init__(self, coefficients, index=-1):  # List of integers and / or Fractions, integer index
        super(RealNumberField, self).__init__(coefficients, index)
        self.cp_polynomial = cp_polynomial(self.coefficients)
        self.lmbda = self([0, 1])
    
    def __call__(self, coefficients):
        return RealAlgebraic(self, cp_polynomial(coefficients).Mod(self.cp_polynomial))

class RealAlgebraic(BaseRealAlgebraic):
    ''' Represents an element of a number field. '''
    __engine = 'cypari2'
    @staticmethod
    def _extract(rep):
        if rep == 0:
            return [Fraction(0, 1)]
        
        polynomial = rep.lift()
        length = polynomial.poldegree()
        return [Fraction(int(polynomial.polcoef(i).numerator()), int(polynomial.polcoef(i).denominator())) for i in range(length+1)]
    
    def minpoly(self):
        ''' Return the (cypari) minimum polynomial of this algebraic number. '''
        return self.rep.minpoly()
    def degree(self):
        ''' Return the degree of this algebraic number. '''
        return self.minpoly().poldegree()

def rational(x):
    ''' Return the cypari rational as a Python rational. '''
    return Fraction(int(x.numerator()), int(x.denominator()))

def eigenvectors(matrix):
    ''' Return the `interesting` (eigenvalue, eigenvector) pairs of a given matrix.
    
    A pair is interesting if:
      - the eigenvalue is: real, greater than 1, has degree greater than 1 and has multiplicity 1.
      - all entries of the eigenvector are non-negative. '''
    
    M = cp.matrix(*matrix.shape, entries=matrix.flatten())  # pylint: disable=not-an-iterable
    
    for polynomial, multiplicity in zip(*M.charpoly().factor()):
        if multiplicity > 1: continue
        
        degree = int(polynomial.poldegree())
        if degree == 1: continue
        
        try:
            K = RealNumberField([int(polynomial.polcoef(i)) for i in range(degree+1)])  # It must be real to be interesting.
        except ValueError:  # No real roots.
            continue
        
        if K.lmbda <= 1: continue
        
        # Compute the kernel:
        a = cp_x.Mod(polynomial)
        kernel_basis = (M - a).matker()
        
        eigenvalue = K.lmbda
        eigenvector = np.array([K([rational(entry.lift().polcoef(i)) for i in range(degree)]) for entry in kernel_basis[0]], dtype=object)
        assert np.array_equal(matrix.dot(eigenvector), eigenvalue * eigenvector)
        
        if all(entry <= 0 for entry in eigenvector):
            eigenvector = -eigenvector
        
        if any(entry < 0 for entry in eigenvector): continue
        
        # Rescale to clear denominators for performance.
        scale = cp.one()
        for entry in eigenvector:
            for coefficient in entry.coefficients:
                scale = scale.lcm(coefficient.denominator)
        eigenvector = eigenvector * int(scale)
        
        yield eigenvalue, eigenvector

