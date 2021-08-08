"""
Minesweeper game

Logic/data structures for the minesweeper game
"""
import numpy as np
import os

# minesweeper game statuses
LOST = 'lost'
WON = 'won'
IN_PROGRESS = 'in_progress'


class Minesweeper:
    # default board size and number of mines for minesweeper
    DEFAULT_SIZE = 10
    DEFAULT_MINES = 10

    # coordinate offsets to represent the neighbors of a square where the upper left of the board is (0, 0)
    _OFFSETS = [
        (1, 1),     # SE
        (1, 0),     # E
        (1, -1),    # NE
        (0, 1),     # S
        (0, -1),    # N
        (-1, 1),    # SW
        (-1, 0),    # W
        (-1, -1)    # NW
    ]

    # unicode characters
    _SQUARE = u'\u25a0'
    _FLAG = u'\u2691'

    def __init__(self, size=DEFAULT_SIZE, mines=DEFAULT_MINES, indent=None):
        """
        Initializes an instance of the Minesweeper game

        :param size: The horizontal and vertical length of the board to create
        :param mines: The number of mines that should be present on the board
        :param indent: The number of spaces to indent the board on the left size. If None, will auto center the board
            in the terminal
        """
        # the board size
        self._size = size

        # the real mine count and player's marked mine count
        self._mine_count = mines
        self._player_mine_count = 0

        # the number of spaces to indent
        if isinstance(indent, int):
            self._indent = indent
        else:
            # auto centers board in terminal
            term_size = os.get_terminal_size()
            self._indent = term_size.columns // 2 - size

        # True for the player's first move
        self._first_move = True

        # stores the game status
        self._status = IN_PROGRESS

        # holds the game board data and if it is visible or not
        self._board = np.zeros(shape=(self.size, self.size))
        self._visible = np.zeros(shape=(self.size, self.size))

    @property
    def size(self):
        """
        Gets the size of the board

        :return: The size of the board
        """
        return self._size

    @property
    def mines(self):
        """
        Gets the number of mines that have been marked by the player

        :return: the number of mines that have been marked by the player
        """
        return self._player_mine_count

    @property
    def indent(self):
        """
        Gets the number of spaces to indent on the left side of the board

        :return: the number of spaces to indent on the left side of the board
        """
        return self._indent

    def _generate_board(self, x, y):
        """
        Generates the board data and ensures that the player will never lose on the first move

        :param x: x coordinate point of the first move
        :param y: y coordinate point of the first move
        """
        value = (x * self.size) + y

        while True:
            # random values to set as the mines on the board
            mines_nums = np.random.default_rng().choice(self.size * self.size, size=self._mine_count, replace=False)
            if value not in mines_nums:
                break

        # builds the board
        for num in mines_nums:
            i, j = divmod(num, self.size)
            self._board[i, j] = -1
            self._find_neighbors(self._update_board, i, j)

    def _is_valid_point(self, x, y):
        """
        Checks if a coordinate point is on the board

        :param x: x coordinate point
        :param y: y coordinate point
        :return: True if the coordinate point are is valid; otherwise, False
        """
        return 0 <= x < self.size and 0 <= y < self.size

    def _find_neighbors(self, fn, x, y, *args, **kwargs):
        """
        Calls a function for all neighboring squares

        :param fn: Function to call that accepts x and y arguments followed by any number of args and kwargs
        :param x: x coordinate point
        :param y: y coordinate point
        :param args: args
        :param kwargs: kwargs
        """
        for i, j in self._OFFSETS:
            fn(x + i, y + j, *args, **kwargs)

    def _count_neighboring_flags(self, x, y):
        """
        Finds the number of mines that the user has marked that are adjacent to the current square

        :param x: x coordinate point
        :param y: y coordinate point
        :return: the number of mines that the user has marked that are adjacent to the current square
        """
        count = 0
        for i, j in self._OFFSETS:
            if self._is_valid_point(x + i, y + j) and self._visible[x + i, y + j] == 2:
                count += 1

        return count

    def _update_board(self, x, y):
        """
        Upon creation of the game board, updates the

        :param x: x coordinate point
        :param y: y coordinate point
        """
        if self._is_valid_point(x, y) and self._board[x, y] != -1:
            self._board[x, y] += 1

    def _make_visible(self, x, y, level=0):
        """
        Recursively uncovers a square

        :param x: x coordinate point
        :param y: y coordinate point
        :param level: 0 is default, -1 for recursively searching hidden or question mark status, 1 for recursively
            searching neighbors if the current position is already visible
        """
        if self._is_valid_point(x, y):
            if self._visible[x, y] in {0, 3}:
                self._visible[x, y] = 1
                if self._board[x, y] == 0:
                    self._find_neighbors(self._make_visible, x, y, level=-1)
            elif level == 0 and self._visible[x, y] == 1 and self._board[x, y] == self._count_neighboring_flags(x, y):
                self._find_neighbors(self._make_visible, x, y, level=1)
            elif level == 1 and self._visible[x, y] in {0, 3}:
                self._visible[x, y] = 1

    def _check_game_status(self):
        """
        Checks the status of the game

        :return: Returns a string representing if the game is 'in_progress', 'lost', or 'won' after this move
        """
        is_in_progress = False
        for i, j in np.ndindex(*self._visible.shape):
            if self._visible[i, j] == 1 and self._board[i, j] == -1:
                return LOST
            elif self._visible[i, j] != 1 and self._board[i, j] != -1:
                is_in_progress = True

        if is_in_progress:
            return IN_PROGRESS

        return WON

    def uncover_square(self, x, y):
        """
        Uncover a square. And recursively uncover adjacent squares. Game over if you uncovered a mine, game won if you
        uncovered all of the safe squares, and game continues otherwise

        :param x: x coordinate point
        :param y: y coordinate point
        :return: Returns a string representing if the game is 'in_progress', 'lost', or 'won' after this move
        """
        if self._first_move:
            self._generate_board(x, y)
            self._first_move = False

        if 2 <= self._visible[x, y] < 3:
            # status is already in progress. Or in other words, it cannot be in progress after the game is over
            pass
        elif self._board[x, y] == -1:
            self._status = LOST
        else:
            self._make_visible(x, y)
            self._status = self._check_game_status()

        return self._status

    def mark_square(self, x, y):
        """
        Changes a square's status from hidden to a flag, from a flag to a question mark, and from a question mark to
        hidden again

        :param x: x coordinate point
        :param y: y coordinate point
        """
        if self._visible[x, y] == 0:
            # convert from hidden to flag
            self._visible[x, y] = 2
            self._player_mine_count += 1
        elif self._visible[x, y] == 2:
            # convert from flag to question mark
            self._visible[x, y] = 3
            self._player_mine_count -= 1
        elif self._visible[x, y] == 3:
            # convert from question mark to hidden
            self._visible[x, y] = 0

    def _convert_board_to_char(self, v):
        if v == 0:
            # square if hidden
            return self._SQUARE
        elif v == -1:
            # asterisk if mine
            return '*'
        else:
            # number of neighboring mines otherwise
            return str(int(v))

    def _board_iterator(self, fn):
        """
        Iterates over the board to create nicely formatted output string with spaces between each column and new lines
        after each row except for the last one.

        :param fn: the function to call that returns a single character based off of the x and y coordinates of the
            board
        :return: A string representing the board
        """
        str_to_write = ''
        for j in range(self.size):
            str_to_write += ' ' * self.indent
            for i in range(self.size):
                str_to_write += fn(i, j)

                if i + 1 != self.size:
                    str_to_write += ' '

            if j + 1 != self.size:
                str_to_write += '\n'

        return str_to_write

    def create_board(self):
        """
        Creates a formatted board for the game in progress state. All uncovered squares, flags, and question marks are
        displayed. Everything else remains hidden.

        :return: A string representing the board
        """
        def in_progress(i, j):
            if self._visible[i, j] == 1:
                return self._convert_board_to_char(self._board[i, j])
            elif self._visible[i, j] == 2:
                return self._FLAG
            elif self._visible[i, j] == 3:
                return '?'
            else:
                return '-'

        return self._board_iterator(in_progress)

    def create_game_over_board(self):
        """
        Creates a formatted board for the game over state. All uncovered squares, mines, flags, and question marks are
        displayed. Hidden squares where none of the previously mentioned are true remain hidden. Additionally, incorrect
        flag are marked with an 'X'.

        :return: A string representing the board
        """
        def game_over(i, j):
            if self._visible[i, j] == 2:
                if self._board[i, j] == -1:
                    return self._FLAG
                else:
                    return 'X'
            elif self._visible[i, j] == 1 or self._board[i, j] == -1:
                return self._convert_board_to_char(self._board[i, j])
            elif self._visible[i, j] == 3:
                return '?'
            else:
                return '-'

        return self._board_iterator(game_over)

    def create_show_all_board(self):
        """
        Creates a formatted board with all of the numbers, mines, and blank squares visible.

        :return: A string representing the board
        """
        def show_all(i, j):
            return self._convert_board_to_char(self._board[i, j])

        return self._board_iterator(show_all)

    def __str__(self):
        """
        Creates a formatted board based on the game status

        :return: A string representing the board
        """
        if self._status == IN_PROGRESS:
            return self.create_board()
        else:
            return self.create_game_over_board()
