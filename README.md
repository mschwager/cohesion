# Cohesion

[![Python Versions](https://img.shields.io/pypi/pyversions/cohesion.svg)](https://img.shields.io/pypi/pyversions/cohesion.svg)
[![PyPI Version](https://img.shields.io/pypi/v/cohesion.svg)](https://img.shields.io/pypi/v/cohesion.svg)

Cohesion is a tool for measuring Python class cohesion.

> In computer programming, cohesion refers to the degree to which the elements
> of a module belong together. Thus, cohesion measures the strength of
> relationship between pieces of functionality within a given module. For
> example, in highly cohesive systems functionality is strongly related.
> - [Wikipedia](https://en.wikipedia.org/wiki/Cohesion_(computer_science))

> When cohesion is high, it means that the methods and variables of the class
> are co-dependent and hang together as a logical whole.
> - Clean Code pg. 140

Some of the advantages of high cohesion, also by Wikipedia:

* Reduced module complexity (they are simpler, having fewer operations).
* Increased system maintainability, because logical changes in the domain
  affect fewer modules, and because changes in one module require fewer
  changes in other modules.
* Increased module reusability, because application developers will find
  the component they need more easily among the cohesive set of operations
  provided by the module.

# Installing

```
$ python -m pip install cohesion
$ cohesion -h
```

# Using

Cohesion measures class and instance variable usage across the methods
of that class.

```
$ cat example.py
class ExampleClass1(object):
    class_variable1 = 5
    class_variable2 = 6

    def func1(self):
        self.instance_variable = 6

        def inner_func(b):
            return b + 5

        local_variable = self.class_variable1

        return local_variable

    def func2(self):
        print(self.class_variable2)

    @staticmethod
    def func3(variable):
        return variable + 7

class ExampleClass2(object):
    def func1(self):
        self.instance_variable1 = 7
```

```
$ cohesion --files example.py --verbose
File: example.py
  Class: ExampleClass1 (1:0)
    Function: func1 2/3 66.67%
      Variable: class_variable1 True
      Variable: class_variable2 False
      Variable: instance_variable True
    Function: func2 1/3 33.33%
      Variable: class_variable1 False
      Variable: class_variable2 True
      Variable: instance_variable False
    Function: func3 0/3 0.00%
      Variable: class_variable1 False
      Variable: class_variable2 False
      Variable: instance_variable False
    Total: 33.33%
  Class: ExampleClass2 (23:0)
    Function: func1 1/1 100.00%
      Variable: instance_variable1 True
    Total: 100.00%
```

The `--below` and `--above` flags can be specified to only show classes with
a cohesion value below or above the specified percentage, respectively.

## Flake8 Support

Cohesion supports being run by `flake8`. First, ensure your installation has
registered `cohesion`:

```
$ flake8 --version
3.2.1 (pyflakes: 1.0.0, cohesion: 1.2.0, pycodestyle: 2.2.0, mccabe: 0.5.3) CPython 2.7.12 on Linux
```

And now use `flake8` to lint your file:

```
$ flake8 example.py
example.py:1:1: H601 class has low cohesion
```

# Developing

First, install development packages:

```
$ python -m poetry install --with=dev
```

## Testing

```
$ python -m poetry run pytest
```

## Linting

```
$ python -m poetry run flake8
```

## Coverage

```
$ python -m poetry run pytest --cov
```
