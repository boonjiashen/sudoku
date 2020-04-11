from typing import Tuple


class Grid(tuple):

    WIDTH = 9  # Also height
    EMPTY = 0  # Number used to denote empty cell

    def __new__(cls, x: Tuple[Tuple[int]]):
        if len(x) != cls.WIDTH:
            raise Exception(f"Height needs to be {cls.WIDTH} but is {len(x)}.")
        for i, row in enumerate(x):
            if len(row) != cls.WIDTH:
                raise Exception(f"Width needs to be {cls.WIDTH} but row {i} is {len(row)}.")
        return super().__new__(cls, x)

    def __str__(self):
        def get_subrow_str(subrow):
            """3 subrows make one row"""
            return " ".join(str(x if x != self.EMPTY else " ") for x in subrow)

        def get_row_str(row):
            """9 rows make a grid"""
            subrows = [row[i * 3: i * 3 + 3] for i in range(3)]
            return " | ".join(get_subrow_str(subrow) for subrow in subrows)

        def get_row_triplet_str(row_triplet):
            """3 row-triplets make a grid"""
            return "\n".join(get_row_str(row) for row in row_triplet)

        row_triplets = [self[i * 3: i * 3 + 3] for i in range(3)]
        row_triplet_strs = [get_row_triplet_str(row_triplet) for row_triplet in row_triplets]
        row_divider = "-" * len(row_triplet_strs[0].splitlines()[0])

        return ("\n" + row_divider + "\n").join(row_triplet_strs)

    def find_first_empty(self):
        """Returns the coordinates of the first empty cell; None otherwise"""
        for r_idx, row in enumerate(self):
            for c_idx, cell in enumerate(row):
                if cell == self.EMPTY:
                    return r_idx, c_idx
        return None

    def is_full(self):
        """Returns true if grid is full, false otherwise"""
        return all(cell != self.EMPTY for row in self for cell in row)

    def get_candidates(self, r_idx, c_idx):
        """Returns the possible candidates for a cell coordinate; throws if it's already filled"""
        if self[r_idx][c_idx]:
            raise Exception(f"({r_idx}, {c_idx}) is already filled with {self[r_idx][c_idx]}")
        row = self[r_idx]
        col = list(zip(*self))[c_idx]
        subgrid_r_idx = r_idx // 3 * 3
        subgrid_c_idx = c_idx // 3 * 3
        subgrid = [self[r][c] for r in range(subgrid_r_idx, subgrid_r_idx+3)
                   for c in range(subgrid_c_idx, subgrid_c_idx+3)]
        return set(range(10)) - set(row) - set(col) - set(subgrid)

    def add(self, r_idx, c_idx, val):
        """Returns a grid that adds val to a coordinate; throws if cell already filled"""

        if self[r_idx][c_idx] != self.EMPTY:
            raise Exception(f"({r_idx}, {c_idx}) is already filled with {self[r_idx][c_idx]}")
        next_grid = list(list(row) for row in self)
        next_grid[r_idx][c_idx] = val
        return Grid(next_grid)


def solve(grid: Grid):
    def do_solve(grid: Grid):
        """Returns solved grid if grid can be solved, else returns None"""
        if grid.is_full():
            return grid
        cell_to_fill = grid.find_first_empty()
        candidates = grid.get_candidates(*cell_to_fill)
        if len(candidates) == 0:
            return None
        for candidate in candidates:
            next_grid = grid.add(*cell_to_fill, candidate)
            solved_next_grid = do_solve(next_grid)
            if solved_next_grid is not None:
                return solved_next_grid
        return None
    return do_solve(grid)


if __name__ == "__main__":
    def print_solve(grid: Grid):
        print("Grid to solve:", grid, sep="\n")
        print("Solution:", solve(grid), sep="\n")

    easy_grid = [
       [9, 7, 0, 0, 0, 0, 6, 0, 0],
       [2, 0, 1, 5, 0, 9, 0, 3, 4],
       [8, 3, 0, 0, 4, 0, 0, 1, 0],
       [0, 0, 0, 4, 0, 2, 0, 0, 0],
       [7, 0, 6, 0, 5, 0, 0, 0, 2],
       [0, 5, 2, 0, 3, 8, 0, 0, 0],
       [5, 0, 0, 8, 1, 7, 0, 0, 6],
       [6, 2, 0, 3, 0, 4, 0, 5, 1],
       [0, 0, 0, 0, 4, 0, 4, 0, 3],
    ]
    med_grid = [
        [1, 2, 0, 6, 0, 0, 4, 0, 9],
        [0, 0, 0, 0, 0, 4, 1, 0, 2],
        [0, 0, 6, 0, 1, 0, 5, 0, 0],
        [6, 0, 8, 1, 0, 0, 0, 0, 0],
        [0, 5, 0, 3, 4, 2, 0, 0, 0],
        [4, 0, 2, 0, 0, 8, 0, 0, 0],
        [8, 0, 7, 0, 0, 0, 3, 0, 5],
        [3, 0, 4, 0, 0, 0, 0, 2, 6],
        [0, 0, 0, 4, 0, 0, 0, 0, 0],
    ]
    hard_grid = [
        [5, 0, 3, 7, 6, 0, 0, 0, 0],
        [0, 2, 6, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 8, 0],
        [7, 0, 0, 0, 4, 0, 0, 0, 1],
        [0, 0, 4, 0, 0, 0, 0, 0, 6],
        [0, 1, 0, 0, 0, 6, 0, 7, 3],
        [9, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 0, 0, 0, 5, 0, 0, 0],
        [0, 0, 0, 6, 0, 3, 1, 9, 0],
    ]
    expert_grid = [
        [0, 7, 0, 3, 0, 5, 0, 0, 9],
        [0, 0, 0, 0, 0, 0, 1, 0, 8],
        [0, 0, 0, 0, 9, 0, 0, 0, 0],
        [0, 3, 0, 4, 0, 0, 0, 0, 0],
        [0, 9, 8, 0, 0, 2, 0, 0, 7],
        [7, 0, 4, 0, 0, 0, 9, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 6, 8, 0, 0, 4, 3],
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    print_solve(Grid(expert_grid))
