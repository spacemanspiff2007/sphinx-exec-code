from pathlib import Path

import pytest

from sphinx_exec_code.configuration.path_config import InvalidPathError
from sphinx_exec_code.configuration.values import SphinxConfigFolder


def test_path_errors():
    a = SphinxConfigFolder('config_key_name')

    with pytest.raises(FileNotFoundError) as e:
        a.check_folder_exists(Path('does_not_exist'))
    assert str(e.value) == 'Directory "does_not_exist" not found! (configured by config_key_name)'

    with pytest.raises(InvalidPathError) as e:
        a.make_path(None, 1)
    assert str(e.value) == 'Could not create Path from "1" (type int) (configured by config_key_name)'
