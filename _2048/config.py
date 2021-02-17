import pyglet.window.key as key


BOARD_SIZE = (4, 4)
INIT_TILES = 2


WIN_H = 400
WIN_W = 400

TILE_SPAWN_DIST = (2, 2, 2, 2, 2, 2, 2, 4)

# Background style
BACKGROUND_COLOR = (146, 135, 125)

# Tile style
TILE_COLOR_DICT = {
    0: (255, 255, 255),

    2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121),
    16: (245, 149, 99), 32: (246, 124, 95), 64: (246, 94, 59),
    128: (237, 207, 114), 256: (237, 204, 97), 512: (237, 200, 80),
    1024: (237, 197, 63), 2048: (237, 194, 46)
}

TILE_PADDING = 10.

# Label style
LABEL_COLOR = (0, 0, 0, 255)
LABEL_FONT = "Verdana"
LABEL_BOLD = True
LABEL_FONT_SIZE_W_RATIO = .3
LABEL_FONT_SIZE_H_RATIO = .3

# Commands
UP_KEYS = key.UP, key.NUM_UP, key.W
RIGHT_KEYS = key.RIGHT, key.NUM_RIGHT, key.D
DOWN_KEYS = key.DOWN, key.NUM_DOWN, key.S
LEFT_KEYS = key.LEFT, key.NUM_LEFT, key.A
