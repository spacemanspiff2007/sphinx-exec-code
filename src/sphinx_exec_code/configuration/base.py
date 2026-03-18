from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, Generic, TypeVar

from sphinx.errors import ConfigError

from sphinx_exec_code.__const__ import log


if TYPE_CHECKING:
    from sphinx.application import Sphinx as SphinxApp


TYPE_VALUE = TypeVar('TYPE_VALUE')


class SphinxConfigValue(Generic[TYPE_VALUE]):
    SPHINX_TYPE: tuple[type[Any], ...] | type[Any]

    def __init__(self, sphinx_name: str, initial_value: TYPE_VALUE | None = None) -> None:
        self.sphinx_name: Final = sphinx_name
        self._value: TYPE_VALUE | None = initial_value

    @property
    def value(self) -> TYPE_VALUE:
        if self._value is None:
            msg = f'{self.sphinx_name} is not set!'
            raise ConfigError(msg)
        return self._value

    def transform_value(self, app: SphinxApp, value: Any) -> TYPE_VALUE:
        return value

    def validate_value(self, value: Any) -> TYPE_VALUE:
        return value

    def from_app(self, app: SphinxApp) -> TYPE_VALUE:
        # load value
        value = self.transform_value(app, getattr(app.config, self.sphinx_name))

        # log transformed value
        assert self.sphinx_name.startswith('exec_code_')
        name = self.sphinx_name[10:].replace('_', ' ').capitalize()
        log.debug(f'[exec-code] {name:s}: {value}')

        # additional validation
        self._value = self.validate_value(value)
        return self._value

    def add_config_value(self, app: SphinxApp, sphinx_default: TYPE_VALUE) -> None:
        self.validate_value(sphinx_default)
        app.add_config_value(self.sphinx_name, sphinx_default, 'env', self.SPHINX_TYPE)
