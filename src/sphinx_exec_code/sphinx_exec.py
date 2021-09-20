import traceback

from docutils import nodes
from sphinx.errors import ExtensionError
from sphinx.util.docutils import SphinxDirective

from sphinx_exec_code.__const__ import log
from sphinx_exec_code.code_exec import CodeException, execute_code
from sphinx_exec_code.code_format import get_show_exec_code, VisibilityMarkerError
from sphinx_exec_code.sphinx_spec import build_spec, SpecCode, SpecOutput, SphinxSpecBase


def create_literal_block(objs: list, code: str, spec: SphinxSpecBase):
    if spec.hide or not code:
        return None

    # generate header if specified
    if spec.caption:
        objs.append(nodes.caption(text=spec.caption))

    # generate code block
    block = nodes.literal_block(code, code)
    objs.append(block)

    # set linenos
    block['linenos'] = spec.linenos
    block['language'] = spec.language
    return None


class ExecCode(SphinxDirective):
    """ Sphinx class for execute_code directive
    """
    has_content = True

    option_spec = build_spec()

    required_arguments = 0
    optional_arguments = len(option_spec)

    def run(self) -> list:
        try:
            return self._run()
        except ExtensionError as e:
            raise e
        except Exception as e:
            name = self.__class__.__name__
            log.error(f'Error while running {name}!')
            log.error(f'File: {self.get_location()}')
            if not isinstance(e, VisibilityMarkerError):
                for line in traceback.format_exc().splitlines():
                    log.error(line)
            raise ExtensionError(f'Error while running {name}!', orig_exc=e)

    def _run(self) -> list:
        """ Executes python code for an RST document, taking input from content or from a filename
        :return:
        """
        output = []

        # format the code
        code_show, code_exec = get_show_exec_code(self.content)

        # Show the code from the user
        create_literal_block(output, code_show, spec=SpecCode.from_options(self.options))

        file, line = self.get_source_info()
        try:
            code_results = execute_code(code_exec, file, line)
        except CodeException as e:
            # Newline so we don't have the build message mixed up with logs
            print()

            # Log pretty message
            for line in e.pformat():
                log.error(line)

            raise ExtensionError('Could not execute code!') from None

        # Show the output from the code execution
        create_literal_block(output, code_results, spec=SpecOutput.from_options(self.options))
        return output
