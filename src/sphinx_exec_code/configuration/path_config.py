from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Final

from typing_extensions import override

from sphinx_exec_code.__const__ import log
from sphinx_exec_code.configuration.base import TYPE_VALUE, SphinxConfigValue


if TYPE_CHECKING:
    from sphinx.application import Sphinx as SphinxApp


class InvalidPathError(Exception):
    pass


class _SphinxConfigPathBase(SphinxConfigValue[TYPE_VALUE]):

    def make_path(self, app: SphinxApp, value: Any) -> Path:
        try:
            path = Path(value)
        except Exception:
            msg = (f'Could not create Path from "{value}" (type {type(value).__name__}) '
                   f'(configured by {self.sphinx_name:s})')
            raise InvalidPathError(msg) from None

        if not path.is_absolute():
            path = (Path(app.confdir) / path).resolve()
        return path

    def check_folder_exists(self, folder: Path) -> Path:
        if not folder.is_dir():
            msg = f'Directory "{folder}" not found! (configured by {self.sphinx_name:s})'
            raise FileNotFoundError(msg)
        return folder


class SphinxConfigFolder(_SphinxConfigPathBase[Path]):
    SPHINX_TYPE = (str, Path)

    @override
    def transform_value(self, app: SphinxApp, value: Any) -> Path:
        return self.make_path(app, value)

    @override
    def validate_value(self, value: Path) -> Path:
        return self.check_folder_exists(value)


class SphinxConfigMultipleFolderStr(_SphinxConfigPathBase[tuple[str, ...]]):
    SPHINX_TYPE = ()

    @override
    def transform_value(self, app: SphinxApp, value: Any) -> tuple[str, ...]:
        return tuple(str(self.make_path(app, p)) for p in value)

    @override
    def validate_value(self, value: Any) -> tuple[str, ...]:
        _path_value: Final = tuple(Path(v) for v in value)

        # check that folders exist
        for f in _path_value:
            self.check_folder_exists(f)

        # Search for a python package and print a warning if we find none
        # since this is the only reason to specify additional folders
        for f in _path_value:
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

        return value
