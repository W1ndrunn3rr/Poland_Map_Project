from math import inf
from source.graph import Graph
import json

if __name__ == "__main__":

    file1 = open("data/dolnoslaski.json", "r", encoding="utf-8")
    file2 = open("/home/omen/Downloads/wielkopolskie.json", "r", encoding="utf-8")
    data1 = json.load(file1)
    data2 = json.load(file2)

    graph = Graph(data2)
    print(graph.a_star_algorithm("Pila", "Kalisz"))
    print(graph.a_star_algorithm("Kalisz", "Pila", "fastest"))
