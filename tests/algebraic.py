
from hypothesis import given, assume
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
    def test_int(self, data):
        K = data.draw(strategies.realnumberfields())
        alpha = data.draw(strategies.realalgebraics(field=K))
        n = int(alpha)
        self.assertLessEqual(n, alpha)
        self.assertLess(alpha, n+1)
    
    @given(st.data())
    def test_floordiv(self, data):
        K = data.draw(strategies.realnumberfields())
        alpha = data.draw(strategies.realalgebraics(field=K))
        beta = data.draw(strategies.realalgebraics(field=K))
        assume(beta != 0)
        self.assertEqual(alpha // beta, int(alpha / beta))
    
    @given(strategies.realalgebraics())
    def test_pickle(self, alpha):
        self.assertEqual(alpha, pickle.loads(pickle.dumps(alpha)))

