# EPAi3 S7

## Scopes:

The concept of **scope** rules how variables and names are looked up in your code. It determines the visibility of a variable within the code.

The Python scope concept is generally presented using a rule known as the **LEGB rule**. The letters in the acronym LEGB stand for **Local, Enclosing, Global, and Built-in** scopes. This summarizes not only the Python scope levels but also the sequence of steps that Python follows when resolving names in a program. 



### Understanding Scope: [src](https://realpython.com/python-scope-legb-rule/)

In programming, the **scope** of a name defines the area of a program in which you can unambiguously access that name, such as variables, functions, objects, and so on. A name will only be visible to and accessible by the code in its scope. Several programming languages take advantage of scope for avoiding name collisions and unpredictable behaviors. Most commonly, you’ll distinguish two general scopes:

1. **Global scope:** The names that you define in this scope are available to all your code.
2. **Local scope:** The names that you define in this scope are only available or visible to the code within the scope.

#### Python Scope vs Namespace

In Python, the concept of scope is closely related to the concept of the namespace. A Python scope determines where in your program a name is visible. Python scopes are implemented as dictionaries that map names to objects. These dictionaries are commonly called **namespaces**. These are the concrete mechanisms that Python uses to store names. They’re stored in a special attribute called `.__dict__`



As a quick summary, some of the implications of Python scope are shown in the following table:

| Action                                                       | Global Code | Local Code                                        | Nested Function Code                              |
| ------------------------------------------------------------ | ----------- | ------------------------------------------------- | ------------------------------------------------- |
| Access or reference names that live in the global scope      | Yes         | Yes                                               | Yes                                               |
| Modify or update names that live in the global scope         | Yes         | No (unless declared `global`)                     | No (unless declared `global`)                     |
| Access or reference names that live in a local scope         | No          | Yes (its own local scope), No (other local scope) | Yes (its own local scope), No (other local scope) |
| Override names in the built-in scope                         | Yes         | Yes (during function execution)                   | Yes (during function execution)                   |
| Access or reference names that live in their enclosing scope | N/A         | N/A                                               | Yes                                               |
| Modify or update names that live in their enclosing scope    | N/A         | N/A                                               | No (unless declared `nonlocal`)                   |



Python provides two keywords that allow you to modify the content of global and nonlocal names. These two keywords are:

1. **`global`**
2. **`nonlocal`**



```python
>>> counter = 0  # A global name
>>> def update_counter():
...     counter = counter + 1  # Fail trying to update counter
...
>>> update_counter()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 2, in update_counter
UnboundLocalError: local variable 'counter' referenced before assignment
```

```python
>>> counter = 0  # A global name
>>> def update_counter():
...     global counter  # Declare counter as global
...     counter = counter + 1  # Successfully update the counter
...
>>> update_counter()
>>> counter
1
>>> update_counter()
>>> counter
2
```

**Note:** The use of `global` is considered bad practice in general, like above. 

For example, you can try to write a self-contained function that relies on local names rather than on global names as follows:

```python
>>> global_counter = 0  # A global name
>>> def update_counter(counter):
...     return counter + 1  # Rely on a local name
...
>>> global_counter = update_counter(global_counter)
>>> global_counter
1
```



You can also use a `global` statement to create lazy global names by declaring them inside a function.

```python
>>> def create_lazy_name():
...     global lazy  # Create a global name, lazy
...     lazy = 100
...     return lazy
...
>>> create_lazy_name()
100
>>> lazy  # The name is now available in the global scope
100
>>> dir()
['__annotations__', '__builtins__',..., 'create_lazy_name', 'lazy']
```



### The `nonlocal` Statement:

nonlocal names can be accessed from inner functions, but not assigned or updated. If you want to modify them, then you need to use a **`nonlocal`statement**.

```python
>>> def func():
...     var = 100  # A nonlocal variable
...     def nested():
...         nonlocal var  # Declare var as nonlocal
...         var += 100
...
...     nested()
...     print(var)
...
>>> func()
200
```



**You can’t use a `nonlocal` statement in either the global scope or in a local scope.**

```python
>>> nonlocal my_var  # Try to use nonlocal in the global scope
  File "<stdin>", line 1
SyntaxError: nonlocal declaration not allowed at module level
>>> def func():
...     nonlocal var  # Try to use nonlocal in a local scope
...     print(var)
...
  File "<stdin>", line 2
SyntaxError: no binding for nonlocal 'var' found
```

 

## Closures:

**A closure occurs when a function has access to a local variable from an enclosing scope that has finished its execution.**

By definition, a closure is a nested function that references one or more variables from its enclosing scope.

In Python, a function can return a value which is another function. For example:

 

```python
def say():
    greeting = 'Hello'
    def display():
        print(greeting)

    return display    
```

In this example, the say function returns the display function instead of executing it.

Also, when the say function returns the display function, it actually returns the **closure**.



```python
fn = say()
fn()
```

Output:

```
Hello
```

The `say` function executes and returns a function. When the `fn` function executes, the `say`function already completes.

In other words, the scope of the `say` function was gone at the time the `fn` function executes.

Since the `greeting` variable belongs to the scope of the `say` function, it should also be destroyed with the scope of the function.

However, you still see that `fn` displays the value of the `message` variable.



The label `greeting` is in two different scopes. However, they always reference the same string object with the value `'Hello'`.

**To achieve this, Python creates an intermediary object called a `cell`:**



![](https://www.pythontutorial.net/wp-content/uploads/2020/11/Python-Closures-and-Cells.png)



**Example:**

```python
>>> def outer():
...    var = 100
...    def inner():
...        print(var)
...    return inner

>>> f = outer()

>>> f()
100

>>> f.__closure__
(<cell at 0x7fbdc7869b20: int object at 0x1099075c0>,)
```



**Now to check the value at above address the cell is pointing to: use `ctypes`**

```python
>>> import ctypes
>>> ctypes.cast(0x1099075c0, ctypes.py_object).value
100

```

To find the free variables that a closure contains:

```python
>>> f.__code__.co_freevars
('var',)
```



## Notes:


### Leaking the loop control:

<u>For Python 3.x:</u>

>
>
>\>>> x = 'before'
>
>\>>> a = [x for x in range(4)]
>
>\>>> x
>
>'before'
>
>\>>> a
>
>[0, 1, 2, 3]
>
>\>>> for a in range(10):
>
>...        pass
>
>\>>> a
>
>9
>
>\>>>

## Task content overview:
    def add(*args):
    """Adds the numbers passed as argument and returns the sum using in-built `sum`"""

----------

    def mul(*args):
    """Multiplies the numbers passed as argument and returns the final value"""

-------------

    def div(*args):
    """Divides the numbers passed as argument and returns the final value"""

---------------

    def check_doc_len(fn):
    """
    Checks if the passed function has at least 50 characters in the doc string.
    
    :param fn: the function to check for doc string length
    ----------

    :return: closure for `check_docstring` inner func with free variable `limit`
    """

-------------

    def fibonacci():
    """
    A function returning a `closure` func to get next valid fibonacci number.
    As a closure is returned, different closures created for `fibonacci` will be independent and start from 0/
    :return: a closure that returns the next valid fibonacci number
    """

-------------

    def count_fn_called(fn):
    """
    Counts and increments the number of times the passed function has been called, uses global dictionary and returns closure for called function.
    :param fn: the function's closure to be returned after incrementing the count
    :return: `check` closure
    """


-------------

    def check_all_fn_called(fn):
    """
    Prints the number of times the passed function was called using global dictionary `fn_global_dict`
    :return: formatted string
    """

----------

    def count_fn_called_with_dict(*, dict_, fn):
    """
    Maintains the called count for each function passed into the dictionary passed.
    :param dict_: the dictionary to maintain the called count for `fn`
    :param fn: the function to return with *args and **kwargs from closure
    :return: a closure that returns the `fn` after incrementing called count by 1
    """


---------

**Important constructs/concepts used in this repo:**
> [
    'namespace',
    'scope',
    'global',
    'local',
    'nonlocal',
    'closure',
    'reduce',
    'lambda'
]


**NOTE:** **List comprehensions leak the loop control variable in Python 2 but NOT in Python 3.**


Here's Guido van Rossum [explaining](http://python-history.blogspot.com/2010/06/from-list-comprehensions-to-generator.html) the history behind this:

> We also made another change in Python 3, to improve equivalence between list comprehensions and generator expressions. In Python 2, the list comprehension "leaks" the loop control variable into the surrounding scope:
>
> ```py
> x = 'before'
> a = [x for x in 1, 2, 3]
> print x # this prints '3', not 'before'
> ```
>
> This was an artifact of the original implementation of list comprehensions; it was one of Python's "dirty little secrets" for years. It started out as an intentional compromise to make list comprehensions blindingly fast, and while it was not a common pitfall for beginners, it definitely stung people occasionally. For generator expressions we could not do this. Generator expressions are implemented using generators, whose execution requires a separate execution frame. Thus, generator expressions (especially if they iterate over a short sequence) were less efficient than list comprehensions.
>
> However, in Python 3, we decided to fix the "dirty little secret" of list comprehensions by using the same implementation strategy as for generator expressions. Thus, in Python 3, the above example (after modification to use print(x) :-) will print 'before', proving that the 'x' in the list comprehension temporarily shadows but does not override the 'x' in the surrounding scope.



-----------


### Generators:

Instead of storing the entire range, `[0,1,2,..,9]`, in memory, the generator stores a definition for `(i=0; i<10; i+=1)` and computes the next value only when needed (AKA lazy-evaluation).

Essentially, a generator allows you to return a list like structure, but here are some differences:

1. A list stores all elements when it is created. A generator generates the next element when it is needed.
2. A list can be iterated over as much as you need, a generator can only be iterated over *exactly* once.
3. A list can get elements by index, a generator cannot -- it only generates values once, from start to end.


----------

### nonlocal:

> **>>>help("nonlocal")**
>
> The "nonlocal" statement
>
> ************************
>
> 
>
>   nonlocal_stmt ::= "nonlocal" identifier ("," identifier)*
>
> 
>
> The "nonlocal" statement causes the listed identifiers to refer to
>
> previously bound variables in the nearest enclosing scope excluding
>
> globals. This is important because the default behavior for binding is
>
> to search the local namespace first. The statement allows
>
> encapsulated code to rebind variables outside of the local scope
>
> besides the global (module) scope.
>
> 
>
> Names listed in a "nonlocal" statement, unlike those listed in a
>
> "global" statement, must refer to pre-existing bindings in an
>
> enclosing scope (the scope in which a new binding should be created
>
> cannot be determined unambiguously).
>
> 
>
> Names listed in a "nonlocal" statement must not collide with pre-
>
> existing bindings in the local scope.
>
> 
>
> See also:
>
> 
>
>  **PEP 3104** - Access to Names in Outer Scopes
>
>    The specification for the "nonlocal" statement.
>
> 
>
> Related help topics: global, NAMESPACES



```python
x = 0
def outer():
    x = 1
    def inner():
        x = 2
        print("inner:", x)

    inner()
    print("outer:", x)

outer()
print("global:", x)

# inner: 2
# outer: 1
# global: 0
```



```python
x = 0
def outer():
    x = 1
    def inner():
        nonlocal x
        x = 2
        print("inner:", x)

    inner()
    print("outer:", x)

outer()
print("global:", x)

# inner: 2
# outer: 2
# global: 0
```
