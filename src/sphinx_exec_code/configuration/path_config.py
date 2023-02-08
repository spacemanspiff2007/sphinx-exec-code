from pathlib import Path
from typing import Tuple

from sphinx.application import Sphinx as SphinxApp

from sphinx_exec_code.__const__ import log
from sphinx_exec_code.configuration.base import SphinxConfigValue, TYPE_VALUE


class InvalidPathError(Exception):
    pass


class SphinxConfigPath(SphinxConfigValue[TYPE_VALUE]):
    SPHINX_TYPE = (str, Path)

    def make_path(self, app: SphinxApp, value) -> Path:
        try:
            path = Path(value)
        except Exception:
            raise InvalidPathError(f'Could not create Path from "{value}" (type {type(value).__name__}) '
                                   f'(configured by {self.sphinx_name:s})') from None

        if not path.is_absolute():
            path = (Path(app.confdir) / path).resolve()
        return path

    def check_folder_exists(self, folder: Path) -> Path:
        if not folder.is_dir():
            raise FileNotFoundError(f'Directory "{folder}" not found! (configured by {self.sphinx_name:s})')
        return folder


class SphinxConfigFolder(SphinxConfigPath[Path]):
    def transform_value(self, app: SphinxApp, value) -> Path:
        return self.make_path(app, value)

    def validate_value(self, value: Path) -> Path:
        return self.check_folder_exists(value)


class SphinxConfigMultipleFolderStr(SphinxConfigPath[Tuple[str, ...]]):
    SPHINX_TYPE = ()

    def transform_value(self, app: SphinxApp, value) -> Tuple[Path, ...]:
        return tuple(self.make_path(app, p) for p in value)

    def validate_value(self, value: Tuple[Path, ...]) -> Tuple[str, ...]:
        # check that folders exist
        for f in value:
            self.check_folder_exists(f)

        # Search for a python package and print a warning if we find none
        # since this is the only reason to specify additional folders
        for f in value:
            package_found = False
            for _f in f.iterdir():
                if not _f.is_dir():
                    continue

                # log warning if we don't find a python package
                for file in _f.glob('__init__.py'):
                    if file.name == '__init__.py':
                        package_found = True
                        break
                if package_found:
                    break

            if not package_found:
                log.warning(f'[exec-code] No Python packages found in {f}')

        return tuple(map(str, value))
