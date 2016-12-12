"""
beal.py

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

Exhaustive search method for finding solutions (and possibly counterexamples) to Beal's conjecture.
That is asearch for positive integers x,m,y,n,z,r such that:
x^m + y^n = z^r
m,n,r > 2 
and x,y,z are co-prime pairwise with no common factor.

Read more: http://www.businessinsider.com/math-problems-that-you-can-solve-to-earn-prizes-2013-7#ixzz2ZGPmrpul

The program suggests the conjecture is valid, however, may need to extend the program to go to very large
numbers and exponents in order to be more confident (need more computing power to do this)

Edit: Added pecentage completion of number space during execution. Can introduce dynamic programming to be more efficient.
Chris Buonocore
"""
import time
from decimal import Decimal

# VAR_LIMITS initial setting defines the solution space of a,b,c,x,y,z that will be searched by the program.
# VAR_LIMITS = (x_limit,y_limit,z_limit,a_limit,b_limit,c_limit).
VAR_LIMITS = (10,10,10,6,6,6)
EPS = 10**(-20)

def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

def gcd(x, y):
    while x:
        x, y = y % x, x
    return y

def nth_root(base, n): 
    return long(round(base ** (1.0/n)))

def timer(b, p):
    start = time.clock()
    beal(b, p)
    secs = time.clock() - start
    return {'secs': secs, 'mins': secs/60, 'hrs': secs/60/60}

def is_prime(n):
    if factors(n) == set([1,n]):
        return 1
    else:
        return 0
def primefactors(x):
    primes = []
    for factor in factors(x):
        if is_prime(factor):
            primes.append(factor)

    return primes

def sharedprimefactors(numlist):
    factorlists = []
    primelist = []
    for x in numlist:
        factorlists.append(primefactors(x))

    length = len(numlist)
    for prime in factorlists[0]:
        if prime == 1:
            continue
        shared = 1
        for i in range(0,length):
            if prime not in factorlists[i]:
                shared = 0
        if shared == 1:
            primelist.append(prime)
    return primelist

def beal_combination_search(limits):
    """
    This function takes a tuple of limits for the various a,b,c,z,y,z values.
    if (a^x +b^y)^(1/z) is an int, then there is a solution for c
    """
    [alim,blim,clim,xlim,ylim,zlim] = limits
    validnums = []
    for a in range(1, alim):
        print('Solution space {0}% searched'.format(float(a - 1) / (alim) * 100))
        for b in range(1, blim):
            for x in range(3, xlim):
                for y in range(3, ylim):
                    for z in range(3, zlim):
                        result = Decimal((a**x + b**y)**(1 / Decimal(z)))
                        # Check if the result differs from an integer value by value < EPS (epsilon).
                        if result - int(result) < EPS:
                            validnums.append((a, b, int(result), x, y, z))
    print('Search {0}% complete'.format(int(100)))
    return validnums

def main():
    print('Beal Conjecture verification test')
    validcombs = beal_combination_search(VAR_LIMITS)
    detected_nonprime_solution = 0
    nonprime_solutions = []
    print('(a,b,c,x,y,z) and shared primes list for a,b,c')
    for comb in validcombs:
        sharedprimes = sharedprimefactors(comb[0:2])
        if not sharedprimes: #if prime list is empty
            detected_nonprime_solution = 1
            print('{0} solution has no shared primes: {1}'.format(comb, sharedprimes))
        else:
            print('{0} shared primes: {1}'.format(comb, sharedprimes))

    if detected_nonprime_solution:
        print('Detected nonprime solution for a,b,c!')
    else:
        print('Did not detect a solution where a,b,c have no common prime factors.')

if __name__ == '__main__':
    main()

