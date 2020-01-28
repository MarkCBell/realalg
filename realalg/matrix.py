
import cypari
import numpy as np

import realalg

def eigenvectors(matrix):
    ''' Return the `interesting` (eigenvalue, eigenvector) pairs of a given matrix.
    
    A pair is interesting if:
      - the eigenvalue is: real, greater than 1, has degree greater than 1 and has multiplicity 1.
      - all entries of the eigenvector are positive. '''
    
    x = cypari.pari('x')
    
    M = cypari.pari.matrix(*matrix.shape, entries=matrix.flatten())  # pylint: disable=not-an-iterable
    
    for polynomial, multiplicity in zip(*M.charpoly().factor()):
        if multiplicity > 1: continue
        
        degree = int(polynomial.poldegree())
        if degree == 1: continue
        
        try:
            K = realalg.RealNumberField([int(polynomial.polcoeff(i)) for i in range(degree+1)])  # It must be real to be interesting.
        except ValueError:  # No real roots.
            continue
        
        if K.lmbda <= 1: continue
        
        # Compute the kernel:
        a = x.Mod(polynomial)
        kernel_basis = (M - a).matker()
        
        eigenvalue = K.lmbda
        eigenvector = np.array([K([entry.lift().polcoeff(i) for i in range(degree)]) for entry in kernel_basis[0]], dtype=object)
        assert np.array_equal(matrix.dot(eigenvector), eigenvalue * eigenvector)
        
        yield eigenvalue, eigenvector
    
    return
