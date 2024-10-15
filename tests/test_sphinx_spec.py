from itertools import chain
from typing import Type

import pytest
from docutils.parsers.rst import directives

from sphinx_exec_code.sphinx_spec import SpecCode, SpecOutput, SphinxSpecBase, build_spec, get_specs


def test_aliases_unique() -> None:
    for key_code in SpecCode.aliases:
        assert key_code not in SpecOutput.aliases
    for key_output in SpecOutput.aliases:
        assert key_output not in SpecCode.aliases


@pytest.mark.parametrize('cls', [SpecCode, SpecOutput])
def test_default_in_aliases(cls: Type[SphinxSpecBase]) -> None:
    names = list(cls.aliases.values())
    for k in cls.defaults:
        assert k in names


def test_build_spec_code() -> None:
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


def test_spec_code() -> None:
    obj = SpecCode.from_options({'linenos': None, 'caption': 'my_header', 'filename': 'filename'})
    assert obj.caption == 'my_header'
    assert obj.language == 'python'
    assert obj.linenos is True
    assert obj.hide is False
    assert obj.filename == 'filename'


def test_spec_output() -> None:
    obj = SpecOutput.from_options({'hide_output': None, 'caption_output': 'my_header_out'})
    assert obj.caption == 'my_header_out'
    assert obj.language == 'none'
    assert obj.linenos is False
    assert obj.hide is True


def test_invalid_options() -> None:
    with pytest.raises(ValueError) as e:    # noqa: PT011
        get_specs({'hide-output': None})

    assert str(e.value) == ('Invalid option: hide-output! '
                            'Supported: caption, caption_output, filename, hide_code, hide_output, '
                            'language, language_output, linenos, linenos_output')


    with pytest.raises(ValueError) as e:    # noqa: PT011
        get_specs({'hide-output': None, 'language_output': 'asdf', 'caption-output': 'test'})

    assert str(e.value) == ('Invalid options: caption-output, hide-output! '
                            'Supported: caption, caption_output, filename, hide_code, hide_output, '
                            'language, language_output, linenos, linenos_output')
