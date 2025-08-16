from platform import python_version
import pkgutil
import os

""" Prosty skrypt do przećwiczenia rzeczy związanych
    z item 1-3 z ksiązki effective books, konkretne zadania:
    Wypisz wersję Pythona i wszystkie moduły standardowe w tej wersji.
    Przeskanuj własny plik .py narzędziem flake8
    lub ruff i wypisz wszystkie ostrzeżenia.
    Znajdź przykład błędu, który wystąpi dopiero w runtime..
"""

version = python_version()
modules = [p for p in pkgutil.iter_modules()]
print(f'Version of python: {version}')
path = os.path.dirname(os.path.realpath(__file__))
os.system(f'flake8 {path}/item1-3.py')


def func(x):  # dwie linie przerwy przed

    if y > 10:
        print(test)  # dwie linie przerwy po


func(5)
