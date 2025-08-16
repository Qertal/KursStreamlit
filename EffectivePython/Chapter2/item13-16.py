from timeit import default_timer as timer
import os
from pathlib import Path

os.system(f'flake8 {__file__}')

"""
Work with string slicing, concatenation methods, and unpacking.

Tasks:
- Return every third character from the end of a string without loops.
- Compare performance of concatenation using '+', ''.join(),
and f-strings on large datasets.
- Apply sequence unpacking to simplify slicing where possible.

"""


def stoper(start: float, end: float):
    total_time = end - start
    return total_time


def check_text(text):
    if isinstance(text, str):
        text = list(text)
    elif isinstance(text, list):
        pass
    else:
        raise TypeError('Check the input data')


def plus_concat(text):
    check_text(text)

    result = ''
    start = timer()
    for i in text:
        result += i
    end = timer()
    total_time = stoper(start, end)

    print(f'Concatenating with "+" last {total_time:.2f} seconds')


def join_concat(text):
    check_text(text)

    start = timer()

    ''.join(text)

    end = timer()
    total_time = stoper(start, end)

    print(f'Concatenating with "join" last {total_time:.2f} seconds')


def concat_fstring(text):
    check_text(text)

    start = timer()
    result = ''
    for i in text:
        result = f'{result}{i}'

    end = timer()
    total_time = stoper(start, end)
    print(f'Concatenating with "fstring" last {total_time:.2f} seconds')


base = Path(os.path.dirname(os.path.realpath(__file__)))
file_name = 'text.txt'

total_path = base / file_name

with open(total_path, 'r') as f:
    content = f.read()

content_list = list(content)

plus_concat(content_list)
join_concat(content_list)
# concat_fstring(content_list) no effective
