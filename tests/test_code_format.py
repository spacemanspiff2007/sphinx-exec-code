import pytest

from sphinx_exec_code.code_format import get_show_exec_code, VisibilityMarkerError


def test_format_hide():
    code = 'print("1")\n# - hide: start - \nprint("2")\n #hide:stop\nprint("3")'
    show, run = get_show_exec_code(code.splitlines())
    assert show == 'print("1")\nprint("3")'


def test_marker_err():
    with pytest.raises(VisibilityMarkerError):
        code = 'print("1")\n# - hide: start - \n# - hide: start - \nprint("2")\n #hide:stop\nprint("3")'
        _, _ = get_show_exec_code(code.splitlines())
