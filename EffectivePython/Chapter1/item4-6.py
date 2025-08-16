import random
import os
"""Script to excercise items 4-6 from Effective Python book.
    What the script is doing:
    Write a function that takes a list and returns
    the 3 smallest and 3 largest elements in one line.

    Finally, I check with flake8 to make sure the code is clean..
"""
path = os.path.dirname(os.path.realpath(__file__))
os.system(f'flake8 {path}/item4-6.py')


def unpack_v1(lista: list):

    if not isinstance(lista, list):
        raise TypeError('Argument bust be the list')

    if len(lista) < 6:
        print('List is too short')
        return

    lista.sort()
    first, second, third, *others, third_end, second_end, first_end = lista
    print(f'Three the smallest values are: {first, second, third}')
    print(f'Three the highest values are: {first_end, second_end, third_end}')


def unpack_v2(lista: list):

    if not isinstance(lista, list):
        raise TypeError('Argument bust be the list')

    if len(lista) < 6:
        print('List is too short')
        return

    lista.sort()
    three_smallest = lista[:3]
    three_biggest = lista[:-4:-1]
    print(f'Three the smallest values are: {three_smallest}')
    print(f'Three the highest values are: {three_biggest}')


example_list = [random.randint(1, 1000) for _ in range(20)]
print(example_list)

unpack_v1(example_list)

unpack_v2(example_list)
