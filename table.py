class Table:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.matrix = list(list() for _ in range(rows))
        self._set_coordonates()
        self._set_neighbors()
        self._buildOutlines()

    def __str__(self):
        return "[" + ", ".join(str(element) for element in self.matrix) + "]"

    def show(self):
        return self.renderer()

    def __repr__(self):
        return f"Graph:\n{self.__str__()}"

    def __iter__(self):
        for row in range(self.rows):
            for column in range(self.columns):
                yield self.matrix[row][column]

    def _set_coordonates(self):
        for row in range(self.rows):
            for column in range(self.columns):
                _case = Case(row, column)
                self.matrix[row].append(_case)

    def _set_neighbors(self):
        for _case in self:
            _case.detect_neighbors(self.matrix)

    def _buildOutlines(self):
        for row in range(self.rows):
            self.matrix[row][self.columns-1].buildWallIn("right")
            self.matrix[row][0].buildWallIn("left")
        
        for column in range(self.columns):
            self.matrix[0][column].buildWallIn("top")
            self.matrix[self.rows-1][column].buildWallIn("bottom")

    def renderer(self):
        render = ""
        render += self._rendererOutlineT()
        for row in range(self.rows):
            render += "│"
            for column in range(self.columns):
                cell = self.matrix[row][column]
                angleTopLeft = cell.walls["left"] and cell.walls["top"]
                angleTopRight = cell.walls["right"] and cell.walls["top"]
                top = cell.walls["top"]
                bottom = cell.walls["bottom"]
                left = cell.walls["left"]
                right = cell.walls["right"]
                angleBottomLeft = cell.walls["left"] and cell.walls["bottom"]
                angleBottomRight = cell.walls["right"] and cell.walls["bottom"]

                if right and column < self.columns - 1:
                    render += " " * 3 + "│"
                else:
                    render += " " * (4 if column < self.columns - 1 else 3)

            render += "│" + "\n" + (("├" if self.matrix[row][0].walls["bottom"] else "│") if row < self.rows-1 else "")

            if row < self.rows - 1:
                for column in range(self.columns):

                    cell = self.matrix[row][column]
                    right = cell.walls["right"]
                    bottom = cell.walls["bottom"]

                    angleBottomLeft = cell.walls["left"] and cell.walls["bottom"]
                    angleBottomRight = cell.walls["right"] and cell.walls["bottom"]
                    angleCrossroads = cell.walls["right"] and cell.walls["bottom"] and cell.neighbors["right"] and cell.neighbors["right"].walls["bottom"] and cell.neighbors["bottom"] and cell.neighbors["bottom"].walls["right"]
                    angleBottomCross = not cell.walls["right"] and cell.walls["bottom"] and cell.neighbors["right"].walls["bottom"] and cell.neighbors["bottom"] and cell.neighbors["bottom"].walls["right"]
                    angleTopCross = cell.walls["right"] and cell.walls["bottom"] and cell.neighbors["right"] and cell.neighbors["right"].walls["bottom"]
                    angleLeftCross = cell.walls["right"] and cell.walls["bottom"] and cell.neighbors["bottom"].walls["right"]
                    angleRightCross = cell.walls["right"] and cell.neighbors["right"] and cell.neighbors["right"].walls["bottom"] and cell.neighbors["bottom"] and cell.neighbors["bottom"].walls["right"]
                    angleBottomLeft = cell.walls["right"] and not cell.walls["bottom"] and cell.neighbors["right"] and cell.neighbors["right"].walls["bottom"]
                    angleBotomRight = cell.walls["bottom"] and cell.walls["right"]
                    angleTopLeft = cell.neighbors["right"] and cell.neighbors["right"].walls["bottom"] and cell.neighbors["bottom"] and cell.neighbors["bottom"].walls["right"]
                    angleTopRight = cell.walls["bottom"] and cell.neighbors["bottom"].walls["right"]

                    if angleCrossroads:
                        render += "─" * 3 + "┼"
                    elif angleBottomCross:
                        render += "─" * 3 + "┬"
                    elif angleTopCross:
                        render += "─" * 3 + "┴"
                    elif angleLeftCross:
                        render += "─" * 3 + "┤"
                    elif angleRightCross:
                        render += " " * 3 + "├"
                    elif angleBottomLeft:
                        render += " " * 3 + "└"
                    elif angleBottomRight:
                        render += "─" * 3 + "┘"
                    elif angleTopLeft:
                        render += " " * 3 + "┌"
                    elif angleTopRight:
                        render += "─" * 3 + "┐"
                    elif bottom:
                        render += "─" * (4 if column < self.columns - 1 else 3)
                    elif right:
                        render += " " * 3 + "│"
                    else:
                        render += " " * (4 if column < self.columns - 1 else 3)
                render += ("│" if (not self.matrix[row][column].walls["bottom"] and self.matrix[row][column].neighbors["right"]) else "") + "\n"

        render += self._rendererOutlineB()
        return render

    def _rendererOutlineT(self):
        render = "┌"
        for column in range(self.columns):
            if self.matrix[0][column].walls["right"] and column < self.columns - 1:
                render += "─" * 3 + "┬"
            else:
                render += "─" * (4 if column < self.columns - 1 else 3)
        render += "┐\n"
        return render

    def _rendererOutlineB(self):
        render = "└"
        for column in range(self.columns):
            if self.matrix[self.rows-1][column].walls["right"] and column < self.columns - 1:
                render += "─" * 3 + "┴"
            else:
                render += "─" * (4 if column < self.columns - 1 else 3)
        render += "┘\n"
        return render

    def _buildAction(self, position1, position2, action):
        row1, column1 = position1
        row2, column2 = position2
        vertical = row1 == row2
        horizontal = column1 == column2

        if vertical:
            a = column1 if column1 < column2 else column2
            b = column1 if column1 > column2 else column2
            self.matrix[row1][a].walls["right"] = action
            self.matrix[row2][b].walls["left"] = action
        elif horizontal:
            a = row1 if row1 < row2 else row2
            b = row1 if row1 > row2 else row2
            self.matrix[a][column1].walls["bottom"] = action
            self.matrix[b][column2].walls["top"] = action

    def buildWall(self, position1, position2):
        self._buildAction(position1, position2, True)

    def removeWall(self, position1, position2):
        self._buildAction(position1, position2, False)

    def buildSquare(self, case):
        top = case.neighbors["top"]
        bottom = case.neighbors["bottom"]
        left = case.neighbors["left"]
        right = case.neighbors["right"]
        case.buildSquareIn()

        if top:
            top.buildWallIn("bottom")
        if bottom:
            bottom.buildWallIn("top")
        if left:
            left.buildWallIn("right")
        if right:
            right.buildWallIn("left")


class Case:
    def __init__(self, row, column):

        self.row = row
        self.column = column

        self.walls = {
            "top": False,
            "bottom": False,
            "left": False,
            "right": False
        }

        self.neighbors = {
            "top": None,
            "bottom": None,
            "left": None,
            "right": None
        }

    def __str__(self):
        return f"({self.row}, {self.column})"

    def __repr__(self):
        return f"Case: {self.__str__()}"

    def setTop(self, otherCase):
        self.top = otherCase

    def setBottom(self, otherCase):
        self.bottom = otherCase

    def setLeft(self, otherCase):
        self.left = otherCase

    def setRight(self, otherCase):
        self.right = otherCase

    def buildWallIn(self, position:"top, bottom, left, right"):
        self.walls[position] = True

    def removeWallIn(self, position: "top, bottom, left, right"):
        self.walls[position] = False

    def buildSquareIn(self):
        for wall in self.walls.keys():
            self.buildWallIn(wall)

    def detect_neighbors(self, matrix):
        firstRow = 0
        lastRow = len(matrix) - 1
        firstColumn = 0
        lastColumn = len(matrix[0]) - 1

        top = self.row > firstRow
        bottom = self.row < lastRow
        left = self.column > firstColumn
        right = self.column < lastColumn

        if top:
            self.neighbors["top"] = matrix[self.row - 1][self.column]

        if bottom:
            self.neighbors["bottom"] = matrix[self.row + 1][self.column]

        if left:
            self.neighbors["left"] = matrix[self.row][self.column - 1]

        if right:
            self.neighbors["right"] = matrix[self.row][self.column + 1]

    def get_neighbors(self):
        return [neighbor for neighbor in self.neighbors.values() if neighbor]
