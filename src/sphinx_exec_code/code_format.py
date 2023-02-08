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


def get_show_exec_code(code_lines: Iterable[str]) -> Tuple[str, str]:
    hide = CodeMarker('hide')
    skip = CodeMarker('skip')

    for org_line in code_lines:
        line = org_line.replace(' ', '').replace('-', '').lower()

        if hide.is_marker(line):
            continue
        if skip.is_marker(line):
            continue

        add_line = org_line.rstrip()
        hide.add_line(add_line)
        skip.add_line(add_line)

    # remove leading and tailing empty lines of the shown code
    shown_lines = hide.lines
    while shown_lines and not shown_lines[0].strip():
        shown_lines.pop(0)
    while shown_lines and not shown_lines[-1].strip():
        shown_lines.pop(-1)

    # check if the shown code block is indented as a whole -> strip
    leading_spaces = [len(line) - len(line.lstrip()) for line in shown_lines]
    if strip_spaces := min(leading_spaces):
        for i, line in enumerate(shown_lines):
            shown_lines[i] = line[strip_spaces:]

    shown_code = '\n'.join(shown_lines)
    executed_code = '\n'.join(skip.lines)

    return shown_code, executed_code.strip()
