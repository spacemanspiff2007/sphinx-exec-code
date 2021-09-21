import pytest

from sphinx_exec_code.code_format import get_show_exec_code, VisibilityMarkerError


def test_format_hide():
    code = 'print("1")\n# - hide: start - \nprint("2")\n #hide:stop\n  \n  \nprint("3")'
    show, run = get_show_exec_code(code.splitlines())
    assert show == 'print("1")\nprint("3")'
    assert run == 'print("1")\nprint("2")\n  \n  \nprint("3")'


def test_format_skip():
    code = 'print("1")\n# - skip: start - \nprint("2")\n #skip:stop\nprint("3")'
    show, run = get_show_exec_code(code.splitlines())
    assert show == 'print("1")\nprint("2")\nprint("3")'
    assert run == 'print("1")\nprint("3")'


def test_marker_err():
    with pytest.raises(VisibilityMarkerError):
        code = 'print("1")\n# - hide: start - \n# - hide: start - \nprint("2")\n #hide:stop\nprint("3")'
        _, _ = get_show_exec_code(code.splitlines())
