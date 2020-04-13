from turtle import Turtle, Screen
import typing
import math

CANVAS_MARGIN = 10
COLUMN_NAMES = 'ABCDEFGHI'
ROW_NAMES = '123456789'


class Sudoku:
    def __init__(self, board: typing.List[typing.List[int]] = None):
        self.board = board
        self.display = SudokuDisplay(board)

    def __getitem__(self, key):
        pass

    def __setitem__(self, key, value):
        pass


class SudokuDisplay:
    def __init__(self, board: typing.List[typing.List[int]], size=900, big_pen=3, small_pen=1):
        if board is None:
            self.board = [[0 for _ in range(9)] for _ in range(9)]
        else:
            self.board = board
        self.small_pen = small_pen
        self.big_pen = big_pen
        self.size = size
        self._font_size = (30 / 900) * self.size
        self._font_offset = self._font_size / 2 + 5
        self._writers: typing.Dict[str, Turtle] = {}
        self.screen = self._setup_screen()
        self._draw_base_board()
        self._instantiate_drawers()
        self.write_matrix(self.board)

    def _draw_base_board(self):
        pen = Turtle()
        pen.hideturtle()
        pen.up()
        pen.width(self.big_pen)
        pen.setpos(0, self.size)
        pen.down()
        for _ in range(4):
            pen.forward(self.size)
            pen.right(90)
        pen.up()
        pen.right(90)
        for _ in range(2):
            pen.setx(pen.xcor() + self.size / 3)
            pen.down()
            pen.forward(self.size)
            pen.up()
            pen.sety(self.size)
        pen.setx(0)
        pen.width(self.small_pen)
        for _ in range(3):
            for _ in range(2):
                pen.setx(pen.xcor() + self.size / 9)
                pen.down()
                pen.forward(self.size)
                pen.up()
                pen.sety(self.size)
            pen.setx(pen.xcor() + self.size / 9)
        pen.setpos(0, 0)
        pen.seth(0)
        pen.width(self.big_pen)
        for _ in range(2):
            pen.sety(pen.ycor() + self.size / 3)
            pen.down()
            pen.forward(self.size)
            pen.up()
            pen.setx(0)
        pen.sety(0)
        pen.width(self.small_pen)
        for _ in range(3):
            for _ in range(2):
                pen.sety(pen.ycor() + self.size / 9)
                pen.down()
                pen.forward(self.size)
                pen.up()
                pen.setx(0)
            pen.sety(pen.ycor() + self.size / 9)
        self.screen.update()

    def _setup_screen(self):
        screen = Screen()
        screen.setup(self.size, self.size)
        screen.setworldcoordinates(-CANVAS_MARGIN, -CANVAS_MARGIN, self.size + CANVAS_MARGIN, self.size + CANVAS_MARGIN)
        screen.tracer(False)
        return screen

    def _instantiate_drawers(self):
        for i, col in enumerate(COLUMN_NAMES):
            for j, row in enumerate(ROW_NAMES):
                writer = Turtle()
                writer.hideturtle()
                writer.up()
                step_size = self.size / 9
                writer.setpos(step_size / 2 + step_size * i,
                              self.size - step_size / 2 - step_size * j - self._font_offset)
                self._writers["".join([col, row])] = writer
        self.screen.update()

    def write_at(self, nums: typing.Union[int, typing.List[int]], pos: str):
        pos: str = pos.upper()
        self._writers[pos].clear()
        if nums:
            if isinstance(nums, int):
                nums = [nums]
            self._get_best_layout(len(nums))(self._writers[pos], nums)

    def _layout_1(self, writer: Turtle, nums: typing.List[int]):
        writer.write("".join(map(str, nums)), align='center', font=('Arial', int(self._font_size), 'normal'))

    def _layout2(self, writer: Turtle, nums: typing.List[int]):
        step_size = self.size / 9
        original_y = writer.ycor()
        y_center = original_y + self._font_offset
        y_top = y_center + step_size / 2
        y_final = y_top - (2 * step_size / 3) - self._font_offset/2
        writer.sety(y_final)
        nums1 = "".join(map(str, nums[:math.ceil(len(nums) / 2)]))
        nums2 = "".join(map(str, nums[math.ceil(len(nums) / 2):]))
        writer.write(f'{nums1}\n{nums2}', align='center', font=('Arial', int(self._font_size), 'normal'))
        writer.sety(original_y)

    def _layout3(self, writer: Turtle, nums: typing.List[int]):
        step_size = self.size / 9
        original_y = writer.ycor()
        y_center = original_y + self._font_offset
        y_top = y_center + step_size / 2
        y_final = y_top - (3 * step_size / 4) - self._font_offset / 3
        writer.sety(y_final)
        nums1 = "".join(map(str, nums[:math.ceil(len(nums) / 3)]))
        nums2 = "".join(map(str, nums[math.ceil(len(nums)/3):math.ceil(2*len(nums)/3)]))
        nums3 = "".join(map(str, nums[math.ceil(2*len(nums)/3):]))
        writer.write(f'{nums1}\n{nums2}\n{nums3}', align='center', font=('Arial', int(self._font_size), 'normal'))
        writer.sety(original_y)

    def _get_best_layout(self, le: int) -> typing.Callable[[Turtle, typing.List[int]], None]:
        return self._layout_1

    def clear(self):
        for writer in self._writers.values():
            writer.clear()
        self.screen.update()

    def clear_at(self, pos: str):
        pos = pos.upper()
        self._writers[pos].clear()

    def write_matrix(self, matrix: typing.List[typing.List[typing.Union[int, typing.List[int]]]]):
        for row, row_id in zip(matrix, ROW_NAMES):
            for num, col_id in zip(row, COLUMN_NAMES):
                if 0 <= num <= 9:
                    self.write_at(num, "".join([col_id, row_id]))
