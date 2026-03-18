from __future__ import annotations

from typing import TYPE_CHECKING, Any

from typing_extensions import override

from sphinx_exec_code.configuration.base import SphinxConfigValue


if TYPE_CHECKING:
    from sphinx.application import Sphinx as SphinxApp


class SphinxConfigFlag(SphinxConfigValue[bool]):
    SPHINX_TYPE = bool

    @override
    def validate_value(self, value: Any) -> bool:
        if not isinstance(value, bool):
            raise TypeError()
        return value

    @override
    def transform_value(self, app: SphinxApp, value: Any) -> bool:
        return bool(value)
