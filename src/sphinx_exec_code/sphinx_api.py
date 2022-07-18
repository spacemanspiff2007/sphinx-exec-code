import os
from pathlib import Path

from sphinx.application import Sphinx as SphinxApp

from sphinx_exec_code import __version__
from sphinx_exec_code.__const__ import log
from sphinx_exec_code.sphinx_exec import ExecCode

from .configuration import EXAMPLE_DIR, PYTHONPATH_FOLDERS, SET_UTF8_ENCODING, WORKING_DIR


def builder_ready(app: SphinxApp):
    # load configuration
    EXAMPLE_DIR.from_app(app)
    WORKING_DIR.from_app(app)
    PYTHONPATH_FOLDERS.from_app(app)
    SET_UTF8_ENCODING.from_app(app)
    return None


def setup(app):
    """ Register sphinx_execute_code directive with Sphinx """

    confdir = Path(app.confdir)

    code_folders = []
    src_dir = confdir.with_name('src')
    if src_dir.is_dir():
        code_folders.append(src_dir)

    # Configuration options
    EXAMPLE_DIR.add_config_value(app, confdir)
    WORKING_DIR.add_config_value(app, confdir.parent)
    PYTHONPATH_FOLDERS.add_config_value(app, code_folders)
    SET_UTF8_ENCODING.add_config_value(app, True if os.name == 'nt' else False)  # Somehow this workaround is required

    app.connect('builder-inited', builder_ready)
    app.add_directive('exec_code', ExecCode)

    log.debug(f'[exec-code] Version: {__version__}')

    return {
        'version': __version__,

        # https://github.com/spacemanspiff2007/sphinx-exec-code/issues/2
        # This extension does not store any states making it safe for parallel reading
        'parallel_read_safe': True
    }
