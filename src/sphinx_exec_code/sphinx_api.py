from pathlib import Path

from sphinx_exec_code import __version__
from sphinx_exec_code.__const__ import log
from sphinx_exec_code.code_exec import setup_code_env
from sphinx_exec_code.sphinx_exec import ExecCode, setup_example_dir

CONF_NAME_CWD = 'exec_code_working_dir'
CONF_NAME_DIRS = 'exec_code_folders'
CONF_NAME_SAMPLE_DIR = 'exec_code_example_dir'


def mk_path(app, obj) -> Path:
    confdir = Path(app.confdir)
    path = Path(obj)
    if not path.is_absolute():
        path = (confdir / path).resolve()
    return path


def builder_ready(app):
    cwd = mk_path(app, getattr(app.config, CONF_NAME_CWD))
    folders = tuple(mk_path(app, _p) for _p in getattr(app.config, CONF_NAME_DIRS))
    example_dir = mk_path(app, getattr(app.config, CONF_NAME_SAMPLE_DIR))

    log.debug(f'[exec-code] Working dir: {cwd}')
    log.debug(f'[exec-code] Folders: {", ".join(map(str, folders))}')
    log.debug(f'[exec-code] Example dir: {example_dir}')

    # Ensure dirs are valid
    if not cwd.is_dir():
        raise FileNotFoundError(f'Working directory "{cwd}" not found! (configured by {CONF_NAME_CWD})')
    if not example_dir.is_dir():
        raise FileNotFoundError(f'Example directory "{example_dir}" not found! (configured by {CONF_NAME_SAMPLE_DIR})')
    for _f in folders:
        if not _f.is_dir():
            raise FileNotFoundError(f'Additional directory "{_f}" not found! (configured by {CONF_NAME_DIRS})')

    # Search for a python package and print a warning if we find none
    # since this is the only reason to specify additional folders
    for _f in folders:
        package_found = False
        for __f in _f.iterdir():
            if not __f.is_dir():
                continue

            # log warning if we don't find a python package
            for file in __f.iterdir():
                if file.name == '__init__.py':
                    package_found = True
                    break
            if package_found:
                break

        if not package_found:
            log.warning(f'[exec-code] No Python packages found in {_f}')

    setup_example_dir(example_dir)
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
    app.add_config_value(CONF_NAME_SAMPLE_DIR, confdir, 'env')

    app.connect('builder-inited', builder_ready)
    app.add_directive('exec_code', ExecCode)

    log.debug(f'[exec-code] Version: {__version__}')

    return {
        'version': __version__,

        # https://github.com/spacemanspiff2007/sphinx-exec-code/issues/2
        # This extension does not store any states so it should be safe for parallel reading
        'parallel_read_safe': True
    }
