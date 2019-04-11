
from hypothesis import given
import hypothesis.strategies as st
import pickle
import unittest

import strategies

class TestRealAlgebraic(unittest.TestCase):
    @given(st.data())
    def test_add(self, data):
        K = data.draw(strategies.realnumberfields())
        alpha = data.draw(strategies.realalgebraics(field=K))
        beta = data.draw(strategies.realalgebraics(field=K))
        const = data.draw(st.integers())
        self.assertEqual(alpha, alpha)
        self.assertEqual(alpha + 0, alpha)
        self.assertEqual(alpha + beta, beta + alpha)
        self.assertEqual(alpha + const, const + alpha)
    
    @given(st.data())
    def test_conversion(self, data):
        K = data.draw(strategies.realnumberfields())
        alpha = data.draw(strategies.realalgebraics(field=K))
        beta = data.draw(strategies.realalgebraics(field=K))
        self.assertAlmostEqual(float(alpha + beta), float(alpha) + float(beta))
    
    @given(strategies.realalgebraics())
    def test_pickle(self, alpha):
        self.assertEqual(alpha, pickle.loads(pickle.dumps(alpha)))
