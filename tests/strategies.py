
from hypothesis import given, assume
import hypothesis.strategies as st
import unittest

import realalg

def is_square(n):
    ''' Return whether n > 1 is a square using the Babylonian algorithm. '''
    s = (len(str(n))-1) // 2
    x = (10**s) * 4  # A good guess for the root.

    A = set([x, n])
    while x * x != n:
        x = (x + (n // x)) >> 1
        if x in A:
            return False
        A.add(x)
    return True  # x = sqrt(n).

@st.composite
def intervals(draw, precision=None):
    if precision is None: precision = draw(st.integers(min_value=1, max_value=100))
    lower = draw(st.integers())
    upper = draw(st.integers(min_value=lower))
    return realalg.Interval(lower, upper, precision)

@st.composite
def realnumberfields(draw):
    while True:
        coeffs = draw(st.one_of(
            st.integers(min_value=2, max_value=50).filter(lambda n: not is_square(n)).map(lambda n: [-n, 0, 1]),
            ))
        print(coeffs)
        try:
            return realalg.RealNumberField(coeffs)
        except ValueError:  # Might be reducible or have no real roots.
            pass

@st.composite
def realalgebraics(draw, field=None):
    if field is None: field = draw(realnumberfields())
    coefficients = draw(st.lists(elements=st.integers()))
    assume(coefficients)
    return field(coefficients)


class TestStrategiesHealth(unittest.TestCase):
    @given(realnumberfields())
    def test_realnumberfields(self, K):
        self.assertIsInstance(K, realalg.RealNumberField)
    
    @given(realalgebraics())
    def test_realalgebraics(self, alpha):
        self.assertIsInstance(alpha, realalg.RealAlgebraic)
    
    @given(intervals())
    def test_intervals(self, I):
        self.assertIsInstance(I, realalg.interval.Interval)

