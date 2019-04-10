
from hypothesis import given
import hypothesis.strategies as st
import pickle
import unittest

import strategies

class TestInterval(unittest.TestCase):
    @given(st.data())
    def test_add(self, data):
        I = data.draw(strategies.intervals())
        J = data.draw(strategies.intervals(precision=I.precision))
        self.assertEqual(I + 0, I)
        self.assertEqual(I + J, J + I)
        self.assertGreaterEqual((I + J).accuracy, min(I.accuracy, J.accuracy) - 1)
    
    @given(strategies.intervals())
    def test_pickle(self, I):
        self.assertEqual(I, pickle.loads(pickle.dumps(I)))
