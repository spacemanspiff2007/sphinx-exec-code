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
#### 0.15 (2024-12-10)
- Removed confusing log output

#### 0.14 (2024-11-15)
- Add support for all options from code block
- Reworked how blocks and options are processed

#### 0.13 (2024-10-15)
- Add support for python 3.13

#### 0.12 (2024-01-09)
- Error when providing invalid options

#### 0.11 (2024-01-09)
- Updated CI and ruff fixes

#### 0.10 (2023-02-13)
- Fixed a bug when no code was shown/executed

#### 0.9 (2023-02-08)
- If the whole shown code block is indented the indention is removed

#### 0.8 (2022-07-18)
- Renamed ``exec_code_folders`` to ``exec_code_source_folders``
- Changed type of parameter to specify stdout to a flag
- Changed default for config parameter that sets encoding
- Dropped support for Python 3.7

#### 0.7 (2022-07-15)
- Added config parameter to specify stdout encoding
- Only empty lines of the output get trimmed

#### 0.6 (2022-04-04)
- Fixed an issue where the line numbers for error messages were not correct

#### 0.5 (2022-03-10)
- Marked as safe for parallel reading

#### 0.4 (2022-03-09)
- Added option to run code from example files

#### 0.3 (2021-09-24)
- Added some more documentation and fixed some false path warnings

#### 0.2 (2021-09-21)
- Initial Release
