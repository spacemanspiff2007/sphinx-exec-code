from sphinx.application import Sphinx as SphinxApp

from sphinx_exec_code.configuration.base import SphinxConfigValue


class SphinxConfigFlag(SphinxConfigValue[bool]):
    SPHINX_TYPE = bool

    def transform_value(self, app: SphinxApp, value) -> bool:
        return bool(value)
