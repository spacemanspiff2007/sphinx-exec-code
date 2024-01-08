from sphinx.application import Sphinx as SphinxApp

from sphinx_exec_code.configuration.base import SphinxConfigValue


class SphinxConfigFlag(SphinxConfigValue[bool]):
    SPHINX_TYPE = bool

    def validate_value(self, value) -> bool:
        if not isinstance(value, bool):
            raise TypeError()
        return value

    def transform_value(self, app: SphinxApp, value) -> bool:
        return bool(value)
