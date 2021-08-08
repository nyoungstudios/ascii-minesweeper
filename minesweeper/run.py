"""
Runs interactive minesweeper game in standard out
"""
from minesweeper.cursor import *
from minesweeper.game import Minesweeper, WON, LOST
from minesweeper.read import controls, Keys


def main():
    # creates an instance of the game and prints the board
    game = Minesweeper()
    print(game)

    # keeps track of the coordinate points of the cursor on the board
    x = 0
    y = 0

    def is_valid_cursor(i=0, j=0):
        """
        Tests if a cursor move is valid

        :param i: offset in the x direction
        :param j: offset in the y direction
        :return: True if the offset is a valid cursor move; otherwise, False
        """
        return 0 <= x + i < game.size and 0 <= y + j < game.size

    def cursor_bottom_left():
        """
        Moves cursor to bottom left of the board
        """
        cursor_down(game.size - y)
        cursor_left(game.indent + (x * 2))

    def cursor_reset_original():
        """
        Moves cursor it's original location after refreshing the board or the top left of the board on start
        """
        cursor_right(game.indent + (x * 2))
        cursor_up(game.size - y)

    def refresh_board():
        """
        Reprints the board in the same location in standard out so that it looks like the board was updated in place
        """
        cursor_bottom_left()
        clear_last_lines(game.size)
        print(game)
        cursor_reset_original()

    # moves cursor to top left of board
    cursor_reset_original()

    try:
        for key in controls():
            if key == Keys.W:
                if is_valid_cursor(j=-1):
                    cursor_up(1)
                    y -= 1
            elif key == Keys.A:
                if is_valid_cursor(i=-1):
                    cursor_left(2)
                    x -= 1
            elif key == Keys.S:
                if is_valid_cursor(j=1):
                    cursor_down(1)
                    y += 1
            elif key == Keys.D:
                if is_valid_cursor(i=1):
                    cursor_right(2)
                    x += 1
            elif key == Keys.ENTER:
                result = game.uncover_square(x, y)
                refresh_board()
                if result == LOST:
                    cursor_bottom_left()
                    print('You lost! Game over :(')
                    break
                elif result == WON:
                    cursor_bottom_left()
                    print('Congratulations, you won! :)')
                    break
            elif key == Keys.SPACE:
                game.mark_square(x, y)
                refresh_board()
            elif key == Keys.BACKSPACE:
                cursor_bottom_left()
                print('Exiting minesweeper.')
                break

    except KeyboardInterrupt:
        # caught exception if CTRL-C is called
        cursor_bottom_left()
        print('Exiting minesweeper.')


if __name__ == '__main__':
    main()
