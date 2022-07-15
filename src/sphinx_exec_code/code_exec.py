import os
import subprocess
import sys
from itertools import dropwhile
from pathlib import Path
from typing import Iterable, Optional

from sphinx.errors import ConfigError

from sphinx_exec_code.code_exec_error import CodeException

WORKING_DIR: Optional[str] = None
ADDITIONAL_FOLDERS: Optional[Iterable[str]] = None
STDOUT_ENCODING: str = sys.stdout.encoding


def setup_code_env(cwd: Path, folders: Iterable[Path], encoding: str):
    global WORKING_DIR, ADDITIONAL_FOLDERS, STDOUT_ENCODING
    WORKING_DIR = str(cwd)
    ADDITIONAL_FOLDERS = tuple(map(str, folders))
    STDOUT_ENCODING = encoding


def execute_code(code: str, file: Path, first_loc: int) -> str:
    if WORKING_DIR is None or ADDITIONAL_FOLDERS is None:
        raise ConfigError('Working dir or additional folders are not set!')

    env = os.environ.copy()
    try:
        env['PYTHONPATH'] = os.pathsep.join(ADDITIONAL_FOLDERS) + os.pathsep + env['PYTHONPATH']
    except KeyError:
        env['PYTHONPATH'] = os.pathsep.join(ADDITIONAL_FOLDERS)

    run = subprocess.run([sys.executable, '-c', code], capture_output=True, cwd=WORKING_DIR, env=env)
    if run.returncode != 0:
        raise CodeException(code, file, first_loc, run.returncode, run.stderr.decode()) from None

    # decode output and drop tailing spaces
    ret_str = (run.stdout.decode(encoding=STDOUT_ENCODING) + run.stderr.decode(encoding=STDOUT_ENCODING)).rstrip()

    # drop leading empty lines
    ret_lines = list(dropwhile(lambda x: not x.strip(), ret_str.splitlines()))

    # Normalize newlines
    return '\n'.join(ret_lines)
