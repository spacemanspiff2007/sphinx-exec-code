from pathlib import Path

from sphinx_exec_code import __version__
from sphinx_exec_code.__const__ import log
from sphinx_exec_code.code_exec import setup_code_env
from sphinx_exec_code.sphinx_exec import ExecCode

CONF_NAME_CWD = 'exec_code_working_dir'
CONF_NAME_DIRS = 'exec_code_folders'


def mk_path(app, obj) -> Path:
    confdir = Path(app.confdir)
    path = Path(obj)
    if not path.is_absolute():
        path = (confdir / path).resolve()
    return path


def builder_ready(app):
    cwd = mk_path(app, app.config.exec_code_working_dir)
    folders = tuple(mk_path(app, _p) for _p in app.config.exec_code_folders)

    log.debug(f'[exec-code] Working dir: {cwd}')
    log.debug(f'[exec-code] Folders: {", ".join(map(str, folders))}')

    # Ensure dirs are valid
    if not cwd.is_dir():
        raise FileNotFoundError(f'Working directory "{cwd}" not found! (configured by {CONF_NAME_CWD})')
    for _f in folders:
        if not _f.is_dir():
            raise FileNotFoundError(f'Additional directory "{_f}" not found! (configured by {CONF_NAME_DIRS})')

    # Search for a python package and print a warning if we find none
    # since this is the only reason to specify a working dir
    for _f in folders:
        for __f in _f.iterdir():
            if not __f.is_dir():
                continue

            # log warning if we don't find a python package
            for file in __f.iterdir():
                if file.name == '__init__.py':
                    break
            else:
                log.warning(f'[exec-code] No Python package found in {_f}')

    setup_code_env(cwd, folders)
    return None


def setup(app):
    """ Register sphinx_execute_code directive with Sphinx """

    confdir = Path(app.confdir)

    cwd = str(confdir.parent)

    code_folders = []
    src_dir = confdir.with_name('src')
    if src_dir.is_dir():
        code_folders.append(str(src_dir))

    # config options
    app.add_config_value(CONF_NAME_CWD, cwd, 'env',)
    app.add_config_value(CONF_NAME_DIRS, code_folders, 'env')

    app.connect('builder-inited', builder_ready)
    app.add_directive('exec_code', ExecCode)

    log.debug(f'[exec-code] Version: {__version__}')
    return {'version': __version__}
