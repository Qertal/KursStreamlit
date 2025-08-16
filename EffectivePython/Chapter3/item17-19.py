from pathlib import Path
from itertools import zip_longest
import os

os.system(f'flake8 {__file__}')

"""
Task:
- Read two text files and compare them line by line.
- Allow an option (`ignore_whitespace`) to remove all spaces before comparison.
- Use `itertools.zip_longest` to detect differences, including extra
trailing lines in either file.
- Number lines starting from 1 and format the label as "Row number X".
- For empty lines, output a message:
  '*There is empty row in file <filename>*'.
- Collect differences as tuples: (row_label, line_from_file_a,
line_from_file_b).
- Stop collecting when the specified `limit` of differences is reached.
- Return the collected differences.
"""


def file_differences(file_name_a: str, file_name_b: str,
                     ignore_whitespace: bool, limit: int):

    base = Path(os.path.dirname(os.path.realpath(__file__)))
    path_a = base / file_name_a
    path_b = base / file_name_b

    if ignore_whitespace:
        with open(path_a, 'r') as f:
            list_a = f.read().replace(' ', '').split('\n')

        with open(path_b, 'r') as f:
            list_b = f.read().replace(' ', '').split('\n')

    else:
        with open(path_a, 'r') as f:
            list_a = f.read().split('\n')

        with open(path_b, 'r') as f:
            list_b = f.read().split('\n')

    differences = []

    for row, (a, b) in enumerate(zip_longest(list_a, list_b), 1):
        if a != b:
            if a == '':
                # print(f'Row number {row}:
                # *There is empty row in file {file_name_a}* =/=', b)
                differences.append((f"Row number {row}",
                                    '*There is empty row'
                                    + f'in file {file_name_a}*',
                                    b))
            elif b == '':
                # print(f'Row number {row}: ',
                # a, f'=/= *There is empty row in file {file_name_b}*')
                differences.append((f"Row number {row}",
                                    a,
                                    '*There is empty row'
                                    + f'in file {file_name_b}*'))
            else:
                differences.append((f'Row number {row}',
                                    a,
                                    b))
                # print(f'Row number {row}: ', a, '=/=' , b)

        if len(differences) >= limit:
            return differences


diff = file_differences('file_a.txt', 'file_b.txt', True, 12)

for row, line_a, line_b in diff:
    print(f'{row}:', line_a, '=/=', line_b)
