import pytest
import s7
import re
import os
import inspect

import math
import random
from collections import defaultdict
import types

CHECK_FOR_FUNCT_IMPL = [
    'add',
    'mul',
    'div',
    'check_doc_len',
    'fibonacci',
    'count_fn_called',
    'check_all_fn_called',
    'count_fn_called_with_dict'
]

README_CONTENT_CHECK_FOR = [
    'namespace',
    'scope',
    'global',
    'local',
    'nonlocal',
    'closure',
    'reduce',
    'lambda'
]


def test_readme_exists():
    """
    checks if README.md exists for the project
    """
    assert os.path.isfile("README.md"), "README.md file missing!"


def test_readme_contents():
    """
    checks if README.md contains at least 500 words
    """
    readme = open("README.md", "r", encoding="utf-8")
    readme_words = readme.read().split()
    readme.close()
    assert len(readme_words) >= 500, "Make your README.md file interesting! Add atleast 500 words"


def test_readme_proper_description():
    """ checks if README.md file has all the mentioned words in the `README_CONTENT_CHECK_FOR` list"""
    READMELOOKSGOOD = True
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in content:
            print(c)
            READMELOOKSGOOD = False
            break

    assert READMELOOKSGOOD is True, "You have not described all the functions/class well in your README.md file"


def test_readme_file_for_formatting():
    """Checks if README.md file has at least 10 `#`s """
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    assert content.count("#") >= 10, "Readme is not formatted properly"


def test_indentations():
    ''' Returns pass if used four spaces for each level of syntactically \
    significant indenting.'''
    lines = inspect.getsource(s7)
    spaces = re.findall('\n +.', lines)
    for space in spaces:
        assert len(space) % 4 == 2, "Your script contains misplaced indentations"
        assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines"


def test_function_name_had_cap_letter():
    """Checks if all the functions in s7.p7 used small letters for function names"""
    functions = inspect.getmembers(s7, inspect.isfunction)
    for function in functions:
        assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"


def test_all_functions_implemented():
    """Checks if each and every function in `CHECK_FOR_FUNCT_IMPL` is present in s7.p7"""
    code_lines = inspect.getsource(s7)
    FUNCS_IMPL = True
    for c in CHECK_FOR_FUNCT_IMPL:
        if c not in code_lines:
            print(c)
            FUNCS_IMPL = False
            break
    assert FUNCS_IMPL is True, 'You forgot to implement all functions! Try again!'


def test_all_docstrings():
    """Checks for doc string in every function in s7.py"""
    functions = inspect.getmembers(s7, inspect.isfunction)
    for func in functions:
        docstring = func[1].__doc__
        assert docstring, "Wooaaahhh !! You have not written docstring for {}".format(func[1].__str__())


def test_check_fn_validity():
    """Checks for error in case function is not passed"""
    with pytest.raises(TypeError, match=r'.*did not pass a function.*'):
        s7.check_doc_len("abc")
        s7.check_doc_len(100)

        def test_doc_len_multi():
            """Checks if the passed function have more than 50 characters in doc string """

            def helper(doc):
                if doc:
                    return True if len(doc) > 50 else False
                else:
                    return 0

            def f():
                pass

            for item in [100, 1.0, "abcd", f, s7.add, s7.mul, s7.div]:
                try:
                    if isinstance(item, types.FunctionType):
                        doc = item.__doc__
                        f = s7.check_doc_len(item)
                        assert f() is helper(doc)
                except Exception as e:
                    assert e.__class__.__name__ == TypeError.__name__


def test_fibonacci():
    """Checks if the number generated randomly is a fibonacci number as per the s7.py file's function"""

    def isPerfectSquare(x):
        s = int(math.sqrt(x))
        return s * s == x

    def isFibonacci(n):
        # n is Fibonacci if one of 5*n*n + 4 or 5*n*n - 4 or both is a perfect square
        return isPerfectSquare(5 * n * n + 4) or isPerfectSquare(5 * n * n - 4)

    for _ in range(10000):
        num = random.randint(0, 1000)
        f = s7.fibonacci()
        for i in range(0, (num // 2) + 1):
            if num in s7.cache.values():
                break
            f()
        assert isFibonacci(num) is (num in s7.cache.values()), "Check your Fibonacci implementation"


def test_add():
    """Checks validity of `add` from s7.py"""
    l = [1, 2, 3, 4]
    assert s7.add(*l) == sum(l)
    assert s7.add(100, 200) == 300
    assert s7.add(1.0, 2.0, 100.0) == 103.0


def test_mul():
    """Checks validity of `mul` from s7.py"""
    l = [1, 2, 3, 4]
    assert s7.mul(*l) == 1 * 2 * 3 * 4
    assert s7.mul(10, 20) == 200
    assert s7.mul(1.0, 2.0, 100.0) == 200.0


def test_div():
    """Checks validity of `div` from s7.py"""
    l = [1, 2, 3, 4]
    assert s7.div(*l) == 1 / 2 / 3 / 4
    assert s7.div(100, 20) == 5
    assert s7.div(100.0, 20) == 5.0
    assert s7.div(100, 20.0) == 5.0


def test_fn_called():
    """Tests for the key and counter value in global dictionary in s7.py through using the functions defined"""
    l = [1, 2, 3, 4, 5]
    for fn in [s7.div, s7.mul, s7.add, "abcd", 1234]:
        try:
            f = s7.count_fn_called(fn=fn)
            for i in range(0, random.randint(2, 10)):
                f(*l)
            assert fn in s7.fn_called_dict.keys() and str(s7.fn_called_dict[fn]) in s7.check_all_fn_called(fn)
        except Exception as e:
            assert e.__class__.__name__ == TypeError.__name__


def test_fn_call_with_dict():
    """Tests if the function works properly for passing dictionary and function"""
    l = [1, 2, 3, 4, 5]
    ds = [defaultdict(int), defaultdict(int), defaultdict(int)]
    for d in ds:
        for fn in [s7.div, s7.mul, s7.add, "abcd", 1234]:
            try:
                f = s7.count_fn_called_with_dict(dict_=d, fn=fn)
                for i in range(0, random.randint(2, 10)):
                    f(*l)
                assert fn in d.keys() and d[fn] == (i + 1)
            except Exception as e:
                assert e.__class__.__name__ == TypeError.__name__
