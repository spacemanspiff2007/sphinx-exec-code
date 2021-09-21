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
Additionally, it's possible to inspect and print output of the documented code.

## Documentation
[The full documentation can be found at here](https://sphinx-exec-code.readthedocs.io)


## Quick Example

````text
.. exec-code::
   :hide_output:

   print('This code will be executed')

   1/0  # <-- This will cause an error during the doc build
````


# Changelog
#### 0.1 (21.09.2021)
- Initial Release
