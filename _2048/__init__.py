from _2048.application import Application
from _2048.board import Board
from _2048.window import Window


def run():
    app = Application(board_size=(4, 4), window_width=400, window_height=400)
    app.run()
