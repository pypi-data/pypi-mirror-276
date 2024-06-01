from .constant import *
from same_print import sprint

def print(*args, sep=' ', end='\n', file=None, bold=False, italicized=False):
    txt = ''
    if bold:
        txt += BOLD
    if italicized:
        txt += ITALICIZED
    for arg in args:
        txt += arg
        txt += sep
    if args:
        txt = txt[:-1]
    if b'\033[' in txt.encode():
        txt += ENDC
    sprint(txt, end=end, file=file)
