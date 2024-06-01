from math import inf
from source.graph import Graph
from source.gui import GUI
import json

if __name__ == "__main__":

    file1 = open("data/podlaskie-wm-poprawione.json", "r", encoding="utf-8")
    file2 = open("data/mazowieckie.json", "r", encoding="utf-8")
    data1 = json.load(file1)
    data2 = json.load(file2)
    graph = Graph(data2)
    print(graph.a_star_algorithm("Warszawa", "Kozienice"))
    print(graph.a_star_algorithm("Kozienice", "Warszawa"))
    gui = GUI(graph)
    gui.main_loop()
