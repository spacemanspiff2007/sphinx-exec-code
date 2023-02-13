from typing import Iterable, List, Tuple


class VisibilityMarkerError(Exception):
    pass


class CodeMarker:
    MARKERS = ('hide', 'skip')

    def __init__(self, marker: str):
        assert marker in CodeMarker.MARKERS
        self.start = f'#{marker}:start'
        self.stop = f'#{marker}:stop'
        self.toggle = f'#{marker}:toggle'

        self.do_add = True
        self.skip_empty = False
        self.lines: List[str] = []

    def is_marker(self, line: str) -> bool:
        if line == self.start:
            if not self.do_add:
                raise VisibilityMarkerError(f'{self.start[1:]} already called! '
                                            f'Use {self.stop[1:]} or {self.toggle[1:]}!')
            self.do_add = False
            return True

        if line == self.stop:
            if self.do_add:
                raise VisibilityMarkerError(f'{self.stop[1:]} already called! '
                                            f'Use {self.start[1:]} or {self.toggle[1:]}!')
            self.do_add = True
            self.skip_empty = True
            return True

        if line == self.toggle:
            self.do_add = not self.do_add
            return True

        return False

    def add_line(self, line: str):
        if not self.do_add:
            return None

        if self.skip_empty:
            if not line.strip():
                return None
            self.skip_empty = False

        self.lines.append(line)

    def get_lines(self) -> List[str]:
        # remove leading and tailing empty lines of the code
        code_lines = self.lines
        while code_lines and not code_lines[0].strip():
            code_lines.pop(0)
        while code_lines and not code_lines[-1].strip():
            code_lines.pop(-1)
        return code_lines


def get_show_exec_code(code_lines: Iterable[str]) -> Tuple[str, str]:
    shown = CodeMarker('hide')
    executed = CodeMarker('skip')

    for org_line in code_lines:
        line = org_line.replace(' ', '').replace('-', '').lower()

        if shown.is_marker(line) or executed.is_marker(line):
            continue

        add_line = org_line.rstrip()
        shown.add_line(add_line)
        executed.add_line(add_line)

    shown_lines = shown.get_lines()

    # check if the shown code block is indented as a whole -> strip
    leading_spaces = [len(line) - len(line.lstrip()) for line in shown_lines]
    if strip_spaces := min(leading_spaces, default=0):
        for i, line in enumerate(shown_lines):
            shown_lines[i] = line[strip_spaces:]

    shown_code = '\n'.join(shown_lines)
    executed_code = '\n'.join(executed.get_lines())

    return shown_code, executed_code.strip()
