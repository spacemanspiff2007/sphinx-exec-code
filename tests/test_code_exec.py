import os
import sys
from pathlib import Path

import pytest

from sphinx_exec_code.code_exec import CodeExceptionError, execute_code
from sphinx_exec_code.configuration import PYTHONPATH_FOLDERS, SET_UTF8_ENCODING, WORKING_DIR


@pytest.fixture()
def _setup_env(monkeypatch) -> None:
    f = Path(__file__).parent
    monkeypatch.setattr(WORKING_DIR, '_value', f)
    monkeypatch.setattr(PYTHONPATH_FOLDERS, '_value', [str(f)])


@pytest.mark.parametrize('utf8', [True, False])
@pytest.mark.usefixtures('_setup_env')
def test_print(monkeypatch, utf8) -> None:
    monkeypatch.setattr(SET_UTF8_ENCODING, '_value', utf8)

    code = "print('Line1')\nprint('Line2')"
    output = execute_code(code, 'my_file', 1)
    assert output == 'Line1\nLine2'


@pytest.mark.parametrize('utf8', [True, False])
@pytest.mark.usefixtures('_setup_env')
def test_print_table(monkeypatch, utf8) -> None:
    monkeypatch.setattr(SET_UTF8_ENCODING, '_value', utf8)

    code = "\n \n  \n\n" \
           "print('      | A | B |')\n" \
           "print(' Col1 | 1 | 2 |')"
    output = execute_code(code, 'my_file', 1)
    assert output == '      | A | B |\n Col1 | 1 | 2 |'


PYTHON_3_13 = sys.version_info[:2] >= (3, 13)


@pytest.mark.skipif(PYTHON_3_13, reason='Old traceback')
@pytest.mark.parametrize('utf8', [True, False])
@pytest.mark.usefixtures('_setup_env')
def test_err_12(monkeypatch, utf8) -> None:
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


@pytest.mark.skipif(not PYTHON_3_13, reason='Old traceback')
@pytest.mark.parametrize('utf8', [True, False])
@pytest.mark.usefixtures('_setup_env')
def test_err_13(monkeypatch, utf8) -> None:
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
        '    1/0',
        '    ~^~',
        'ZeroDivisionError: division by zero'
    ]


IS_WIN = os.name == 'nt'


@pytest.mark.skipif(not IS_WIN, reason='Windows only')
@pytest.mark.usefixtures('_setup_env')
def test_unicode_fails(monkeypatch) -> None:
    code = "print('●')"

    monkeypatch.setattr(SET_UTF8_ENCODING, '_value', False)
    assert execute_code(code, 'my_file', 1) != '●'

    monkeypatch.setattr(SET_UTF8_ENCODING, '_value', True)
    assert execute_code(code, 'my_file', 1) == '●'

    code = "print('This is a beautiful unicode character: \u265E.')"
    assert execute_code(code, 'my_file', 1) == 'This is a beautiful unicode character: \u265E.'


@pytest.mark.skipif(IS_WIN, reason='Fails on Windows')
@pytest.mark.usefixtures('_setup_env')
def test_unicode_no_utf8(monkeypatch) -> None:
    code = "print('●')"

    monkeypatch.setattr(SET_UTF8_ENCODING, '_value', False)
    assert execute_code(code, 'my_file', 1) == '●'

    monkeypatch.setattr(SET_UTF8_ENCODING, '_value', True)
    assert execute_code(code, 'my_file', 1) == '●'
