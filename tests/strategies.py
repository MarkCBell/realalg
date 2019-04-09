
from hypothesis import given, assume
import hypothesis.strategies as st
import pytest
import unittest

import realalg

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

class TestStrategiesHealth(unittest.TestCase):
    @given(realnumberfields())
    def test_realnumberfields(self, K):
        self.assertIsInstance(K, realalg.RealNumberField)


if __name__ == '__main__':
    unittest.main()

