import re
from pathlib import Path
from typing import List

re_line = re.compile(r'^\s*File "(<string>)", line (\d+), in <module>', re.MULTILINE)


class CodeException(Exception):
    def __init__(self, code: str, file: Path, first_loc: int, ret: int, stderr: str):
        self.code = code

        self.file: Path = file
        self.first_loc: int = first_loc

        self.exec_ret = ret
        self.exec_err = stderr

    def _err_line(self, lines: List[str]) -> int:
        # Find the last line where the error happened
        err_line = len(lines)
        for m in re_line.finditer(self.exec_err):
            err_line = int(m.group(2))
        return err_line - 1

    def pformat(self) -> List[str]:
        filename = self.file.name
        code_lines = self.code.splitlines()
        err_line = self._err_line(code_lines)

        ret = []

        # add code snippet
        snip_start = max(0, err_line - 8)
        snip_last = min(err_line + 1, len(code_lines))
        for i in range(snip_start, snip_last):
            ret.append(f'   {code_lines[i]}' if i != err_line else f'   {code_lines[err_line]} <--')

        # add traceback
        ret.append('')
        for tb_line in self.exec_err.splitlines():
            m = re_line.search(tb_line)
            if m:
                tb_line = tb_line.replace('File "<string>"', f'File "{filename}"')
                tb_line = tb_line.replace('File "<string>"', f'File "{filename}"')
                tb_line = tb_line.replace(f', line {m.group(2)}, in <module>',
                                          f', line {int(m.group(2)) + self.first_loc - 1}')
            ret.append(tb_line)
        return ret
