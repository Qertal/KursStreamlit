import numpy as np
import math
from itertools import combinations, combinations_with_replacement
import os

os.system(f'flake8 {__file__}')
"""
Task:
- Implement `is_all_even(nums)` using `all()` to check if all numbers are even.
- Implement `has_prime(nums)` using `any()` to check if the list contains a prime number.
- Use `itertools.combinations` to generate triples of numbers:
  * Use `any()` to check if there exists a triple summing to 15.
  * Use `all()` to check if every triple contains at least one even number.
"""


def is_prime(n):
    if n == 1:
        return False

    arange = np.arange(2, math.ceil(n**(1/2))+1, 1)
    return not any((z == int(z)) for z in n/arange)


def has_primes(nums):
    return any(is_prime(n) for n in nums)


def check_atleast_one_even(nums):
    return any(n % 2 == 0 for n in nums)


print('Is there any primes?', has_primes([1, 4, 6, 16, 23]))

it = combinations([i for i in range(10)], 3)
comb = list(it)

it = combinations_with_replacement([i for i in range(10)], 3)
comb_w_r = list(it)

print('Is there any number devided by 15?',
      any(sum(i) % 15 == 0 for i in comb))

print('Is there any number devided by 15?',
      any(sum(i) % 15 == 0 for i in comb_w_r))

print('Is every package has a number which is even?',
      all(check_atleast_one_even(i) for i in comb))

print('Is every package has a number which is even?',
      all(check_atleast_one_even(i) for i in comb_w_r))
