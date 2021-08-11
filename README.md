# ASCII Minesweeper
Inspired by a minesweeper game on my graphing calculator, I decided to create this version that you can play directly in your terminal. I originally started this project as an Easter egg project to embed into another Python script. This implementation is written in Python and uses `numpy` under the hood. While it is called `ascii-minesweeper`, it actually does use a few characters not in the ASCII character set. Hope you enjoy playing!

## Screenshot
![ascii minesweeper screenshot](https://github.com/nyoungstudios/ascii-minesweeper/blob/main/images/homescreen.png?raw=true)
<!-- ![ascii minesweeper screenshot](images/homescreen.png) -->

## Install
```shell
pip install ascii-minesweeper
```

## Run
In order to run the program from the terminal, you can type:
```shell
minesweeper
```

Otherwise, you can also launch the program from another Python script as an Easter egg like this:
```python
from minesweeper.play import PlayMinesweeper
play = PlayMinesweeper()
play.launch_game()
```

## Controls
* Arrow keys or WASD - Moves the cursor
* Space - Mark a square as a flag, question mark, or back to hidden
* Enter - Select a square to uncover
* Backspace or CTRL-C - Returns to main menu
