from table import Table
from random import randint


class Graph(Table):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)

        self._makeWay()

    def _makeWay(self):
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
