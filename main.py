from math import inf
from source.graph import Graph
import json

if __name__ == "__main__":

    with open("data/lubelskie.json", "r", encoding="utf-8") as file:
        data = json.load(file)

        graph = Graph(data)
        print(graph.a_star_algorithm("Lukow", "Bilograj"))
