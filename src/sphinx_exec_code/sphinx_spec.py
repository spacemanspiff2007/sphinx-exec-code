from typing import Any, ClassVar, Dict, Final, Tuple

from docutils.nodes import literal_block
from docutils.parsers.rst import directives
from sphinx.directives.code import CodeBlock
from sphinx.util.typing import OptionSpec

from sphinx_exec_code.__const__ import log


class SphinxSpecBase:
    defaults: ClassVar[Dict[str, str]]

    @staticmethod
    def alias_to_name(alias: str) -> str:
        raise NotImplementedError()

    @staticmethod
    def name_to_alias(name: str) -> str:
        raise NotImplementedError()

    @staticmethod
    def post_process_spec(spec: Dict[str, Any], options: Dict[str, Any]) -> None:
        raise NotImplementedError()

    def __init__(self, spec: Dict[str, Any]) -> None:
        self.hide: Final = spec.pop('hide')
        self.language: Final = spec.pop('language')
        self.spec: Final = spec

    def set_block_spec(self, block: literal_block) -> None:
        for name, value in self.spec.items():
            block[name] = value
        return None

    @classmethod
    def from_options(cls, options: Dict[str, Any]) -> 'SphinxSpecBase':
        spec_names = tuple(cls.create_spec().keys())

        spec = {cls.alias_to_name(n): v for n, v in cls.defaults.items()}
        for name in spec_names:
            if name not in options:
                continue
            spec[cls.alias_to_name(name)] = options[name]

        cls.post_process_spec(spec, options)
        return cls(spec=spec)

    @classmethod
    def create_spec(cls) -> OptionSpec:

        # spec from CodeBlock
        this_spec: OptionSpec = {}
        for name, directive in CodeBlock.option_spec.items():
            this_spec[cls.name_to_alias(name)] = directive

        # own flags after the default flags so we overwrite them in case we have duplicate names
        for name, default in cls.defaults.items():
            # all own options are currently strings
            if isinstance(default, str):
                this_spec[cls.name_to_alias(name)] = directives.unchanged
            elif isinstance(default, bool):
                this_spec[cls.name_to_alias(name)] = directives.flag
            else:
                msg = f'Unsupported type {type(default)} for default "{name:s}"!'
                raise TypeError(msg)

        return this_spec


def build_spec() -> OptionSpec:
    spec: OptionSpec = {}
    spec.update(SpecCode.create_spec())
    spec.update(SpecOutput.create_spec())
    return spec


def get_specs(options: Dict[str, Any]) -> Tuple['SpecCode', 'SpecOutput']:
    supported = set(SpecCode.create_spec()) | set(SpecOutput.create_spec())
    invalid = set(options) - supported

    if invalid:
        msg = (
            f'Invalid option{"s" if len(invalid) != 1 else ""}: '
            f'{", ".join(sorted(map(str, invalid)))}! Supported: {", ".join(sorted(map(str, supported)))}'
        )
        raise ValueError(msg)

    return SpecCode.from_options(options), SpecOutput.from_options(options)


class SpecCode(SphinxSpecBase):
    defaults: ClassVar = {
        'filename': '',
        'hide_code': False,    # deprecated 2024 - remove after some time, must come before the new hide flag!
        'hide': False,
        'language': 'python',
    }

    @staticmethod
    def alias_to_name(alias: str) -> str:
        if alias == 'hide_code':
            log.info('The "hide_code" directive is deprecated! Use "hide" instead!')
            return 'hide'
        return alias

    @staticmethod
    def name_to_alias(name: str) -> str:
        return name

    @staticmethod
    def post_process_spec(spec: Dict[str, Any], options :Dict[str, Any]) -> None:
        return None

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        super().__init__(**kwargs)
        self.filename: Final[str] = self.spec.pop('filename')


class SpecOutput(SphinxSpecBase):
    @staticmethod
    def alias_to_name(alias: str) -> str:
        if alias.endswith('_output'):
            return alias[:-7]
        return alias

    @staticmethod
    def name_to_alias(name: str) -> str:
        if name.endswith('_output'):
            return name
        return name + '_output'

    @staticmethod
    def post_process_spec(spec: Dict[str, Any], options: Dict[str, Any]) -> None:
        # if we have a name for code but not for output we programmatically build it by appending the _output suffix
        name_output = SpecOutput.name_to_alias('name')
        if name_output in options:
            return None

        name_code = SpecCode.name_to_alias('name')
        if name_code not in options:
            return None

        # if we have a name for input we create a name for output
        spec['name'] = f'{options[name_code]:s}_output'

    defaults: ClassVar = {
        'hide': False,
        'language': 'none',
    }
