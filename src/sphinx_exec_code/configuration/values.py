from typing import Final

from .flag_config import SphinxConfigFlag
from .path_config import SphinxConfigFolder, SphinxConfigMultipleFolderStr


EXAMPLE_DIR: Final = SphinxConfigFolder('exec_code_example_dir')

# Options for code execution
WORKING_DIR: Final = SphinxConfigFolder('exec_code_working_dir')
PYTHONPATH_FOLDERS: Final = SphinxConfigMultipleFolderStr('exec_code_source_folders')
SET_UTF8_ENCODING: Final = SphinxConfigFlag('exec_code_set_utf8_encoding')
