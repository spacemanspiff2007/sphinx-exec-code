import typing
from pathlib import Path

from setuptools import find_packages, setup


def load_version() -> str:
    version: typing.Dict[str, str] = {}
    with open("src/sphinx_exec_code/__version__.py") as fp:
        exec(fp.read(), version)
    assert version['__version__'], version
    return version['__version__']


__version__ = load_version()

print(f'Version: {__version__}')
print('')

# When we run tox tests we don't have these files available so we skip them
readme = Path(__file__).with_name('readme.md')
long_description = ''
if readme.is_file():
    with readme.open("r", encoding='utf-8') as fh:
        long_description = fh.read()

setup(
    name="sphinx-exec-code",
    version=__version__,
    author="spaceman_spiff",
    # author_email="",
    description="Execute code blocks in Sphinx and display the output",
    keywords=[
        'sphinx',
        'execute',
        'exec',
        'code'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spacemanspiff2007/sphinx-exec-code",
    project_urls={
        'GitHub': 'https://github.com/spacemanspiff2007/sphinx-exec-code',
        'Documentation': 'https://sphinx-exec-code.readthedocs.io/',
    },
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['tests*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        'Intended Audience :: Developers',
        'Framework :: Sphinx :: Extension',
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
