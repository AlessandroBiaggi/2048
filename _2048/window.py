import pyglet

import _2048.config as c
from _2048.board import Board

from _2048.util import generate_matrix


class Window(pyglet.window.Window):
    _board: Board

    _background: pyglet.shapes.Rectangle

    _tile_padding: float

    _tile_width: float
    _tile_height: float

    _tiles_batch: pyglet.graphics.Batch
    _tiles_grid: [[pyglet.shapes.Rectangle]]

    _labels_batch: pyglet.graphics.Batch
    _labels_grid: [[pyglet.text.Label]]

    def __init__(
            self,
            board: Board,
            width: int = c.WIN_W,
            height: int = c.WIN_H,
            tile_padding: float = c.TILE_PADDING,
            icon: pyglet.image.AbstractImage = None,
             *args, **kwargs
    ):
        super(Window, self).__init__(width, height, *args, **kwargs)
        self._board = board

        self._tile_padding = tile_padding

        if icon is not None:
            self.set_icon(icon)

        self.generate_background()

        self.update_tile_size()
        self.generate_tiles()

        self.generate_labels()

    def update_tile_size(self):
        col, row = self._board.size

        self._tile_width = (self.width - 2 * self._tile_padding - (col - 1) * self._tile_padding) / col
        self._tile_height = (self.height - 2 * self._tile_padding - (row - 1) * self._tile_padding) / row

    def generate_background(self):
        self._background = pyglet.shapes.Rectangle(
            x=0, y=0,
            width=self.width, height=self.height,
            color=c.BACKGROUND_COLOR
        )

    def update_background(self):
        self._background.width = self.width
        self._background.height = self.height

    def get_tile_position(self, x: int, y: int) -> (float, float):
        ax = (x + 1) * self._tile_padding + x * self._tile_width
        ay = (y + 1) * self._tile_padding + y * self._tile_height

        return ax, ay

    def generate_tiles(self):
        self._tiles_batch = pyglet.graphics.Batch()
        self._tiles_grid = generate_matrix(self._board.size)

        for x, y in self._board.indexes:
            ax, ay = self.get_tile_position(x, y)

            self._tiles_grid[x][y] = pyglet.shapes.Rectangle(
                x=ax, y=ay,
                width=self._tile_width, height=self._tile_height,
                color=c.TILE_COLOR_DICT[self._board[x, y]],
                batch=self._tiles_batch
            )

    def update_tiles_position(self):
        for x, y in self._board.indexes:
            ax, ay = self.get_tile_position(x, y)

            self._tiles_grid[x][y].x = ax
            self._tiles_grid[x][y].y = ay

    def update_tiles_size(self):
        for x, y in self._board.indexes:
            self._tiles_grid[x][y].width = self._tile_width
            self._tiles_grid[x][y].height = self._tile_height

    def update_tiles_color(self):
        for x, y in self._board.indexes:
            self._tiles_grid[x][y].color = c.TILE_COLOR_DICT[self._board[x, y]]

    def get_label_position(self, x: int, y: int) -> (float, float):
        ax = self._tile_padding * (x + 1) + x * self._tile_width + self._tile_width / 2
        ay = self._tile_padding * (y + 1) + y * self._tile_height + self._tile_height / 2

        return ax, ay

    def get_labels_font_size(self) -> float:
        return min(
            self._tile_width * c.LABEL_FONT_SIZE_W_RATIO,
            self._tile_height * c.LABEL_FONT_SIZE_H_RATIO
        )

    def get_label_text(self, x: int, y: int) -> str:
        if self._board[x, y]:
            return str(self._board[x, y])
        return ''

    def generate_labels(self):
        self._labels_batch = pyglet.graphics.Batch()
        self._labels_grid = generate_matrix(self._board.size)

        font_size = self.get_labels_font_size()

        for x, y in self._board.indexes:
            ax, ay = self.get_label_position(x, y)

            self._labels_grid[x][y] = pyglet.text.Label(
                text=self.get_label_text(x, y),

                x=ax, y=ay,
                anchor_x='center', anchor_y='center',

                color=c.LABEL_COLOR, font_name=c.LABEL_FONT,
                font_size=font_size, bold=c.LABEL_BOLD,

                batch=self._labels_batch
            )

    def update_labels_position(self):
        for x, y in self._board.indexes:
            ax, ay = self.get_label_position(x, y)

            self._labels_grid[x][y].x = ax
            self._labels_grid[x][y].y = ay

    def update_labels_size(self):
        font_size = self.get_labels_font_size()

        for x, y in self._board.indexes:
            self._tiles_grid[x][y].font_size = font_size

    def update_labels_text(self):
        for x, y in self._board.indexes:
            self._labels_grid[x][y].text = self.get_label_text(x, y)

    def on_draw(self):
        self.clear()

        self._background.draw()
        self._tiles_batch.draw()
        self._labels_batch.draw()
