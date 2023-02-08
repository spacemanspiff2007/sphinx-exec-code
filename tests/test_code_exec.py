import os
from pathlib import Path

import pytest

from sphinx_exec_code.code_exec import CodeExceptionError, execute_code
from sphinx_exec_code.configuration import PYTHONPATH_FOLDERS, SET_UTF8_ENCODING, WORKING_DIR


@pytest.fixture()
def setup_env(monkeypatch):
    f = Path(__file__).parent
    monkeypatch.setattr(WORKING_DIR, '_value', f)
    monkeypatch.setattr(PYTHONPATH_FOLDERS, '_value', [str(f)])
    return None


@pytest.mark.parametrize('utf8', [True, False])
def test_print(setup_env, monkeypatch, utf8):
    monkeypatch.setattr(SET_UTF8_ENCODING, '_value', utf8)

    code = "print('Line1')\nprint('Line2')"
    output = execute_code(code, 'my_file', 1)
    assert output == 'Line1\nLine2'


@pytest.mark.parametrize('utf8', [True, False])
def test_print_table(setup_env, monkeypatch, utf8):
    monkeypatch.setattr(SET_UTF8_ENCODING, '_value', utf8)

    code = "\n \n  \n\n" \
           "print('      | A | B |')\n" \
           "print(' Col1 | 1 | 2 |')"
    output = execute_code(code, 'my_file', 1)
    assert output == '      | A | B |\n Col1 | 1 | 2 |'


@pytest.mark.parametrize('utf8', [True, False])
def test_err(setup_env, monkeypatch, utf8):
    monkeypatch.setattr(SET_UTF8_ENCODING, '_value', utf8)

    code = "print('Line1')\nprint('Line2')\n1/0"

    with pytest.raises(CodeExceptionError) as e:
        execute_code(code, Path('/my_file'), 5)

    msg = e.value.pformat()
    assert msg == [
        "   print('Line1')",
        "   print('Line2')",
        '   1/0 <--',
        '',
        'Traceback (most recent call last):',
        '  File "my_file", line 7',
        'ZeroDivisionError: division by zero'
    ]


IS_WIN = os.name == 'nt'


@pytest.mark.skipif(not IS_WIN, reason='Windows only')
def test_unicode_fails(setup_env, monkeypatch):
    code = "print('●')"

    monkeypatch.setattr(SET_UTF8_ENCODING, '_value', False)
    assert execute_code(code, 'my_file', 1) != '●'

    monkeypatch.setattr(SET_UTF8_ENCODING, '_value', True)
    assert execute_code(code, 'my_file', 1) == '●'


@pytest.mark.skipif(IS_WIN, reason='Fails on Windows')
def test_unicode_no_utf8(setup_env, monkeypatch):
    code = "print('●')"

    monkeypatch.setattr(SET_UTF8_ENCODING, '_value', False)
    assert execute_code(code, 'my_file', 1) == '●'

    monkeypatch.setattr(SET_UTF8_ENCODING, '_value', True)
    assert execute_code(code, 'my_file', 1) == '●'
