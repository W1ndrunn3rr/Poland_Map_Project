from math import inf
from source.n_list_graph import NeighborListGraph
from source.n_matrix_graph import NeighborMatrixGraph
from source.gui import GUI
import json

if __name__ == "__main__":

    file = open("data/all_czyste.json", "r", encoding="utf-8")
    data = json.load(file)
    graph = NeighborMatrixGraph(data)

    gui = GUI(graph)
    gui.main_loop()
