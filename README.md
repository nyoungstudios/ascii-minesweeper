# ASCII Minesweeper
[![Gitpod ready](https://img.shields.io/badge/Gitpod-ready-blue?logo=gitpod)](https://gitpod.io/#https://github.com/nyoungstudios/ascii-minesweeper)
[![PyPI version shields.io](https://img.shields.io/pypi/v/ascii-minesweeper.svg)](https://pypi.python.org/project/ascii-minesweeper/)
[![PyPI license](https://img.shields.io/pypi/l/ascii-minesweeper.svg)](https://pypi.python.org/project/ascii-minesweeper/)

Inspired by a minesweeper game on my graphing calculator, I decided to create this version that you can play directly in your terminal. I originally started this project as an Easter egg project to embed into another Python script. This implementation is written in Python and uses `numpy` under the hood. While it is called `ascii-minesweeper`, it actually does use a few characters not in the ASCII character set. Hope you enjoy playing!

## Gameplay
![ascii minesweeper screenshot](https://github.com/nyoungstudios/ascii-minesweeper/blob/main/images/MinesweeperGamePlay480.gif?raw=true)
<!-- ![ascii minesweeper screenshot](images/MinesweeperGamePlay480.gif) -->

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
from minesweeper import PlayMinesweeper
play = PlayMinesweeper()
play.launch_game()
```

## Controls
* Arrow keys or WASD - Moves the cursor
* Space - Mark a square as a flag, question mark, or back to hidden
* Enter - Select a square to uncover
* Backspace or CTRL-C - Returns to main menu

## Play in your web browser
Click this link below to open the code in Gitpod and sign in with your GitHub account.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/nyoungstudios/ascii-minesweeper)
