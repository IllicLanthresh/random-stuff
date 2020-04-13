import typing
from itertools import chain
from .sudoku import Sudoku


class SudokuSolver:
    def __init__(self, board: typing.List[typing.List[int]]):
        self.sudoku = Sudoku(board)

    def step(self):
        for cell in self.sudoku.editable_cells:
            no_nums = {_ for _ in chain(self.quadrant_nums(cell), self.vertical_nums(cell), self.horizontal_nums(cell))}
            possible_nums = {_ for _ in range(1, 10)} - no_nums
            self.sudoku[cell] = [*possible_nums]

    def quadrant_nums(self, cell: str) -> typing.Iterator[int]:
        raise NotImplementedError

    def vertical_nums(self, cell: str) -> typing.Iterator[int]:
        for other_cell in self.sudoku.filled_cells():
            if cell[0] == other_cell[0] and cell != other_cell:
                yield other_cell

    def horizontal_nums(self, cell: str) -> typing.Iterator[int]:
        for other_cell in self.sudoku.filled_cells():
            if cell[1] == other_cell[1] and cell != other_cell:
                yield other_cell
