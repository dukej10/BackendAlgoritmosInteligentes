# Implementation by Andreas Krause (krausea@gmail.com)
# Takes a function handle fn (a set function, mapping an array to a real
# number), and wraps it as a sfo_fn object
# Example: fn = @(A) length(sfo_unique_fast(A)); F = sfo_fn_wrapper(fn); F([1 2 2 4 3])
    
from . import fn as sfofn

def sfo_fn_wrapper(fn = None): 
    F.fn = fn
    F = class_(F,'sfo_fn_wrapper',sfofn.sfo_fn)
    return F