import types
from functools import reduce
from collections import defaultdict

cache = {0: 0, 1: 1}
fn_called_dict = defaultdict(int)


def add(*args):
    """Adds the numbers passed as argument and returns the sum using in-built `sum`"""
    return sum(args)


def mul(*args):
    """Multiplies the numbers passed as argument and returns the final value"""
    return float(reduce(lambda x, y: x * y, args))


def div(*args):
    """Divides the numbers passed as argument and returns the final value"""
    return float(reduce(lambda x, y: x / y, args))


def check_doc_len(fn):
    """
    Checks if the passed function has at least 50 characters in the doc string.
    :param fn: the function to check for doc string length
    ----------
    :return: closure for `check_docstring` inner func with free variable `limit`
    """
    if not isinstance(fn, types.FunctionType):
        raise TypeError("\n You did not pass a function.")
    if fn.__doc__:
        l = len(fn.__doc__)
        limit = 50

        def check_docstring():
            """
                Returns True or False on number of characters being > 50 or not respectively.
                :return: bool
                """
            if l > limit:
                print("The passed function has more than 50 characters in doc string")
                return True
            else:
                print("The passed function does not have more than 50 characters in doc string")
                return False

        return check_docstring
    else:
        raise NotImplementedError("\n 😑 No doc string available.")


def fibonacci():
    """
    A function returning a `closure` func to get next valid fibonacci number.
    As a closure is returned, different closures created for `fibonacci` will be independent and start from 0/
    :return: a closure that returns the next valid fibonacci number
    """
    n = 0

    def get_fib_num():
        """
        uses free variable `n` and global `cache` for returning the next valid fibonacci number
        :return: next valid fibonacci number
        """
        global cache
        nonlocal n
        if n not in cache.keys():
            cache[n] = cache[n - 1] + cache[n - 2]
            n = n + 1
            return cache[n - 1]
        n = n + 1
        return cache[n - 1]

    return get_fib_num


def count_fn_called(fn):
    """
    Counts and increments the number of times the passed function has been called, uses global dictionary and returns closure for called function.
    param fn: the function's closure to be returned after incrementing the count
    return: `check` closure
    """
    if not isinstance(fn, types.FunctionType):
        raise TypeError("\n Please pass a function type.")

    def check(*args, **kwargs):
        """
        Increments the `fn` called count by 1 and returns `fn` with *args and **kwargs
        """
        global fn_called_dict
        fn_called_dict[fn] += 1
        return fn(*args, **kwargs)

    return check


def check_all_fn_called(fn):
    """
    Prints the number of times the passed function was called using global dictionary `fn_global_dict`
    return: formatted string
    """
    global fn_called_dict
    return "Function: {0} called: {1} times".format(fn, fn_called_dict.get(fn, 0))


def count_fn_called_with_dict(*, dict_, fn):
    """
    Maintains the called count for each function passed into the dictionary passed.
    :param dict_: the dictionary to maintain the called count for `fn`
    :param fn: the function to return with *args and **kwargs from closure
    :return: a closure that returns the `fn` after incrementing called count by 1
    """
    if not (isinstance(dict_, dict) and isinstance(fn, types.FunctionType)):
        raise TypeError("\n You should pass dict and function types only.")

    def check(*args, **kwargs):
        """
        uses the nonlocal `dict_` and `fn` to maintain the `fn` called count
        :return: function with arguments and key word arguments
        """
        nonlocal dict_
        dict_[fn] += 1
        print(f"\nFunction {fn} called {dict_[fn]} times")
        return fn(*args, **kwargs)

    return check
