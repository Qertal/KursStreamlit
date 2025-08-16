from pathlib import Path
import os
"""
Convert text files between UTF-8 and UTF-16 encodings and log operations.

Rules:
- Read a UTF-8 file and save it as UTF-16.
- Read a UTF-16 file and save it as UTF-8.
- Log each operation

Returns:
    None
"""

os.system(f'flake8 {__file__}')


def convert_utf8_to_utf16(file_name: str):
    if file_name.find('utf8') == 1:
        raise ValueError('Filename must contain phrase "utf8"')

    file_name_utf16 = file_name.replace('utf8', 'utf16')
    base = Path(os.path.dirname(os.path.realpath(__file__)))
    print(f'Opening {file_name} and reading the data...')

    with open(f'{base / file_name}', 'r', encoding='utf-8') as f:
        test = f.read()

    print('Encoding data to utf-16...')

    test_utf16 = test.encode('utf-16')

    print(f'Saving data to {file_name_utf16}...')

    with open(f'{base / file_name_utf16}', 'wb') as f:
        f.write(test_utf16)

    print(f'Reading data from {file_name_utf16}...')

    with open(f'{base / file_name_utf16}', 'r', encoding='utf-16') as f:
        test_utf16_decoded = f.read()

    print('Encoding data to utf-8...')

    test_utf8 = test_utf16_decoded.encode('utf-8')

    print(f'Saving data to {file_name}...')

    with open(f'{base / file_name}', 'wb') as f:
        f.write(test_utf8)

    print('Everything is done!')


file_name = 'item10-12_utf8.txt'

convert_utf8_to_utf16(file_name)
