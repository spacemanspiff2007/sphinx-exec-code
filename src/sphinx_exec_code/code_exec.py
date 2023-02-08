import os
import subprocess
import sys
from itertools import dropwhile
from pathlib import Path

from sphinx_exec_code.code_exec_error import CodeExceptionError
from sphinx_exec_code.configuration import PYTHONPATH_FOLDERS, SET_UTF8_ENCODING, WORKING_DIR


def execute_code(code: str, file: Path, first_loc: int) -> str:
    cwd: Path = WORKING_DIR.value
    encoding = 'utf-8' if SET_UTF8_ENCODING.value else None
    python_folders = PYTHONPATH_FOLDERS.value

    env = os.environ.copy()

    if python_folders:
        try:
            env['PYTHONPATH'] = os.pathsep.join(python_folders) + os.pathsep + env['PYTHONPATH']
        except KeyError:
            env['PYTHONPATH'] = os.pathsep.join(python_folders)

    run = subprocess.run([sys.executable, '-c', code.encode('utf-8')], capture_output=True, text=True,
                         encoding=encoding, cwd=cwd, env=env)

    if run.returncode != 0:
        raise CodeExceptionError(code, file, first_loc, run.returncode, run.stderr) from None

    # decode output and drop tailing spaces
    ret_str = (run.stdout if run.stdout is not None else '' + run.stderr if run.stderr is not None else '').rstrip()

    # drop leading empty lines
    ret_lines = list(dropwhile(lambda x: not x.strip(), ret_str.splitlines()))

    # Normalize newlines
    return '\n'.join(ret_lines)
