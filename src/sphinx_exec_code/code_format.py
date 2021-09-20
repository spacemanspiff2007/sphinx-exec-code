from typing import Iterable, List, Tuple


class VisibilityMarkerError(Exception):
    pass


def _process_code(code_lines: Iterable[str], marker: str) -> List[str]:

    marker_start = f'#{marker}:start'
    marker_stop = f'#{marker}:stop'
    marker_toggle = f'#{marker}:toggle'

    lines = []
    do_add = True
    for org_line in code_lines:
        line = org_line.replace(' ', '').replace('-', '').lower()
        if line == marker_start:
            if not do_add:
                raise VisibilityMarkerError(f'{marker}:start already called! Use {marker}:stop or {marker}:toggle!')
            do_add = False
            continue
        elif line == marker_stop:
            if do_add:
                raise VisibilityMarkerError(f'{marker}:stop already called! Use {marker}:start or {marker}:toggle!')
            do_add = True
            continue
        elif line == marker_toggle:
            do_add = not do_add
            continue

        if do_add:
            lines.append(org_line)
    return lines


def get_show_exec_code(code_lines: Iterable[str]) -> Tuple[str, str]:
    shown_code = '\n'.join(_process_code(code_lines, 'hide'))
    executed_code = '\n'.join(_process_code(code_lines, 'skip'))

    return shown_code.strip(), executed_code.strip()
