
from hypothesis import given, assume
import hypothesis.strategies as st
import unittest

import realalg

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
            st.integers(min_value=2).map(lambda n: [-n, 0, 1]),
            ))
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

