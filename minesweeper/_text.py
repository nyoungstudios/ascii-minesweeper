"""
Text blobs for minesweeper game
"""

# ASCII art for minesweeper
# Slightly modified version of http://patorjk.com/software/taag/#p=display&h=1&v=1&f=Slant&t=minesweeper
HEADER_TEXT = '''\
               _                                                            
   ____ ___   (_)____   ___   _____ _      __ ___   ___   ____   ___   _____
  / __ `__ \ / // __ \ / _ \ / ___/| | /| / // _ \ / _ \ / __ \ / _ \ / ___/
 / / / / / // // / / //  __/(__  ) | |/ |/ //  __//  __// /_/ //  __// /    
/_/ /_/ /_//_//_/ /_/ \___/ \___/  |__/|__/ \___/ \___// .___/ \___//_/     
                                                      /_/                   \
'''

# Help screen text with instructions and controls
HELP_SCREEN = (
    'Minesweeper',
    '',
    'How to play?',
    '1. Uncover a mine, you lose. Otherwise, the game continues.',
    '2. Uncover all of the squares that are not mines, you win!',
    '3. Uncover a empty or number square, it will recursively uncover all of the neighboring non-flagged and non-mine '
    'squares.',
    '4. A number square represents the number of mines that are present in the 8 neighboring squares. This information '
    'can be used to help you with your next move.',
    '',
    'Controls:',
    'Arrow keys or WASD - Moves the cursor',
    'Space - Mark a square as a flag, question mark, or back to hidden',
    'Enter - Select a square to uncover',
    'Backspace or CTRL-C - Returns to main menu',
    '',
    'Advanced:',
    'If you select a square that is already uncovered and the number of the square matches the number of flagged '
    'squares, it will uncover the neighboring non-flagged squares too.',
    '',
    'Created by Nathaniel Young'
)
