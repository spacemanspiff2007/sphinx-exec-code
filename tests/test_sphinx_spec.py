import pytest

from sphinx_exec_code.sphinx_spec import SpecCode, SpecOutput, get_specs


def test_aliases_unique() -> None:
    names_code = set(SpecCode.create_spec())
    names_output = set(SpecOutput.create_spec())

    assert not names_code.intersection(names_output)


def test_spec_code() -> None:
    obj = SpecCode.from_options({'linenos': True, 'caption': 'my_header', 'filename': 'filename'})
    assert obj.hide is False
    assert obj.filename == 'filename'
    assert obj.spec == {'caption': 'my_header', 'linenos': True}


def test_spec_output() -> None:
    obj = SpecOutput.from_options({'hide_output': True, 'caption_output': 'my_header_out'})
    assert obj.hide is True
    assert obj.spec == {'caption': 'my_header_out'}


def test_invalid_options() -> None:
    with pytest.raises(ValueError) as e:    # noqa: PT011
        get_specs({'hide-output': None})

    assert str(e.value) == (
        'Invalid option: hide-output! '
        'Supported: caption, caption_output, class, class_output, dedent, dedent_output, '
        'emphasize-lines, emphasize-lines_output, filename, force, force_output, hide, hide_code, hide_output, '
        'language, language_output, lineno-start, lineno-start_output, linenos, linenos_output, name, name_output'
    )

    with pytest.raises(ValueError) as e:    # noqa: PT011
        get_specs({'hide-output': None, 'language_output': 'asdf', 'caption-output': 'test'})

    assert str(e.value) == (
        'Invalid options: caption-output, hide-output! '
        'Supported: caption, caption_output, class, class_output, dedent, dedent_output, '
        'emphasize-lines, emphasize-lines_output, filename, force, force_output, hide, hide_code, hide_output, '
        'language, language_output, lineno-start, lineno-start_output, linenos, linenos_output, name, name_output'
    )


def test_post_process() -> None:
    assert SpecOutput.from_options({'name': 'asdf'}).spec == {'name': 'asdf_output'}
    assert SpecOutput.from_options({'name_output': 'asdf'}).spec == {'name': 'asdf'}
    assert SpecOutput.from_options({'name': '1', 'name_output': '2'}).spec == {'name': '2'}
