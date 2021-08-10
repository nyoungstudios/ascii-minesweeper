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

    # option menu options
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

    _DEFAULT_DIFFICULTY = 'Easy'
    _DEFAULT_MODE = 'Normal'
    _DEFAULT_HEIGHT = 26

    def __init__(self):
        term_size = os.get_terminal_size()
        self._center = term_size.columns // 2

        def build_centered_header_text():
            """
            Builds a centered Minesweeper ASCII art header text

            :return: a tuple of the string to write and the number of vertical lines it takes up
            """
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
            """
            Builds the help text to be shown on the help screen

            :return: a tuple of the string to write and the number of vertical lines it takes up
            """
            str_to_write = ''
            line_count = 0
            for line in HELP_SCREEN:
                line_count += 1
                str_to_write += line + '\n'

            return str_to_write, line_count

        # defines the constants for the height of the screen of the various pages

        # gets the length of the number of arguments on the selector pages
        self._MENU_LENGTH = len(self.MENU)
        self._OPTIONS_LENGTH = len(self.OPTIONS)

        # builds string constants
        self._CENTERED_HEADER_TXT, self._HEADER_HEIGHT = build_centered_header_text()
        self._HELP_TXT, self._HELP_HEIGHT = build_help_text()

        # sets height of screen with additional spaces taken into account
        self._MENU_HEIGHT = self._MENU_LENGTH + 1
        self._OPTIONS_HEIGHT = self._OPTIONS_LENGTH + 7

        # the sum of the height of the header, default board size, menu height and an additional empty line
        self._HOMEPAGE_HEIGHT = self._HEADER_HEIGHT + Minesweeper.DEFAULT_SIZE + self._MENU_HEIGHT + 1

        # stores the height of the board on the game screen
        self._BOARD_HEIGHT = 0

        # stores the string to indent the header on the game screen
        self._header_indent = ''

        # values to store position of cursor
        self._x = 0
        self._y = 0
        self._menu_pos = 0
        self._options_pos = 0
        self._custom_pos = 0

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

    def _create_label(self, label, offset=6):
        """
        Helper function to create a formatted string for a label text for option/menu screens with an additional
        newline afterwards

        :param label: the label name
        :param offset: the number of characters to the left to offset from center
        :return: a formatted string
        """
        return ' ' * (self._center - offset) + label + '\n\n'

    def _add_right_arrow(self, pos, length, index):
        """
        Helper function to write the right arrow selector based off of the current position, number of options, and the
        index.

        :param pos: current position of the selected menu option
        :param length: the number of menu options
        :param index: the current index as you iterate over the menu options
        :return: a string with a right arrow and a space if the position matches the index; otherwise, two spaces
        """
        if pos % length == index:
            return self._RIGHT_ARROW + ' '
        else:
            return ' ' * 2

    def launch_game(self):
        """
        The main function to start and run the game. This is the game's homepage
        """
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
                str_to_write += ' ' * (self._center - 4)
                str_to_write += self._add_right_arrow(self._menu_pos, self._MENU_LENGTH, i)
                str_to_write += v + '\n'

            print(str_to_write)

        def control_map(key):
            self._menu_pos %= self._MENU_LENGTH
            if key == Keys.W:
                self._menu_pos -= 1
                clear_last_lines(self._MENU_HEIGHT)
                refresh_screen()
            elif key == Keys.S:
                self._menu_pos += 1
                clear_last_lines(self._MENU_HEIGHT)
                refresh_screen()
            elif key == Keys.ENTER:
                if self._menu_pos == 0:
                    # Play
                    clear_last_lines(self._HOMEPAGE_HEIGHT)
                    self.play_game()
                    clear_last_lines(self._BOARD_HEIGHT)
                    refresh_screen(status=START)
                elif self._menu_pos == 1:
                    # Options
                    clear_last_lines(self._HOMEPAGE_HEIGHT - self._HEADER_HEIGHT)
                    self.open_options_screen()
                    clear_last_lines(self._OPTIONS_HEIGHT)
                    refresh_screen(status=BODY)
                elif self._menu_pos == 2:
                    # Help
                    clear_last_lines(self._HOMEPAGE_HEIGHT)
                    self.open_help_screen()
                    clear_last_lines(self._HELP_HEIGHT + 4)
                    refresh_screen(status=START)
                else:
                    # Exit
                    return self._break()
            elif key == Keys.BACKSPACE:
                # Exit
                return self._break()

        # prints initial screen
        refresh_screen(status=START)
        # listen on keyboard input
        self._on_key_input(control_map)

    def open_options_screen(self):
        """
        Opens and runs the option screen
        """
        # resets option position to difficulty index
        self._options_pos = self.OPTIONS.index(self._difficulty)

        def create_screen():
            str_to_write = ''
            for i, v in enumerate(self.OPTIONS):
                if v == self._DEFAULT_MODE:
                    str_to_write += '\n' + self._create_label('Modes:')
                elif i == self._OPTIONS_LENGTH - 1:
                    str_to_write += '\n'

                str_to_write += ' ' * (self._center - 6)
                str_to_write += self._add_right_arrow(self._options_pos, self._OPTIONS_LENGTH, i)

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

        # builds and prints initial screen
        screen_body = self._create_label('Difficulty:')
        screen_body += create_screen()
        print(screen_body)

        # listen on keyboard input
        self._on_key_input(control_map)

    def open_help_screen(self):
        """
        Opens help screen
        """
        print(self._HELP_TXT)
        self._on_key_input()

    def play_game(self):
        # sets game options based off of difficulty level and mode selected
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

        # creates an instance of the game
        game = Minesweeper(**opts)
        # calculates the number of new lines that need to be prepended to properly center the board
        num_prepend_lines = self._DEFAULT_HEIGHT // 2 - game.height // 2
        self._BOARD_HEIGHT = num_prepend_lines + game.height + 2

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
            cursor_down(game.height - self._y + 2)
            cursor_left(game.indent + (self._x * 2))

        def cursor_reset_original():
            """
            Moves cursor it's original location after refreshing the board or the top left of the board on start
            """
            cursor_right(game.indent + (self._x * 2))
            cursor_up(game.height - self._y + 2)

        def format_header():
            """
            Formats game info header

            :return: a formatted string with the game info
            """
            moves_str = str(game.moves)
            moves_ch_len = len(moves_str)
            header_str = 'Moves: {}'.format(game.moves) + ' ' * (11 - moves_ch_len)  + \
                         'Mines: {}/{}'.format(game.mines, opts['mines'])
            if not self._header_indent:
                self._header_indent = ' ' * (self._center - len(header_str) // 2)
            return self._header_indent + header_str

        def build_game_screen(msg=None):
            """
            Builds the text to write for the game screen. Includes header/footer text as well as text for the game board

            :param msg: Message to add to the header (should be used for displaying game over information)
            :return: a formatted string to write
            """
            str_to_write = '\n' + format_header() + '\n\n'
            remainder_lines = num_prepend_lines - 3
            if msg:
                str_to_write += self._header_indent + msg + '\n' + \
                                self._header_indent + 'Time elapsed: {:.2f} seconds'.format(game.time)
                remainder_lines -= 1

            str_to_write += '\n' * remainder_lines + str(game) + '\n\n'

            if msg:
                str_to_write += self._header_indent + 'Press any key to exit.'

            return str_to_write

        def refresh_board(**kwargs):
            """
            Reprints the board in the same location in standard out so that it looks like the board was updated in place
            """
            cursor_bottom_left()
            clear_last_lines(self._BOARD_HEIGHT)
            print(build_game_screen(**kwargs))
            cursor_reset_original()

        def control_map(key):
            if not game:
                # if the game is over, wait on any key press to exit
                cursor_bottom_left()
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
                msg = ''
                if result == LOST:
                    msg = 'You lost! Game over :('
                elif result == WON:
                    msg = 'Congratulations, you won! :)'
                refresh_board(msg=msg)
            elif key == Keys.SPACE:
                game.mark_square(self._x, self._y)
                refresh_board()
            elif key == Keys.BACKSPACE:
                cursor_bottom_left()
                return self._break()

        def on_interrupt():
            cursor_bottom_left()

        # print initial board
        print(build_game_screen())

        # moves cursor to top left of board
        cursor_reset_original()

        # listen on keyboard input
        self._on_key_input(control_map, on_interrupt)


def main():
    play = PlayMinesweeper()
    play.launch_game()
    
if __name__ == '__main__':
    main()
