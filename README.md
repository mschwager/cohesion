# Cohesion

[![Build Status](https://travis-ci.org/mschwager/cohesion.svg?branch=master)](https://travis-ci.org/mschwager/cohesion)
[![Coverage Status](https://coveralls.io/repos/github/mschwager/cohesion/badge.svg?branch=master)](https://coveralls.io/github/mschwager/cohesion?branch=master)

Cohesion is a tool for measuring Python class cohesion.

> In computer programming, cohesion refers to the degree to which the elements
> of a module belong together. Thus, cohesion measures the strength of
> relationship between pieces of functionality within a given module. For
> example, in highly cohesive systems functionality is strongly related.
> - [Wikipedia](https://en.wikipedia.org/wiki/Cohesion_(computer_science))

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
$ pip3 install cohesion
$ cohesion -h
```

OR

```
$ git clone https://github.com/mschwager/cohesion.git
$ cd cohesion
$ python3 lib/cohesion/main.py -h
```

# Using

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
  Class: ExampleClass1
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
  Class: ExampleClass2
    Function: func1 1/1 100.00%
      Variable: instance_variable1 True
    Total: 100.00%
```

# Developing

First, install development packages:

```
$ pip3 install -r requirements-dev.txt
```

## Testing

```
$ nosetests
.....................
----------------------------------------------------------------------
Ran 21 tests in 0.006s

OK
```

## Linting

```
$ flake8
```

## Coverage

```
$ nosetests --with-coverage
```
