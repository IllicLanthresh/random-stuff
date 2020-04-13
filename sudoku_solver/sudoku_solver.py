from .sudoku import Sudoku
import typing


class SudokuSolver:
    def __init__(self, board: typing.List[typing.List[int]]):
        self.sudoku = Sudoku(board)
