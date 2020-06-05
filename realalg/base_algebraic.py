
''' A module for representing and manipulating real algebraic numbers and the fields that they live in. '''

from abc import ABCMeta, abstractmethod
from fractions import Fraction
from functools import total_ordering
from math import log10 as log
from numbers import Integral
import six
import sympy as sp

from .interval import Interval

sp_x = sp.Symbol('x')
sp_QQ_x = sp.QQ.old_poly_ring(sp_x)
LOG_2 = log(2)

def log_plus(x):
    ''' Return the height of the number ``x``. '''
    return log(max(1, abs(x)))

class BaseRealNumberField(object):
    ''' Represents the NumberField QQ(lmbda) = QQ[x] / << f(x) >> where lmbda is a real root of f(x). '''
    def __init__(self, coefficients, index=-1):  # List of integers and integer index
        if len(coefficients) < 3:
            raise ValueError('Degree of Polynomial must be at least two')
        if not coefficients[-1]:
            raise ValueError('Leading coefficient must be non-zero')
        self.coefficients = coefficients  # List of integers.
        self.index = index
        self.sp_polynomial = sp_QQ_x(self.coefficients[::-1])
        if not self.sp_polynomial.is_irreducible:
            raise ValueError('Polynomial {} is reducible'.format(self.sp_polynomial))
        self.degree = self.sp_polynomial.degree()
        self.length = sum(LOG_2 + log_plus(coefficient.numerator) + log_plus(coefficient.denominator) for coefficient in self.coefficients)
        self.log_bound = log(sum(abs(coefficient) for coefficient in self.coefficients))  # log(self.sp_place) must be less than this.
        real_roots = sp.Poly(self.coefficients[::-1], sp_x).real_roots()
        if not real_roots:
            raise ValueError('Polynomial {} has no real roots'.format(self.sp_polynomial))
        self.sp_place = real_roots[index]
        self._accuracy = 0
        self._intervals = None
        self.lmbda = None  # To be created by instances.
    
    def __str__(self):
        return 'QQ[x] / <<{}>> embedding x |--> {}'.format(sp.Poly(self.sp_polynomial.all_coeffs(), sp_x).as_expr(), self.lmbda)
    def __repr__(self):
        return 'RealNumberField({})'.format(self.coefficients)
    def __hash__(self):
        return hash(tuple(self.coefficients) + (self.index,))
    def __reduce__(self):
        return (self.__class__, (self.coefficients,))
    
    def intervals(self, accuracy):
        ''' Return intervals around self.lmbda**i with at least the requested accuracy. '''
        assert isinstance(accuracy, Integral)
        assert accuracy > 0
        if accuracy > self._accuracy:
            precision = int(accuracy + self.degree*self.log_bound + 1) + 1  # Cheap ceil.
            s = str(sp.N(self.sp_place, precision))
            interval = Interval.from_string(s, precision)
            self._intervals = [interval**i for i in range(self.degree)]
            assert all(I.accuracy >= accuracy for I in self._intervals)
            self._accuracy = accuracy
        return [I.simplify(accuracy+1) for I in self._intervals]

@total_ordering
@six.add_metaclass(ABCMeta)
class BaseRealAlgebraic(object):
    ''' Represents an element of a number field. '''
    __engine = 'base'
    @staticmethod
    def _extract(rep):
        return [Fraction(coeff.numerator, coeff.denominator) for coeff in reversed(rep.data.all_coeffs())]
    
    def __init__(self, field, rep):
        self.field = field
        self.rep = rep
        self.coefficients = self._extract(rep)
        if not self.coefficients:
            self.coefficients = [Fraction(0, 1)]
        self.length = sum(LOG_2 + log_plus(coefficient.numerator) + log_plus(coefficient.denominator) + index * self.field.length for index, coefficient in enumerate(self.coefficients))
    def __str__(self):
        return str(self.N())
    def __repr__(self):
        return '{!r}([{}])'.format(self.field, ', '.join(str(coeff) for coeff in self.coefficients))
    def __reduce__(self):
        return (self.field, (self.coefficients,))
    def __bool__(self):
        return self.coefficients != [Fraction(0, 1)]
    def __nonzero__(self):  # For Python2.
        return self.__bool__()
    def __pos__(self):
        return self
    def __add__(self, other):
        if isinstance(other, BaseRealAlgebraic):
            return self.__class__(self.field, self.rep + other.rep)
        elif isinstance(other, (Fraction, Integral)):
            return self + self.field([other])
        elif isinstance(other, float):
            return float(self) + other
        else:
            return NotImplemented
    def __radd__(self, other):
        return self + other
    def __sub__(self, other):
        return self + (-other)
    def __rsub__(self, other):
        return other + (-self)
    def __neg__(self):
        return self.__class__(self.field, -self.rep)
    def __abs__(self):
        return self if self > 0 else -self
    def __mul__(self, other):
        if isinstance(other, BaseRealAlgebraic):
            return self.__class__(self.field, self.rep * other.rep)
        elif isinstance(other, (Fraction, Integral)):
            return self * self.field([other])
        elif isinstance(other, float):
            return float(self) * other
        else:
            return NotImplemented
    def __rmul__(self, other):
        return self * other
    def __div__(self, other):
        return self.__truediv__(other)
    def __floordiv__(self, other):
        if other == 0:
            raise ZeroDivisionError
        
        return int(self / other)
        # Something like:
        #   accuracy = int(self.length + other.length) + 1
        #   I = self.interval(accuracy)
        #   J = other.interval(accuracy)
        #   return I.upper // J.lower
        # Should be much more efficient.
    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError('division by zero')
        if isinstance(other, BaseRealAlgebraic):
            return self.__class__(self.field, self.rep / other.rep)
        elif isinstance(other, (Fraction, Integral)):
            return self / self.field([other])
        elif isinstance(other, float):
            return float(self) / other
        else:
            return NotImplemented
    def __rdiv__(self, other):
        return self.__rtruediv__(other)
    def __rtruediv__(self, other):
        if isinstance(other, (Fraction, Integral)):
            return self.field([other]) / self
        else:
            return NotImplemented
    def __mod__(self, other):
        return self - (self // other) * other
    def __pow__(self, other):
        if isinstance(other, Integral):
            return self.__class__(self.field, self.rep ** other)
        else:
            return NotImplemented
    
    @abstractmethod
    def minpoly(self):
        ''' Return the minimum polynomial of this algebraic number. '''
    
    def degree(self):
        ''' Return the degree of this algebraic number. '''
        return self.minpoly().degree()
    
    def interval(self, accuracy=8):
        ''' Return an interval around self with at least the requested accuracy. '''
        intermediate_accuracy = int(accuracy + max(log_plus(coefficient) for coefficient in self.coefficients) + len(self.coefficients)) + 1
        interval = sum(coeff * interval for coeff, interval in zip(self.coefficients, self.field.intervals(intermediate_accuracy)))
        assert interval.accuracy >= accuracy
        return interval.simplify(accuracy+1)
    def N(self, accuracy=8):
        ''' Return a string approximating self to at least ``accuracy`` digits. '''
        return self.interval(accuracy).midpoint()
    def __int__(self):
        return int(self.interval())
    def __float__(self):
        return float(self.N(64))
    def sign(self):
        ''' Return the sign of this real number. '''
        if not any(self.coefficients):  # self == 0.
            return 0
        
        d = 1
        while True:
            potential_sign = self.interval(accuracy=d).sign()
            if potential_sign:  # sign is 'obvious' at this point.
                return potential_sign
            if d > 2*int(self.length+1):
                raise RuntimeError('Should be zero')  # self == 0.
            d = d * 2
    
    def __eq__(self, other):
        return not self - other
    def __gt__(self, other):
        return (self - other).sign() == +1
    def __lt__(self, other):
        return (self - other).sign() == -1
    def __hash__(self):
        return hash(tuple(self.coefficients))

