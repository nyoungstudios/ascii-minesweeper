import sys
import termios
import tty

# konami code
CODE = [27, 91, 65, 27, 91, 65, 27, 91, 66, 27, 91, 66, 27, 91, 68, 27, 91, 67, 27, 91, 68, 27, 91, 67, 98, 97, 10]

# character integer sequences for the arrow keys
UP = [27, 91, 65]
DOWN = [27, 91, 66]
LEFT = [27, 91, 68]
RIGHT = [27, 91, 67]
DELETE_SEQ = [27, 91, 51, 126]


class Keys:
    # constant identifiers for game controls
    W = 'w'
    A = 'a'
    S = 's'
    D = 'd'
    ENTER = 'enter'
    SPACE = 'space'
    BACKSPACE = 'backspace'
    DELETE = 'delete'


def get_char():
    """
    Reads a single character from standard in. CTRL-C raises a KeyboardInterrupt exception

    :return: a string for the character read from standard in
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


class Input:
    def __init__(self):
        # stores the input word
        self._word = ''
        # stores the sequence of characters represented by their ascii integer value
        self._ascii_arr = []

    @property
    def word(self):
        return self._word

    @property
    def ascii_arr(self):
        return self._ascii_arr

    def get_input(self):
        """
        Gets input from standard in and returns after the 'enter' key press, just like Python's standard input()
        function

        :return: A string of the input characters from standard in
        """
        while True:
            ch = get_char()
            i = ord(ch)
            self._ascii_arr.append(i)
            print(ch, end='', flush=True)
            if i == 10:
                # enter
                break
            elif i == 27:
                # escape character
                self._word += '\x1b'
            elif 32 <= i <= 126:
                # printable ascii characters
                self._word += ch
            elif i == 127:
                # backspace
                self._word = self._word[:-1]
                print('\b \b', end='', flush=True)

        return self._word


def controls():
    ascii_arr = []
    while True:
        ch = get_char()
        i = ord(ch)
        ascii_arr.append(i)
        ascii_arr = ascii_arr[-4:]
        if i == 10:
            yield Keys.ENTER
        elif i == 32:
            yield Keys.SPACE
        elif i == 127:
            yield Keys.BACKSPACE
        elif ascii_arr[-3:] == UP:
            yield Keys.W
        elif ascii_arr[-3:] == DOWN:
            yield Keys.S
        elif ascii_arr[-3:] == LEFT:
            yield Keys.A
        elif ascii_arr[-3:] == RIGHT:
            yield Keys.D
        elif ascii_arr == DELETE_SEQ:
            yield Keys.DELETE
        elif 33 <= i <= 126:
            # printable characters
            yield ch
