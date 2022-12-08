# Helper for quickly computing the set difference
# Author: Andreas Krause (krausea@gmail.com)
#
# function C=sfo_setdiff_fast(A,B)
# A, B: sets (arrays) of positive integers
#
# Example: C = sfo_setdiff_fast([1 3 7 8], [3 7])

import numpy as np
    
def sfo_setdiff_fast(A = None,B = None): 
    mx = np.amax(np.array([np.amax(A),np.amax(B)]))
    vals = np.zeros((1,mx))
    vals[A] = 1
    vals[B] = 0
    C = find(vals)
    return C