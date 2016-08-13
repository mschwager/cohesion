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
$ python3 lib/cohesion/__main__.py -h
```

# Using

TODO

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
