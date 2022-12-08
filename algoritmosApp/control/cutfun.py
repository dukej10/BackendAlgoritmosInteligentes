# Implementation of a (directed) cut function
# Author: Andreas Krause (krausea@gmail.com)
#
# function C = sfo_fn_cutfun(G,A)
# G: Adjacency matrix of the graph
# A: subset of vertices to measure cut *from*
#
# Example: G = [1 1 0; 1 0 1; 0 1 1]; F = sfo_fn_cutfun(G); F([1 3])

import numpy as np
from . import setdiff
from . import uniqueFast
from . import wrapper
    
def sfo_fn_cutfun(G = None): 
    fn = lambda A = None: eval_cut_fn(G,A)
    F = wrapper.sfo_fn_wrapper(fn)
    return F
    
def eval_cut_fn(G = None,A = None): 
    A = uniqueFast.sfo_unique_fast(A)
    n = G.shape[1-1]
    C = sum(sum(G(A,setdiff.sfo_setdiff_fast(np.arange(1,n+1),A))))
    return C