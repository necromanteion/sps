'''
Contains functions to calculate the nth partial sum of some commonly used Taylor series.
'''

import math


def partial_sum(func, n):
    '''
    Calculates the nth partial sum of func.

    Args:
        func: The single argument callable that takes an integer i and returns the ith term in the Taylor series
              expansion.
        n: The integer term to perform a sum up to.
    '''
    return sum(func(i) for i in range(n))


def exponential(x, n=10):
    '''
    Calculates the nth partial sum in the Taylor series expansion of e^x.

    Args:
        x: Numeric value to expand about.
        n: Non-negative integer term to calculate.
    '''

    def term(n):
        return x**n/math.factorial(n)

    return partial_sum(term, n)


def cos(x, n=10):
    '''
    Calculates the nth partial sum in the Taylor series expansion of cos(x).

    Args:
        x: Numeric value to expand about.
        n: Non-negative integer term to calculate.
    '''

    def term(n):
        return (-1)**n * x**(2*n)/math.factorial(2*n)

    return partial_sum(term, n)


def sin(x, n=10):
    '''
    Calculates the nth partial sum in the Taylor series expansion of sin(x).

    Args:
        x: Numeric value to expand about.
        n: Non-negative integer term to calculate.
    '''

    def term(n):
        return (-1)**n * x**(2*n + 1) / math.factorial(2*n + 1)

    return partial_sum(term, n)