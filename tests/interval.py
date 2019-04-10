
from hypothesis import given
import hypothesis.strategies as st
import pickle
import unittest

import strategies

class TestInterval(unittest.TestCase):
    @given(st.data())
    def test_add(self, data):
        pass
    
    @given(strategies.intervals())
    def test_pickle(self, I):
        self.assertEqual(I, pickle.loads(pickle.dumps(I)))
