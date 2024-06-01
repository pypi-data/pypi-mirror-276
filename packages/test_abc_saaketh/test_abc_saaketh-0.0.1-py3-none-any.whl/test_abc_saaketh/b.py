from .a import function_a
from .c import function_c

def function_b():
    return function_a(function_c(100, 100))
