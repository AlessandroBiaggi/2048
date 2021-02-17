import pyglet

from _2048.window import Window
from _2048.board import Board
import _2048.config as c


class Application:
    _window: Window
    _board: Board

    def __init__(
            self,
            board_size: (int, int) = c.BOARD_SIZE,
            init_tiles: int or [(int, int, int)] = c.INIT_TILES,
            window_width: int = c.WIN_W,
            window_height: int = c.WIN_H,
            icon: str or pyglet.image.AbstractImage = None
    ):
        self._board = Board(board_size)

        if type(init_tiles) == int:
            for x in range(init_tiles):
                self._board.spawn_tile()
        else:
            for v, x, y in init_tiles:
                self._board.spawn_tile(v, (x, y))

        if icon is not None and type(icon) == str:
            icon = pyglet.image.load(icon)

        self._window = Window(board=self._board, width=window_width, height=window_height, icon=icon, resizable=True)
        self._window.on_key_release = self.on_key_release

    def on_key_release(self, symbol, _):
        update = False

        if symbol in c.UP_KEYS:
            update = self._board.slide_up()
        elif symbol in c.RIGHT_KEYS:
            update = self._board.slide_right()
        elif symbol in c.DOWN_KEYS:
            update = self._board.slide_down()
        elif symbol in c.LEFT_KEYS:
            update = self._board.slide_left()

        if update:
            self._board.spawn_tile()

        state = self._board.get_state()
        if state != Board.State.CONTINUE:
            if state == Board.State.WIN:
                print("WIN")
                self.exit()
            else:  # state == Board.State.LOST:
                print("LOST")
                self.exit()

        if update:
            self._window.update_tiles_color()
            self._window.update_labels_text()

    def run(self):
        pyglet.app.run()

    def exit(self):
        pyglet.app.exit()
