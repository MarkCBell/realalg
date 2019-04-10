
from hypothesis import given, assume
import hypothesis.strategies as st
import unittest

import realalg

@st.composite
def intervals(draw, precision=None):
    if precision is None: precision = draw(st.integers(min_value=1, max_value=100))
    lower = draw(st.integers())
    upper = draw(st.integers(min_value=lower))
    return realalg.interval.Interval(lower, upper, precision)

@st.composite
def realnumberfields(draw, degree=None):
    if degree is None: degree = draw(st.integers(min_value=2, max_value=10))
    while True:
        coeffs = draw(st.lists(elements=st.integers(), min_size=degree, max_size=degree)) + [1]
        assume(coeffs[0])
        try:  # Only 1 / degree of the polynomials are irreducible.
            return realalg.RealNumberField(coeffs)
        except ValueError:
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


if __name__ == '__main__':
    unittest.main()

