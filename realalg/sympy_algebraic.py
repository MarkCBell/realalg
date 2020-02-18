
''' A module for representing and manipulating real algebraic numbers and the fields that they live in. '''

from fractions import Fraction
import sympy as sp
from .base_algebraic import BaseRealNumberField, BaseRealAlgebraic, log_plus

sp_Fraction = sp.polys.domains.PythonRational
sp_x = sp.Symbol('x')
sp_QQ_x = sp.QQ.old_poly_ring(sp_x)

class RealNumberField(BaseRealNumberField):
    ''' Represents the NumberField QQ(lmbda) = QQ[x] / << f(x) >> where lmbda is a real root of f(x). '''
    __engine = 'sympy'
    
    def __init__(self, coefficients, index=-1):  # List of integers and integer index
        super(RealNumberField, self).__init__(coefficients, index)
        self.sp_quotient_ring = sp_QQ_x.quotient_ring([self.sp_polynomial])
        self.lmbda = self([0, 1])
    
    def __call__(self, coefficients):
        return RealAlgebraic(self, self.sp_quotient_ring([sp_Fraction(coeff.numerator, coeff.denominator) for coeff in coefficients[::-1]]))

class RealAlgebraic(BaseRealNumberField):
    ''' Represents an element of a number field. '''
    __engine = 'sympy'
    
    def __init__(self, field, cp_mod):
        self.field = field
        self.cp_mod = cp_mod
        self.coefficients = [Fraction(coeff.numerator, coeff.denominator) for coeff in reversed(self.cp_mod.data.all_coeffs())]
        if not self.coefficients:
            self.coefficients = [Fraction(0, 1)]
        self.length = sum(log_plus(coefficient.numerator) + log_plus(coefficient.denominator) + index * self.field.length for index, coefficient in enumerate(self.coefficients))
    
    def minpoly(self):
        ''' Return the minimum polynomial of this algebraic number. '''
        return NotImplemented

def rational(x):
    ''' Return the sympy rational as a Python rational. '''
    return Fraction(int(x))

def eigenvectors(matrix):
    
    width, height = matrix.shape
    assert width == height
    
    M = sp.Matrix(matrix)
    char_poly = sp_QQ_x([int(coeff) for coeff in M.charpoly().all_coeffs()])  # Convert to DMP.
    
    for polynomial, multiplicity in char_poly.factor_list()[1]:
        if multiplicity > 1: continue
        
        degree = polynomial.degree()
        if degree == 1: continue
        
        poly_coefficients = [int(coeff) for coeff in polynomial.all_coeffs()[::-1]]
        try:
            K = RealNumberField(poly_coefficients)
        except ValueError:  # No real roots.
            continue
        
        if K.lmbda <= 1: continue
        
        companion_matrix = sp.Matrix([[-poly_coefficients[j] if i == degree-1 else 1 if i == j-1 else 0 for i in range(degree)] for j in range(degree)])
        eye_D = sp.eye(degree)
        eye_M = sp.eye(width)
        
        representation = sp.kronecker_product(M, eye_D) - sp.kronecker_product(eye_M, companion_matrix)
        
        # Compute the kernel:
        kernel = representation.nullspace()
        assert len(kernel) == degree
        
        null_vector = kernel[0]
        
        eigenvalue = K.lmbda
        eigenvector = np.array([K([rational(null_vector[degree*i + j]) for j in range(degree)]) for i in range(width)], dtype=object)
        assert np.array_equal(matrix.dot(eigenvector), eigenvalue * eigenvector)
        
        # Rescale to clear denominators for performance.
        scale = sp.lcm_list([coeff.denominator for entry in eigenvector for coeff in entry.coefficients])
        scaled_eigenvector = eigenvector * int(scale)
        
        yield eigenvalue, scaled_eigenvector

