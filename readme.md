# sphinx-exec-code
![Tests Status](https://github.com/spacemanspiff2007/sphinx-exec-code/workflows/Tests/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/sphinx-exec-code/badge/?version=latest)](https://sphinx-exec-code.readthedocs.io/en/latest/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sphinx-exec-code)
![PyPI](https://img.shields.io/pypi/v/sphinx-exec-code)
[![Downloads](https://pepy.tech/badge/sphinx-exec-code/month)](https://pepy.tech/project/sphinx-exec-code)

_A Sphinx extension to run python code in the documentation_

## About
Sphinx-exec-code allows execution of any python code during the documentation build.
It's also possible to display the output of the code execution.

With this extension it's easy to ensure that the provided code samples are always working.
Additionally, it's possible to show the output of the documented code.

Each code snippet runs in a fresh interpreter so changes to not leak between executions.

## Documentation
[The full documentation can be found at here](https://sphinx-exec-code.readthedocs.io)


## Quick Example

````text
.. exec-code::

   print('This code will be executed')
````
generates
```python
print('This code will be executed')
```
```
This code will be executed
```

# Changelog
#### 0.7 (15.07.2022)
- Added config parameter to specify stdout encoding
- Only empty lines of the output get trimmed 

#### 0.6 (04.04.2022)
- Fixed an issue where the line numbers for error messages were not correct

#### 0.5 (10.03.2022)
- Marked as safe for parallel reading

#### 0.4 (09.03.2022)
- Added option to run code from example files

#### 0.3 (24.09.2021)
- Added some more documentation and fixed some false path warnings

#### 0.2 (21.09.2021)
- Initial Release
