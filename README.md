# epai3-s7

## Notes/info:


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



### Closures:

**A closure occurs when a function has access to a local variable from an enclosing scope that has finished its execution.**

