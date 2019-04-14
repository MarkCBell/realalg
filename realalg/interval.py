
''' A module for representing and manipulating intervals. '''

from fractions import Fraction
from numbers import Integral

class Interval(object):
    ''' This represents a closed interval [lower / 10**precision, upper / 10**precision]. '''
    def __init__(self, lower, upper, precision):
        assert isinstance(lower, Integral)
        assert isinstance(upper, Integral)
        assert isinstance(precision, Integral)
        if lower > upper: raise ValueError('Interval is empty')
        if precision < 1: raise ValueError('Interval must have precision at least 1')
        
        self.lower = lower
        self.upper = upper
        self.precision = precision
        self.accuracy = self.precision if self.upper == self.lower else self.precision - len(str(abs(self.upper - self.lower)))
    
    @classmethod
    def from_string(cls, string, precision=None):
        ''' A short way of constructing Intervals from a string. '''
        
        if '.' not in string:
            raise ValueError('invalid specification of interval: {}'.format(string))
        if 'e' in string:
            d, _, p = string.partition('e')
            p = int(p)
            if p < 0:
                string = ('-' if d.startswith('-') else '') + '0.' + '0' * (-1-p) + d.replace('.', '').replace('-', '')
            else:
                i, r = d.split('.')
                string = i + r[:p] + '.' + r[p:]
        
        if precision is None: precision = len(string.split('.')[1])
        
        i, r = string.split('.')
        lower = int(i + r[:precision] + '0' * (precision - len(r)))
        upper = lower + 10**max(precision - len(r), 0)
        return cls(lower, upper, precision)
    
    @classmethod
    def from_integer(cls, integer, precision):
        ''' A short way of constructing Intervals from a fraction. '''
        
        return cls(integer*10**precision, integer*10**precision, precision)
    
    @classmethod
    def from_fraction(cls, fraction, precision):
        ''' A short way of constructing Intervals from a fraction. '''
        
        return cls((fraction.numerator*10**precision - 1) // fraction.denominator, (fraction.numerator*10**precision + 1) // fraction.denominator, precision)
    
    def __repr__(self):
        return str(self)
    def __str__(self):
        p = self.precision
        l, u = str(self.lower).zfill(p + (1 if self.lower >= 0 else 2)), str(self.upper).zfill(p + (1 if self.lower >= 0 else 2))
        return '[{}.{}, {}.{}]'.format(l[:-p], l[-p:], u[:-p], u[-p:])
    def __eq__(self, other):
        if not isinstance(other, Interval):
            return NotImplemented
        
        return self.lower == other.lower and self.upper == other.upper and self.precision == other.precision
    def __ne__(self, other):
        return not self == other
    
    def __add__(self, other):
        if isinstance(other, Interval):
            assert self.precision == other.precision
            values = [
                self.lower + other.lower,
                self.upper + other.upper
                ]
            return Interval(min(values), max(values), self.precision)
        elif isinstance(other, Integral):
            return self + Interval.from_integer(other, self.precision)
        elif isinstance(other, Fraction):
            return self + Interval.from_fraction(other, self.precision)
        else:
            return NotImplemented
    def __radd__(self, other):
        return self + other
    def __sub__(self, other):
        return self + (-other)
    def __neg__(self):
        return Interval(-self.upper, -self.lower, self.precision)
    def __mul__(self, other):
        if isinstance(other, Interval):
            assert self.precision == other.precision
            values = [
                self.lower * other.lower // 10**self.precision,
                self.upper * other.lower // 10**self.precision,
                self.lower * other.upper // 10**self.precision,
                self.upper * other.upper // 10**self.precision
                ]
            return Interval(min(values), max(values), self.precision)
        elif isinstance(other, Integral):
            return self * Interval.from_integer(other, self.precision)
        elif isinstance(other, Fraction):
            return self * Interval.from_fraction(other, self.precision)
        else:
            return NotImplemented
    def __rmul__(self, other):
        return self * other
    def __pow__(self, power):
        I = Interval.from_integer(1, self.precision)
        powered = self
        while power:
            if power & 1: I *= powered
            powered *= powered
            power >>= 1
        return I
    
    def __int__(self):
        return self.upper // 10**self.precision
    
    def midpoint(self):
        ''' Return a string describing the midpoint of this interval. '''
        m = (self.lower + self.upper) // 2
        ms = str(m).zfill(self.precision + (1 if m >= 0 else 2))  # Amount of padding depends upon sign.
        return '{}.{}'.format(ms[:-self.precision], ms[-self.precision:])
    
    def simplify(self, new_precision):
        ''' Return a larger interval containing this of the given precision. '''
        if new_precision > self.precision:
            raise ValueError('new_precision must be less than or equal to self.precision')
        
        d = self.precision - new_precision
        return Interval(self.lower // 10**d, -(-self.upper // 10**d), new_precision)  # Divide and round down / up without using math.ceil.
    
    def sign(self):
        ''' Return the sign of this interval.
        
        This is +1 if the entire interval is > 0; -1 if the entire interval is < 0 and 0 otherwise. '''
        if self.upper < 0:
            return -1
        elif self.lower > 0:
            return 1
        else:
            return 0

