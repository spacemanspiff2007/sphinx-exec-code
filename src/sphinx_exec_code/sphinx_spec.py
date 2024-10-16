from typing import Any, Callable, ClassVar, Dict, Tuple

from docutils.parsers.rst import directives  # type: ignore


class SphinxSpecBase:
    aliases: ClassVar[Dict[str, str]]
    defaults: ClassVar[Dict[str, str]]

    def __init__(self, hide: bool, linenos: bool, caption: str, language: str) -> None:
        # flags
        self.hide = hide
        self.linenos = linenos
        # values
        self.caption = caption
        self.language = language

    @classmethod
    def from_options(cls, options: Dict[str, Any]) -> 'SphinxSpecBase':
        opts = {}
        for alias, name in cls.aliases.items():
            if name not in cls.defaults:
                # is a flag
                opts[name] = alias in options
            else:
                # is a value
                val = options.get(alias, None)
                if not val:
                    val = cls.defaults[name]
                opts[name] = val

        return cls(**opts)

    @classmethod
    def update_spec(cls, spec: Dict[str, Callable[[Any], Any]]) -> None:
        for alias, name in cls.aliases.items():
            # Flags don't have a default
            spec[alias] = directives.flag if name not in cls.defaults else directives.unchanged


def build_spec() -> Dict[str, Callable[[Any], Any]]:
    spec = {}
    SpecCode.update_spec(spec)
    SpecOutput.update_spec(spec)
    return spec


def get_specs(options: Dict[str, Any]) -> Tuple['SpecCode', 'SpecOutput']:
    supported = set(SpecCode.aliases) | set(SpecOutput.aliases)
    invalid = set(options) - supported

    if invalid:
        msg = (
            f'Invalid option{"s" if len(invalid) != 1 else ""}: '
            f'{", ".join(sorted(map(str, invalid)))}! Supported: {", ".join(sorted(map(str, supported)))}'
        )
        raise ValueError(msg)

    return SpecCode.from_options(options), SpecOutput.from_options(options)


class SpecCode(SphinxSpecBase):
    aliases: ClassVar = {
        'hide_code': 'hide',
        'caption': 'caption',
        'language': 'language',
        'linenos': 'linenos',
        'filename': 'filename',
    }
    defaults: ClassVar = {
        'caption': '',
        'language': 'python',
        'filename': '',
    }

    def __init__(self, hide: bool, linenos: bool, caption: str, language: str, filename: str) -> None:
        super().__init__(hide, linenos, caption, language)
        self.filename: str = filename


class SpecOutput(SphinxSpecBase):
    aliases: ClassVar = {
        'hide_output': 'hide',
        'caption_output': 'caption',
        'language_output': 'language',
        'linenos_output': 'linenos',
    }
    defaults: ClassVar = {
        'caption': '',
        'language': 'none',
    }
