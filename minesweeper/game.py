"""
Minesweeper game

Logic/data structures for the minesweeper game
"""
import numpy as np
import time

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

    # visible states
    _MARK_HIDDEN = 0
    _MARK_VISIBLE = 1
    _MARK_FLAG = 2
    _MARK_QUESTION_MARK = 3

    def __init__(
        self,
        height: int = DEFAULT_SIZE,
        width: int = DEFAULT_SIZE,
        size: int = None,
        mines: int = DEFAULT_MINES,
        indent: int = 0
    ):
        """
        Initializes an instance of the Minesweeper game

        :param height: The vertical length of the board to create
        :param width: The horizontal length of the board to create
        :param size: The horizontal and vertical length of the board to create. If this is provided, it will override
            height and width values
        :param mines: The number of mines that should be present on the board
        :param indent: The number of spaces to indent the board on the left size
        """
        # the board size
        if size:
            self._height = size
            self._width = size
        else:
            self._height = height
            self._width = width

        # the real mine count and player's marked mine count
        self._mine_count = mines
        self._player_mine_count = 0

        # the number of spaces to indent
        self._indent = indent

        # stores the game status
        self._status = IN_PROGRESS
        self._moves = 0
        self._start_time = 0
        self._time_elapsed = 0

        # stores the game data
        # -1 for a mine; otherwise the numerical count of the number of neighboring mines
        self._board = np.zeros(shape=(self.width, self.height))
        # 0 for hidden, 1 for visible, 2 for flag, 3 for question mark
        self._visible = np.zeros(shape=(self.width, self.height))

        # stores which indices have already been searched when recursively finding squares to recover
        self._already_searched = None

    @property
    def height(self):
        """
        Gets the height of the board

        :return: The height of the board
        """
        return self._height

    @property
    def width(self):
        """
        Gets the width of the board

        :return: The width of the board
        """
        return self._width

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

    @property
    def moves(self):
        """
        Gets the total number of moves made in the game. If the squares are recursively uncovered, that only counts as
        one move. Putting marking a square as a flag or question mark does not count as a move

        :return: the total number of moves made in the game
        """
        return self._moves

    @property
    def time(self):
        """
        Get the total elapsed time of the game. If the game is in progress, calculate the elapsed time; otherwise,
        return the calculated time from when the game ended

        :return: the total elapsed time of the game
        """
        if self:
            return time.time() - self._start_time
        else:
            return self._time_elapsed

    def _is_valid_point(self, x, y):
        """
        Checks if a coordinate point is on the board

        :param x: x coordinate point
        :param y: y coordinate point
        :return: True if the coordinate point are is valid; otherwise, False
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def _call_neighbors(self, fn, x, y, check_searched=False, *args, **kwargs):
        """
        Calls a function for all valid neighboring squares

        :param fn: Function to call that accepts x and y arguments followed by any number of args and kwargs
        :param x: x coordinate point
        :param y: y coordinate point
        :param check_searched: if True, will check if a square has already been called by the recursive search rather
            than calling the function again
        :param args: args
        :param kwargs: kwargs
        :return: the logical or of all of the return values from the functions called
        """
        out = None
        for i, j in self._OFFSETS:
            if self._is_valid_point(x + i, y + j):
                if not check_searched or (self._already_searched is not None and self._already_searched[x + i, y + j] == 0):
                    v = fn(x + i, y + j, *args, **kwargs)
                    out = out or v

        return out

    def _update_board(self, x, y):
        """
        Upon creation of the game board, updates the board with the mine count from the neighboring squares

        :param x: x coordinate point
        :param y: y coordinate point
        """
        if self._board[x, y] != -1:
            self._board[x, y] += 1

    def _generate_board(self, x, y):
        """
        Generates the board data and ensures that the player will never lose on the first move

        :param x: x coordinate point of the first move
        :param y: y coordinate point of the first move
        """
        value = (x * self.height) + y

        while True:
            # random values to set as the mines on the board
            mines_nums = np.random.default_rng().choice(self.width * self.height, size=self._mine_count, replace=False)
            if value not in mines_nums:
                break

        # builds the board
        for num in mines_nums:
            i, j = divmod(num, self.height)
            self._board[i, j] = -1
            self._call_neighbors(self._update_board, i, j)

    def _count_neighboring_flags(self, x, y):
        """
        Finds the number of mines that the user has marked that are adjacent to the current square

        :param x: x coordinate point
        :param y: y coordinate point
        :return: the number of mines that the user has marked that are adjacent to the current square
        """
        count = 0
        for i, j in self._OFFSETS:
            if self._is_valid_point(x + i, y + j) and self._visible[x + i, y + j] == self._MARK_FLAG:
                count += 1

        return count

    def _make_visible(self, x, y, level=0):
        """
        Recursively uncovers a square

        :param x: x coordinate point
        :param y: y coordinate point
        :param level: 0 is default, -1 for recursively searching hidden or question mark status, 1 for recursively
            searching neighbors if the current position is already visible
        :return: True if at least one square was uncovered; otherwise, False
        """
        self._already_searched[x, y] = 1
        if self._visible[x, y] in {self._MARK_HIDDEN, self._MARK_QUESTION_MARK}:
            self._visible[x, y] = self._MARK_VISIBLE
            if self._board[x, y] == 0:
                self._call_neighbors(self._make_visible, x, y, check_searched=True, level=-1)
            return True
        elif level == 0 and self._visible[x, y] == self._MARK_VISIBLE and self._board[x, y] == self._count_neighboring_flags(x, y):
            return self._call_neighbors(self._make_visible, x, y, check_searched=True, level=1) or False
        elif level == 1 and self._visible[x, y] in {self._MARK_HIDDEN, self._MARK_QUESTION_MARK}:
            self._visible[x, y] = self._MARK_VISIBLE
            return True

        return False

    def _check_game_status(self):
        """
        Checks the status of the game

        :return: a string representing if the game is 'in_progress', 'lost', or 'won' after this move
        """
        is_in_progress = False
        for i, j in np.ndindex(*self._visible.shape):
            if self._visible[i, j] == self._MARK_VISIBLE and self._board[i, j] == -1:
                return LOST
            elif self._visible[i, j] != self._MARK_VISIBLE and self._board[i, j] != -1:
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
        :return: a string representing if the game is 'in_progress', 'lost', or 'won' after this move
        """
        if self.moves == 0:
            self._start_time = time.time()
            self._generate_board(x, y)

        if self._visible[x, y] == self._MARK_FLAG:
            # if square is a flag, no game status or squares to update
            pass
        elif self._board[x, y] == -1:
            self._status = LOST
            self._moves += 1
        else:
            self._already_searched = np.zeros(shape=(self.width, self.height))
            uncovered_square = self._make_visible(x, y)
            if uncovered_square:
                self._moves += 1
            self._status = self._check_game_status()

        if not self:
            self._time_elapsed = time.time() - self._start_time

        return self._status

    def mark_square(self, x, y):
        """
        Changes a square's status from hidden to a flag, from a flag to a question mark, and from a question mark to
        hidden again

        :param x: x coordinate point
        :param y: y coordinate point
        """
        if self._visible[x, y] == self._MARK_HIDDEN:
            # convert from hidden to flag
            self._visible[x, y] = self._MARK_FLAG
            self._player_mine_count += 1
        elif self._visible[x, y] == self._MARK_FLAG:
            # convert from flag to question mark
            self._visible[x, y] = self._MARK_QUESTION_MARK
            self._player_mine_count -= 1
        elif self._visible[x, y] == self._MARK_QUESTION_MARK:
            # convert from question mark to hidden
            self._visible[x, y] = self._MARK_HIDDEN

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
        for j in range(self.height):
            str_to_write += ' ' * self.indent
            for i in range(self.width):
                str_to_write += fn(i, j)

                if i + 1 != self.width:
                    str_to_write += ' '

            if j + 1 != self.height:
                str_to_write += '\n'

        return str_to_write

    def create_board(self):
        """
        Creates a formatted board for the game in progress state. All uncovered squares, flags, and question marks are
        displayed. Everything else remains hidden.

        :return: A string representing the board
        """
        def in_progress(i, j):
            if self._visible[i, j] == self._MARK_VISIBLE:
                return self._convert_board_to_char(self._board[i, j])
            elif self._visible[i, j] == self._MARK_FLAG:
                return self._FLAG
            elif self._visible[i, j] == self._MARK_QUESTION_MARK:
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
            if self._visible[i, j] == self._MARK_FLAG:
                if self._board[i, j] == -1:
                    return self._FLAG
                else:
                    return 'X'
            elif self._visible[i, j] == self._MARK_VISIBLE or self._board[i, j] == -1:
                return self._convert_board_to_char(self._board[i, j])
            elif self._visible[i, j] == self._MARK_QUESTION_MARK:
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

    def __bool__(self):
        """
        Checks if the game is in progress or is over

        :return: True if the game is still in progress, False if the game is over
        """
        return self._status == IN_PROGRESS

    def __str__(self):
        """
        Creates a formatted board based on the game status

        :return: A string representing the board
        """
        if self:
            return self.create_board()
        else:
            return self.create_game_over_board()
