from pathlib import Path

import pytest

import sphinx_exec_code.code_exec
from sphinx_exec_code.code_exec import CodeException, execute_code


@pytest.fixture
def setup_env(monkeypatch):
    f = Path(__file__).parent
    monkeypatch.setattr(sphinx_exec_code.code_exec, 'WORKING_DIR', str(f))
    monkeypatch.setattr(sphinx_exec_code.code_exec, 'ADDITIONAL_FOLDERS', [str(f)])

    yield


def test_print(setup_env):
    code = "print('Line1')\nprint('Line2')"
    output = execute_code(code, 'my_file', 1)
    assert output == 'Line1\nLine2'


def test_err(setup_env):
    code = "print('Line1')\nprint('Line2')\n1/0"

    with pytest.raises(CodeException) as e:
        execute_code(code, 'my_file', 5)

    msg = e.value.pformat()
    assert msg == [
        "   print('Line1')",
        "   print('Line2')",
        '   1/0 <--',
        '',
        'Traceback (most recent call last):',
        '  File "my_file", line 9',
        'ZeroDivisionError: division by zero'
    ]
