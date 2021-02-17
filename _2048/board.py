import random
import enum

import _2048.config as c
from _2048.util import generate_matrix


class Board:
    class State(enum.Enum):
        LOST = 0
        WIN = 1
        CONTINUE = 2

    _row: int
    _col: int

    _board: [[int]]

    def __init__(self, size: (int, int)):
        self._col, self._row = size

        self._board = generate_matrix(size, 0)

    def __getitem__(self, item: (int, int)) -> int:
        x, y = item
        return self._board[x][y]

    def __iter__(self):
        for x in range(self._col):
            for y in range(self._row):
                yield self._board[x][y]

    @property
    def size(self):
        return self._col, self._row

    @property
    def indexes(self):
        for x in range(self._col):
            for y in range(self._row):
                yield x, y

    def spawn_tile(self, value: int = None, pos: (int, int) = None) -> bool:
        if value is None:
            value = random.choice(c.TILE_SPAWN_DIST)

        if pos is None:
            empty_tiles = [
                (x, y)
                for x in range(self._col)
                for y in range(self._row)
                if not self._board[x][y]
            ]

            if empty_tiles:
                pos = random.choice(empty_tiles)

        if pos is not None:
            x, y = pos
            self._board[x][y] = value

            return True
        return False

    def slide_up(self) -> bool:
        update = False

        new_board = generate_matrix((self._col, self._row), 0)

        for x in range(self._col):
            new_board[x][-1] = self._board[x][-1]

            y_idx = self._row - 1

            for y in reversed(range(self._row - 1)):
                if self._board[x][y]:
                    if not new_board[x][y_idx]:
                        # Slide into empty tile
                        new_board[x][y_idx] = self._board[x][y]
                        update = True
                    elif self._board[x][y] == new_board[x][y_idx]:
                        # Slide and add
                        new_board[x][y_idx] *= 2
                        y_idx -= 1
                        update = True
                    else:
                        # Slide and pile
                        y_idx -= 1
                        new_board[x][y_idx] = self._board[x][y]

                        # If isn't only copying
                        if y_idx != y:
                            update = True

        if update:
            self._board = new_board

        return update

    def slide_right(self) -> bool:
        update = False

        new_board = generate_matrix((self._col, self._row), 0)

        for y in range(self._row):
            new_board[-1][y] = self._board[-1][y]

            x_idx = self._col - 1

            for x in reversed(range(self._col - 1)):
                if self._board[x][y]:
                    if not new_board[x_idx][y]:
                        # Slide into empty tile
                        new_board[x_idx][y] = self._board[x][y]
                        update = True
                    elif self._board[x][y] == new_board[x_idx][y]:
                        # Slide and add
                        new_board[x_idx][y] *= 2
                        x_idx -= 1
                        update = True
                    else:
                        # Slide and pile
                        x_idx -= 1
                        new_board[x_idx][y] = self._board[x][y]

                        # If it isn't just a copy
                        if x_idx != x:
                            update = True

        if update:
            self._board = new_board

        return update

    def slide_down(self) -> bool:
        update = False

        new_board = generate_matrix((self._col, self._row), 0)

        for x in range(self._col):
            new_board[x][0] = self._board[x][0]

            y_idx = 0

            for y in range(1, self._row):
                if self._board[x][y]:
                    if not new_board[x][y_idx]:
                        # Slide into empty tile
                        new_board[x][y_idx] = self._board[x][y]
                        update = True
                    elif self._board[x][y] == new_board[x][y_idx]:
                        # Slide and add
                        new_board[x][y_idx] *= 2
                        y_idx += 1
                        update = True
                    else:
                        # Slide and pile
                        y_idx += 1
                        new_board[x][y_idx] = self._board[x][y]

                        # If isn't only copying
                        if y_idx != y:
                            update = True

        if update:
            self._board = new_board

        return update

    def slide_left(self) -> bool:
        update = False

        new_board = generate_matrix((self._col, self._row), 0)

        for y in range(self._row):
            new_board[0][y] = self._board[0][y]

            x_idx = 0

            for x in range(1, self._col):
                if self._board[x][y]:
                    if not new_board[x_idx][y]:
                        # Slide into empty tile
                        new_board[x_idx][y] = self._board[x][y]
                        update = True
                    elif self._board[x][y] == new_board[x_idx][y]:
                        # Slide and add
                        new_board[x_idx][y] *= 2
                        x_idx += 1
                        update = True
                    else:
                        # Slide and pile
                        x_idx += 1
                        new_board[x_idx][y] = self._board[x][y]

                        # If it isn't only copying
                        if x_idx != x:
                            update = True

        if update:
            self._board = new_board

        return update

    def get_state(self) -> State:
        # Check for _2048
        for x in range(self._col):
            for y in range(self._row):
                if self._board[x][y] == 2048:
                    return Board.State.WIN

        # Check for empty tiles
        for x in range(self._col):
            for y in range(self._row):
                if not self._board[x][y]:
                    return Board.State.CONTINUE

        # Check for adjacent tiles with equal values (excluding the angles)
        for x in range(1, self._col - 1):
            for y in range(1, self._row - 1):
                neighbours = set()

                neighbours.add(self._board[x + 1][y])
                neighbours.add(self._board[x][y + 1])
                neighbours.add(self._board[x - 1][y])
                neighbours.add(self._board[x][y - 1])

                if self._board[x][y] in neighbours:
                    return Board.State.CONTINUE

        # Check for adjacent tiles with equal values (in the angles)
        if (
                # Bottom left
                self._board[0][0] in (self._board[0][1], self._board[1][0])
                or
                # Bottom right
                self._board[-1][0] in (self._board[-2][0], self._board[-1][1])
                or
                # Top right
                self._board[-1][-1] in (self._board[-1][-2], self._board[-2][-1])
                or
                # Top left
                self._board[0][-1] in (self._board[1][-1], self._board[0][-2])
        ):
            return Board.State.CONTINUE

        return Board.State.LOST
