

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

    def test_matrix2(self):
        M = np.array([
            [66001, 59627, -90134, -66002, -55601, 86110],
            [12079, 11127, -16746, -12079, -10298, 15918],
            [22852, 20850, -31447, -22852, -19368, 29966],
            [15009, 13532, -20464, -15010, -12628, 19562],
            [42230, 37989, -57480, -42230, -35482, 54974],
            [22536, 20338, -30750, -22536, -18972, 29385]
            ], dtype=object)
        list(realalg.eigenvectors(M))

