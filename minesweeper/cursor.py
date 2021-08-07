"""
Helper functions to move the cursor around in standard out
"""


def cursor_up(n):
    write_chars('\x1b[1A', n)


def cursor_down(n):
    write_chars('\x1b[1B', n)


def cursor_left(n):
    write_chars('\x1b[1D', n)


def cursor_right(n):
    write_chars('\x1b[1C', n)


def clear_last_lines(n):
    write_chars('\x1b[1A\x1b[2K', n)


def write_chars(ch, n):
    print(ch * n, end='', flush=True)
