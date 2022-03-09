from itertools import chain
from typing import Type

import pytest
from docutils.parsers.rst import directives

from sphinx_exec_code.sphinx_spec import build_spec, SpecCode, SpecOutput, SphinxSpecBase


def test_aliases_unique():
    for key_code in SpecCode.aliases:
        assert key_code not in SpecOutput.aliases
    for key_output in SpecOutput.aliases:
        assert key_output not in SpecCode.aliases


@pytest.mark.parametrize('cls', (SpecCode, SpecOutput))
def test_default_in_aliases(cls: Type[SphinxSpecBase]):
    names = list(cls.aliases.values())
    for k in cls.defaults:
        assert k in names


def test_build_spec_code():
    spec = build_spec()

    for name in chain(SpecCode.aliases.keys(), SpecOutput.aliases.keys()):
        assert name in spec

    assert spec == {
        'hide_code': directives.flag,
        'linenos': directives.flag,
        'caption': directives.unchanged,
        'language': directives.unchanged,
        'filename': directives.unchanged,

        'hide_output': directives.flag,
        'linenos_output': directives.flag,
        'caption_output': directives.unchanged,
        'language_output': directives.unchanged,
    }


def test_spec_code():
    obj = SpecCode.from_options({'linenos': None, 'caption': 'my_header'})
    assert obj.caption == 'my_header'
    assert obj.language == 'python'
    assert obj.linenos is True
    assert obj.hide is False
    assert obj.filename == ''


def test_spec_output():
    obj = SpecOutput.from_options({'hide_output': None, 'caption_output': 'my_header_out'})
    assert obj.caption == 'my_header_out'
    assert obj.language == 'none'
    assert obj.linenos is False
    assert obj.hide is True
