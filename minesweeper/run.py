"""
Runs interactive minesweeper game in standard out
"""

if __name__ == '__main__':
    from game import *
    from read import *
    from cursor import *

    # creates an instance of the game and prints the board
    game = Minesweeper()
    game.print_board()

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
        cursor_down(1 + game.size - y)
        cursor_left(INDENT + (x * 2))


    def cursor_reset_original():
        """
        Moves cursor to the middle
        """
        cursor_right(INDENT + (x * 2))
        cursor_up(1 + game.size - y)


    def refresh_board(game_lost=False):
        """
        Reprints the board in the same location in standard out so that it looks like the board was updated in place

        :param game_lost: True if we should print the game over board; False, otherwise
        """
        cursor_bottom_left()
        clear_last_lines(1 + game.size)

        if game_lost:
            game.print_game_over_board()
        else:
            game.print_board()

        cursor_reset_original()

    # moves cursor to top left of board
    cursor_reset_original()

    try:
        for key in controls():
            if key == KEY_W:
                if is_valid_cursor(j=-1):
                    cursor_up(1)
                    y -= 1
            elif key == KEY_A:
                if is_valid_cursor(i=-1):
                    cursor_left(2)
                    x -= 1
            elif key == KEY_S:
                if is_valid_cursor(j=1):
                    cursor_down(1)
                    y += 1
            elif key == KEY_D:
                if is_valid_cursor(i=1):
                    cursor_right(2)
                    x += 1
            elif key == ENTER:
                result = game.uncover_square(x, y)
                is_lost = result == LOST
                refresh_board(game_lost=is_lost)
                if is_lost:
                    cursor_bottom_left()
                    print('You lost! Game over :(')
                    break
                elif result == WON:
                    cursor_bottom_left()
                    print('Congratulations, you won! :)')
                    break
            elif key == SPACE:
                game.mark_square(x, y)
                refresh_board()
            elif key == BACKSPACE:
                cursor_bottom_left()
                print('Exiting minesweeper.')
                break

    except KeyboardInterrupt:
        # caught exception if CTRL-C is called
        cursor_bottom_left()
        print('Exiting minesweeper.')
