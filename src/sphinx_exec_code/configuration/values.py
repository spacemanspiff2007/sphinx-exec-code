from .flag_config import SphinxConfigFlag
from .path_config import SphinxConfigFolder, SphinxConfigMultipleFolderStr

EXAMPLE_DIR = SphinxConfigFolder('exec_code_example_dir')

# Options for code execution
WORKING_DIR = SphinxConfigFolder('exec_code_working_dir')
PYTHONPATH_FOLDERS = SphinxConfigMultipleFolderStr('exec_code_source_folders')
SET_UTF8_ENCODING = SphinxConfigFlag('exec_code_set_utf8_encoding')
