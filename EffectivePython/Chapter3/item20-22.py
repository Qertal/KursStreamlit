import os

"""
Task:
- Write a loop and show that the loop variable
is still accessible after the loop ends.
- Refactor to avoid leaking loop variables outside their intended scope.
- Implement `find_first_even(nums)`:
  * Version 1: use a for/else block to return the first even number or None.
  * Version 2: use early return instead of else.
- Show why modifying a list inside a for loop is unsafe.
- Provide safer alternatives:
  * Iterate over a copy.
  * Build a new list with only the desired elements.
"""

os.system(f'flake8 {__file__}')

num = 60  # I like this number and want to remember it
print(f'{num=} before first loop')
numbers = [i for i in range(1, 5)]
for num in numbers:
    if num == numbers[-1]:
        print(f'This is step number {num}')

print(f'{num=} after first loop\n')  # oopsie?

# It can be dangerous because the loop variable
# remains accessible after the loop,
# which may unintentionally overwrite
# existing variables and cause subtle bugs.

num = 60  # I like this number and want to remember it
print(f'{num=} before second loop')


def loop_helper(numbers):
    numbers = [i for i in range(1, 5)]
    for num in numbers:
        if num == numbers[-1]:
            print(f'This is step number {num}')


loop_helper(numbers)
print(f'{num=} after second loop\n')


def find_first_even_v1(nums):
    evens = []
    for i in nums:
        if i % 2 == 0:
            evens.append(i)
    else:
        return evens[0]


def find_first_even_v2(nums):
    for i in nums:
        if i % 2 == 0:
            return i
    return None


x = find_first_even_v1([1, 3, 7, 8, 11])
y = find_first_even_v2([1, 3, 7, 8, 11])
print(x, y, '\n')

my_list = [1, 2, 3, 5]
my_list_copy = list(my_list)

for i in my_list_copy:
    if i % 2 != 0:
        my_list_copy.remove(i)
print(my_list_copy, '\n')

my_list_copy = list(my_list)
for i in my_list_copy[:]:  # copying by slicing
    if i % 2 != 0:
        my_list_copy.remove(i)
print(my_list_copy, '\n')

my_list_copy = list(my_list)
even_nums = [i for i in my_list_copy if i % 2 == 0]  # pythontic style
print(even_nums)
