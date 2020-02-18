

import numpy as np
import realalg
import unittest

class TestRegression(unittest.TestCase):
    def assertEqualArray(self, M, N):
        self.assertTrue(np.array_equal(M, N), msg='AssertionError: %s != %s' % (M, N))
    
    def test_matrix(self):
        M = np.array([[0, -2, 3], [-1, -4, 6], [-2, -7, 10]])
        Vs = list(realalg.eigenvectors(M))
        self.assertEqual(len(Vs), 1)
        d, V = Vs[0]
        K = realalg.RealNumberField([1, -5, 1])
        self.assertEqual(d, K([0, 1]))
        self.assertEqualArray(V, np.array([K([-3, 1]), K([8, -1]), K([5])], dtype=object))

