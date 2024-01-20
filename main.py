from graph import Graph
from table import Table


if __name__ == "__main__":

    for _ in range(100):

        graph = Graph(10, 10)

        print(graph.show())

        graph1 = Graph(10, 10)
        print(graph1.show())

        labyrinth = graph + graph1

        print(labyrinth.show())
