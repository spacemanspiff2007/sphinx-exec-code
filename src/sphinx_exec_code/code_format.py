from typing import Iterable, Tuple


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
        self.lines = []

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

        hide.add_line(org_line)
        skip.add_line(org_line)

    shown_code = '\n'.join(hide.lines)
    executed_code = '\n'.join(skip.lines)

    return shown_code.strip(), executed_code.strip()
