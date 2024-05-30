from math import inf
from source.graph import Graph
import json

if __name__ == "__main__":

    file1 = open("data/lubelskie.json", "r", encoding="utf-8")
    file2 = open("data/podlaskie-wm-poprawione.json", "r", encoding="utf-8")
    data1 = json.load(file1)
    data2 = json.load(file2)

    graph = Graph(data1)
    print(graph.a_star_algorithm("Bilograj", "BialaPodlaska", option="shortest"))
    print(graph.a_star_algorithm("BialaPodlaska", "Bilograj", option="shortest"))
