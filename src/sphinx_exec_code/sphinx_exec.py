import traceback
from pathlib import Path

from docutils.statemachine import StringList
from sphinx.directives.code import CodeBlock
from sphinx.errors import ExtensionError
from sphinx.util.docutils import SphinxDirective

from sphinx_exec_code.__const__ import log
from sphinx_exec_code.code_exec import CodeExceptionError, execute_code
from sphinx_exec_code.code_format import VisibilityMarkerError, get_show_exec_code
from sphinx_exec_code.configuration import EXAMPLE_DIR
from sphinx_exec_code.sphinx_spec import SphinxSpecBase, build_spec, get_specs


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
            raise e from None
        except Exception as e:
            name = self.__class__.__name__
            log.error(f'Error while running {name}!')
            log.error(f'File: {self.get_location()}')
            if not isinstance(e, VisibilityMarkerError):
                for line in traceback.format_exc().splitlines():
                    log.error(line)

            msg = f'Error while running {name}!'
            raise ExtensionError(msg, orig_exc=e) from None

    def _get_code_line(self, line_no: int, content: StringList) -> int:
        """Get the first line number of the code"""
        if not content:
            return line_no

        i = 0
        first_line = content[0]

        for i, raw_line in enumerate(self.block_text.splitlines()):
            # raw line contains the leading white spaces
            if raw_line.lstrip() == first_line:
                break

        return line_no + i

    def _run(self) -> list:
        """ Executes python code for an RST document, taking input from content or from a filename
        :return:
        """
        output = []
        raw_file, raw_line = self.get_source_info()
        content = self.content

        file = Path(raw_file)
        line = self._get_code_line(raw_line, content)

        code_spec, output_spec = get_specs(self.options)

        # Read from example files
        if code_spec.filename:
            filename = (EXAMPLE_DIR.value / code_spec.filename).resolve()
            content = filename.read_text(encoding='utf-8').splitlines()
            file, line = filename, 1

        # format the code
        try:
            code_show, code_exec = get_show_exec_code(content)
        except Exception as e:
            msg = f'Could not parse code markers at {self.get_location()}'
            raise ExtensionError(msg, orig_exc=e) from None

        # Show the code from the user
        self.create_literal_block(output, code_show, code_spec, line)

        try:
            code_results = execute_code(code_exec, file, line)
        except CodeExceptionError as e:
            # Newline so we don't have the build message mixed up with logs
            print()

            # Log pretty message
            for line in e.pformat():
                log.error(line)

            msg = 'Could not execute code!'
            raise ExtensionError(msg) from None

        # Show the output from the code execution
        self.create_literal_block(output, code_results, output_spec, line)
        return output

    def create_literal_block(self, objs: list, code: str, spec: SphinxSpecBase, line: int) -> None:
        if spec.hide or not code:
            return None

        c = CodeBlock(
            'code-block', [spec.language], spec.spec,
            StringList(code.splitlines()),
            line,
            # I'm not sure what these two do
            self.content_offset, '',
            # Let's hope these are just for producing error messages and not for anything else
            self.state, self.state_machine
        )

        objs.extend(c.run())
        return None
