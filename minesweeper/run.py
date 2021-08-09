"""
Runs interactive minesweeper game in standard out
"""
import copy
import os

from minesweeper.cursor import *
from minesweeper.game import Minesweeper, WON, LOST
from minesweeper.read import controls, Keys
from minesweeper._text import *


class PlayMinesweeper:
    # unicode constants
    _RIGHT_ARROW = u'\u25b6'
    _OPEN_CIRCLE = u'\u25ef'
    _SOLID_CIRCLE = u'\u25cf'

    # main menu options
    MENU = (
        'Play',
        'Options',
        'Help',
        'Exit'
    )

    OPTIONS = (
        'Easy',
        'Medium',
        'Hard',
        'Custom',
        'Normal',
        'Double Wide',
        'Triple Wide',
        'Back'
    )

    _MENU_LENGTH = len(MENU)
    _OPTIONS_LENGTH = len(OPTIONS)

    _MENU_HEIGHT = _MENU_LENGTH
    _OPTIONS_HEIGHT = _OPTIONS_LENGTH

    _DEFAULT_DIFFICULTY = 'Easy'
    _DEFAULT_MODE = 'Normal'
    _DEFAULT_HEIGHT = 26

    def __init__(self):
        term_size = os.get_terminal_size()
        self._center = term_size.columns // 2

        def build_centered_header_text():
            # adds an extra new line to the start of the header text
            str_to_write = '\n'
            line_count = 1
            lines = HEADER_TEXT.split('\n')
            indent = self._center - (len(lines[0]) // 2)
            for line in lines:
                line_count += 1
                str_to_write += ' ' * indent + line + '\n'

            # adds an extra new line to the end of the header text
            str_to_write += '\n'
            line_count += 1

            return str_to_write, line_count

        def build_help_text():
            str_to_write = ''
            line_count = 0
            for line in HELP_SCREEN:
                line_count += 1
                str_to_write += line + '\n'

            return str_to_write, line_count

        self._HELP_TXT, self._HELP_HEIGHT = build_help_text()

        self._CENTERED_HEADER_TXT, self._HEADER_HEIGHT = build_centered_header_text()

        # the sum of the height of the header, default board size, menu height and two additional empty lines
        self._HOMEPAGE_HEIGHT = self._HEADER_HEIGHT + Minesweeper.DEFAULT_SIZE + self._MENU_HEIGHT + 2

        # stores the height of the board
        self._board_height = 0

        # values to store position of cursor
        self._x = 0
        self._y = 0
        self._menu_pos = 0
        self._options_pos = 0

        # options to launch the game with
        self._difficulty = self._DEFAULT_DIFFICULTY
        self._mode = self._DEFAULT_MODE
        self._game_options = {
            'Easy': {'size': 10, 'mines': 10},
            'Medium': {'size': 12, 'mines': 25},
            'Hard': {'size': 15, 'mines': 45}
        }

        # sets board indent
        for level, opt in self._game_options.items():
            width = opt.get('size') or opt.get('width')
            opt['indent'] = self._center - width

        # example board for home screen
        self._game_example = str(Minesweeper(**self._game_options[self._DEFAULT_DIFFICULTY]))

    @staticmethod
    def _break():
        return True

    @staticmethod
    def _on_key_input(fn=None, interrupt_fn=None):
        """
        Function wrapper for keyboard input

        :param fn: Function to call on keyboard input. Must have one positional argument. If this function returns True,
            it will break the keyboard input loop and exit. If no provided, will return on any key press
        :param interrupt_fn: Function to call on keyboard interrupt (CTRL-C)
        """
        try:
            for key in controls():
                if fn:
                    out = fn(key)
                    if out:
                        break
                else:
                    break
        except KeyboardInterrupt:
            # caught exception if CTRL-C is called
            if interrupt_fn:
                interrupt_fn()

    def launch_game(self):
        START = 1
        BODY = 2
        MENU = 3

        def refresh_screen(status=MENU):
            str_to_write = ''

            if status == START or status == BODY:
                if status == START:
                    str_to_write += self._CENTERED_HEADER_TXT

                str_to_write += self._game_example + '\n\n'

            for i, v in enumerate(self.MENU):
                str_to_write += ' ' * (self._center - 6)
                if self._menu_pos % self._MENU_LENGTH == i:
                    str_to_write += self._RIGHT_ARROW + ' '
                else:
                    str_to_write += ' ' * 2

                str_to_write += v + '\n'

            print(str_to_write)

        def control_map(key):
            self._menu_pos %= self._MENU_LENGTH
            if key == Keys.W:
                self._menu_pos -= 1
                clear_last_lines(self._MENU_HEIGHT + 1)
                refresh_screen()
            elif key == Keys.S:
                self._menu_pos += 1
                clear_last_lines(self._MENU_HEIGHT + 1)
                refresh_screen()
            elif key == Keys.ENTER:
                if self._menu_pos == 0:
                    # Play
                    clear_last_lines(self._HOMEPAGE_HEIGHT)
                    self.play_game()
                    clear_last_lines(self._board_height)
                    refresh_screen(status=START)
                elif self._menu_pos == 1:
                    # Options
                    clear_last_lines(self._HOMEPAGE_HEIGHT - self._HEADER_HEIGHT)
                    self.open_options_screen()
                    clear_last_lines(self._OPTIONS_HEIGHT + 7)
                    refresh_screen(status=BODY)
                elif self._menu_pos == 2:
                    # Help
                    clear_last_lines(self._HOMEPAGE_HEIGHT)
                    self.open_help_screen()
                    clear_last_lines(self._HELP_HEIGHT + 2)
                    refresh_screen(status=START)
                else:
                    # Exit
                    return self._break()
            elif key == Keys.BACKSPACE:
                # Exit
                return self._break()

        refresh_screen(status=START)
        self._on_key_input(control_map)

    def open_options_screen(self):
        def create_label(text):
            return ' ' * (self._center - 6) + text + '\n\n'

        def create_screen():
            str_to_write = ''
            for i, v in enumerate(self.OPTIONS):
                if v == self._DEFAULT_MODE:
                    str_to_write += '\n' + create_label('Modes:')
                elif i == self._OPTIONS_LENGTH - 1:
                    str_to_write += '\n'

                str_to_write += ' ' * (self._center - 6)
                if self._options_pos % self._OPTIONS_LENGTH == i:
                    str_to_write += self._RIGHT_ARROW + ' '
                else:
                    str_to_write += ' ' * 2

                if i != self._OPTIONS_LENGTH - 1:
                    if v == self._difficulty or v == self._mode:
                        str_to_write += self._SOLID_CIRCLE + ' '
                    else:
                        str_to_write += self._OPEN_CIRCLE + ' '
                else:
                    str_to_write += ' ' * 2

                str_to_write += v + '\n'

            return str_to_write

        def control_map(key):
            self._options_pos %= self._OPTIONS_LENGTH
            if key == Keys.W:
                self._options_pos -= 1
            elif key == Keys.S:
                self._options_pos += 1
            elif key == Keys.ENTER:
                if 0 <= self._options_pos <= 3:
                    # Easy, Medium, Hard, and Custom
                    self._difficulty = self.OPTIONS[self._options_pos]

                    if self._options_pos == 3:
                        pass
                        # call custom screen
                elif 4 <= self._options_pos <= 6:
                    # Normal, Double Wide, Triple Wide
                    self._mode = self.OPTIONS[self._options_pos]
                else:
                    # Exit
                    return self._break()
            elif key == Keys.BACKSPACE:
                # Exit
                return self._break()

            clear_last_lines(self._OPTIONS_LENGTH + 5)
            print(create_screen())

        screen_body = create_label('Difficulty:')
        screen_body += create_screen()
        print(screen_body)
        self._on_key_input(control_map)

    def open_help_screen(self):
        print(self._HELP_TXT, end='')
        self._on_key_input()

    def play_game(self):
        # creates an instance of the game and prints the board
        opts = self._game_options[self._difficulty]
        if self._mode != self._DEFAULT_MODE:
            opts = copy.copy(opts)
            h = opts.pop('size')
            opts['height'] = h
            if self._mode == 'Double Wide':
                opts['width'] = 2 * h
                opts['mines'] *= 2
            else:
                opts['width'] = 3 * h
                opts['mines'] *= 3

            opts['indent'] = self._center - opts['width']

        game = Minesweeper(**opts)
        num_prepend_lines = self._DEFAULT_HEIGHT // 2 - game.height // 2
        board_str = '\n' * num_prepend_lines + str(game)
        self._board_height = num_prepend_lines + game.height + 1
        print(board_str)

        # keeps track of the coordinate points of the cursor on the board
        self._x = 0
        self._y = 0

        def is_valid_cursor(i=0, j=0):
            """
            Tests if a cursor move is valid

            :param i: offset in the x direction
            :param j: offset in the y direction
            :return: True if the offset is a valid cursor move; otherwise, False
            """
            return 0 <= self._x + i < game.width and 0 <= self._y + j < game.height

        def cursor_bottom_left():
            """
            Moves cursor to bottom left of the board
            """
            cursor_down(game.height - self._y)
            cursor_left(game.indent + (self._x * 2))

        def cursor_reset_original():
            """
            Moves cursor it's original location after refreshing the board or the top left of the board on start
            """
            cursor_right(game.indent + (self._x * 2))
            cursor_up(game.height - self._y)

        def refresh_board():
            """
            Reprints the board in the same location in standard out so that it looks like the board was updated in place
            """
            cursor_bottom_left()
            clear_last_lines(game.height)
            print(game)
            cursor_reset_original()

        def control_map(key):
            if not game:
                return self._break()
            elif key == Keys.W:
                if is_valid_cursor(j=-1):
                    cursor_up(1)
                    self._y -= 1
            elif key == Keys.A:
                if is_valid_cursor(i=-1):
                    cursor_left(2)
                    self._x -= 1
            elif key == Keys.S:
                if is_valid_cursor(j=1):
                    cursor_down(1)
                    self._y += 1
            elif key == Keys.D:
                if is_valid_cursor(i=1):
                    cursor_right(2)
                    self._x += 1
            elif key == Keys.ENTER:
                result = game.uncover_square(self._x, self._y)
                refresh_board()
                if result == LOST:
                    cursor_bottom_left()
                    print('You lost! Game over :(')
                elif result == WON:
                    cursor_bottom_left()
                    print('Congratulations, you won! :)')
            elif key == Keys.SPACE:
                game.mark_square(self._x, self._y)
                refresh_board()
            elif key == Keys.BACKSPACE:
                cursor_bottom_left()
                print('Exiting minesweeper.')
                return self._break()

        def on_interrupt():
            cursor_bottom_left()
            print()

        # moves cursor to top left of board
        cursor_reset_original()

        self._on_key_input(control_map, on_interrupt)


def main():
    play = PlayMinesweeper()
    play.launch_game()
    
if __name__ == '__main__':
    main()
