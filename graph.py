from table import Table
from random import randint


class Graph(Table):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)

        self.makeWay()

    def placeWall(self, position1, position2, history):
        row = 0
        column = 1
        horizontal = position1[row] == position2[row]
        vertical = position1[column] == position2[column]
        previousPosition = (history[-2][row], history[-2][column]) if 1 < len(history) else (None, None)

        if horizontal:
            # Bottom position
            if position1[row] < self.rows - 1:
                bottomPosition = (position1[row]+1, position1[column])
                if bottomPosition != previousPosition:
                    self.buildWall(position1, bottomPosition)
            # Top position
            if 0 < position1[row]:
                topPosition = (position1[row]-1, position1[column])
                if topPosition != previousPosition:
                    self.buildWall(position1, topPosition)

        elif vertical:
            # Right position
            if position1[column] < self.columns - 1:
                rightPosition = (position1[row], position1[column]+1)
                if rightPosition != previousPosition:
                    self.buildWall(position1, rightPosition)
            # left position
            if 0 < position1[column]:
                leftPosition = (position1[row], position1[column]-1)
                if leftPosition != previousPosition:
                    self.buildWall(position1, leftPosition)

    def makeWay(self):
        steps = (self.rows * self.columns) - 1
        position = (randint(0, self.rows-1), randint(0, self.columns-1))
        visited = set()
        history = list()

        while 0 < steps:
            row, column = position
            history.append(position) if (row, column) not in visited else None
            visited.add(position)
            current = self.matrix[row][column]
            nextCurrent = [neighbor for neighbor in current.get_neighbors() if (neighbor.row, neighbor.column) not in visited]
            if len(nextCurrent):
                nextPosition = nextCurrent[randint(0, len(nextCurrent)-1)]
                self.buildSquare(nextPosition)
                self.removeWall(position, (nextPosition.row, nextPosition.column))
                steps -= 1
                position = (nextPosition.row, nextPosition.column)
            else:
                position = history.pop()

    def __add__(self, otherGraph):

        if isinstance(otherGraph, Graph):
            labyrinth = Table(self.rows, self.columns)
            for row in range(self.rows):
                for column in range(self.columns):
                    for wall in ["top", "bottom", "left", "right"]:
                        reference = self.matrix[row][column].walls[wall]
                        if reference == otherGraph.matrix[row][column].walls[wall]:
                            labyrinth.matrix[row][column].walls[wall] = reference
            return labyrinth
        else:
            return NotImplemented
