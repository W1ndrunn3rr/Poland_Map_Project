from math import inf
from source.graph import Graph
from source.gui import GUI
import json

if __name__ == "__main__":

    file = open("data/all_czyste.json", "r", encoding="utf-8")
    data = json.load(file)
    graph = Graph(data)
    gui = GUI(graph)
    gui.main_loop()
