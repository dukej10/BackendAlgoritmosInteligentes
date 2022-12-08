# Helper for quickly computing the unique set representation
# Author: Andreas Krause (krausea@gmail.com)
#
# function C=sfo_unique_fast(A)
# A: set (array) of positive integers
#
# Example: C = sfo_unique_fast([1 3 3 7 2 3 2 8])

import numpy as np
    
def sfo_unique_fast(A = None): 
    mx = np.amax(A)
    vals = np.zeros((1,mx))
    vals[A] = 1
    C = np.where(vals)
    return C