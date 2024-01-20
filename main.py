from graph import Graph
from table import Table


if __name__ == "__main__":

    for _ in range(100):
        row, colmun = (20, 20)

        graph = Graph(row, colmun)

        print(graph.show())

        graph1 = Graph(row, colmun)
        print(graph1.show())

        labyrinth = graph + graph1

        print(labyrinth.show())
