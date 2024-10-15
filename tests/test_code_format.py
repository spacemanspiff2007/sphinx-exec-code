import pytest

from sphinx_exec_code.code_format import VisibilityMarkerError, get_show_exec_code


def test_format_hide() -> None:
    code = 'print("1")\n# - hide: start - \nprint("2")\n #hide:stop\n  \n  \nprint("3")'
    show, run = get_show_exec_code(code.splitlines())
    assert show == 'print("1")\nprint("3")'
    assert run == 'print("1")\nprint("2")\n\n\nprint("3")'


def test_format_skip() -> None:
    code = 'print("1")\n# - skip: start - \nprint("2")\n #skip:stop\nprint("3")'
    show, run = get_show_exec_code(code.splitlines())
    assert show == 'print("1")\nprint("2")\nprint("3")'
    assert run == 'print("1")\nprint("3")'


def test_marker_err() -> None:
    code = 'print("1")\n# - hide: start - \n# - hide: start - \nprint("2")\n #hide:stop\nprint("3")'
    with pytest.raises(VisibilityMarkerError):
        get_show_exec_code(code.splitlines())


def test_code_indent() -> None:
    code = '''

    print('asdf')
        print('1234')
      # comment


    '''
    show, run = get_show_exec_code(code.splitlines())

    assert show == "print('asdf')\n" \
                   "    print('1234')\n" \
                   "  # comment"


def test_code_split_empty() -> None:
    show, run = get_show_exec_code([''])
    assert show == ''
    assert run == ''


def test_code_no_show() -> None:
    code = '# - hide: start -\nprint("l1")\nprint("l2")'
    show, run = get_show_exec_code(code.splitlines())
    assert show == ''
    assert run == 'print("l1")\nprint("l2")'


def test_code_no_exec() -> None:
    code = '# - skip: start -\nprint(1 / 0)\nprint(2 / 0)'
    show, run = get_show_exec_code(code.splitlines())
    assert show == 'print(1 / 0)\nprint(2 / 0)'
    assert run == ''
