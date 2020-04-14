import typing
import time
from itertools import chain
from sudoku import Sudoku, COLUMN_NAMES, ROW_NAMES


class SudokuSolver:
    def __init__(self, board: typing.List[typing.List[int]]):
        self.sudoku = Sudoku(board)

    def solve(self):
        prev_board = None
        while self.sudoku.board != prev_board:
            prev_board = self.sudoku.board.copy()
            self.step()

    def step(self):
        for cell in self.sudoku.editable_cells:
            no_go_nums = set()
            no_go_cells = chain(self.quadrant_cells(cell), self.vertical_cells(cell), self.horizontal_cells(cell))
            for _ in no_go_cells:
                if len(self.sudoku.board[_]) == 1:
                    no_go_nums.add(self.sudoku.board[_][0])
            possible_nums = {_ for _ in range(1, 10)} - no_go_nums
            self.sudoku[cell] = [*possible_nums]
            time.sleep(0.01)

    def quadrant_cells(self, cell: str) -> typing.Iterator[str]:
        col_group = COLUMN_NAMES.find(cell[0]) * 3 // 9
        row_group = ROW_NAMES.find(cell[1]) * 3 // 9

        quadrant_cols = COLUMN_NAMES[col_group*3:col_group*3+3]
        quadrant_rows = ROW_NAMES[row_group*3:row_group*3+3]

        for other_cell in self.sudoku.filled_cells():
            if other_cell[0] in quadrant_cols and other_cell[1] in quadrant_rows and cell != other_cell:
                yield other_cell

    def vertical_cells(self, cell: str) -> typing.Iterator[str]:
        for other_cell in self.sudoku.filled_cells():
            if cell[0] == other_cell[0] and cell != other_cell:
                yield other_cell

    def horizontal_cells(self, cell: str) -> typing.Iterator[str]:
        for other_cell in self.sudoku.filled_cells():
            if cell[1] == other_cell[1] and cell != other_cell:
                yield other_cell

b=[[0,2,9,0,5,3,0,0,0],
[4,8,3,0,0,0,0,2,0],
[0,6,5,0,0,0,0,0,3],
[2,5,0,9,0,0,0,1,0],
[0,0,0,0,3,8,6,0,0],
[0,3,0,0,6,5,4,0,0],
[0,0,0,6,4,2,5,9,0],
[0,0,4,0,1,7,0,0,0],
[0,0,0,5,0,0,0,0,0]]
s=SudokuSolver(b)
s.solve()