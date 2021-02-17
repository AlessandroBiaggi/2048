def generate_matrix(size: (int, int), value=None):
    col, row = size
    return [[value for _ in range(row)] for _ in range(col)]
