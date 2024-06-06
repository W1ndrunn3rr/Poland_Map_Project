from math import inf
from source.n_list_graph import NeighborListGraph
from source.n_matrix_graph import NeighborMatrixGraph
from source.gui import GUI
import json
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="W celu wyboru GUI, nie używaj argumentów | Argumenty wywołania bez GUI : town1 town2 [ (LENGTH|TIME) [maxclass [minclass]] ]"
    )
    parser.add_argument(
        "town1", type=str, nargs="?", default=None, help="Nazwa miasta początkowego"
    )
    parser.add_argument(
        "town2", type=str, nargs="?", default=None, help="Nazwa miasta końcowego"
    )

    parser.add_argument(
        "option",
        type=str,
        nargs="?",
        default=None,
        help="Opcja wyboru: LENGTH | TIME",
    )

    parser.add_argument(
        "maxclass", type=int, nargs="?", default=0, help="Maksymalna klasa dróg"
    )
    parser.add_argument(
        "minclass", type=int, nargs="?", default=0, help="Minimalna klasa dróg"
    )

    args = parser.parse_args()

    if args.town1 is None or args.town2 is None:
        print("Podaj miasta początkowe i końcowe")
        exit(1)

    if args.option != "LENGTH" and args.option != "TIME":
        print("Podaj opcję: LENGTH | TIME")
        exit(1)

    if args.maxclass < 0 or args.minclass < 0 or args.maxclass > 5 or args.minclass > 5:
        print("Klasy dróg muszą być liczbami nieujemnymi w przedziale [0, 5]")
        exit(1)

    file = open("data/mapa_polski.json", "r", encoding="utf-8")
    data = json.load(file)
    graph = NeighborListGraph(data)

    if args.town1 is None and args.town2 is None:
        gui = GUI(graph)
        gui.main_loop()
    else:
        print(
            graph.a_star_algorithm(
                args.town1,
                args.town2,
                args.option,
                False,
                args.maxclass,
                args.minclass,
                False,
            )
        )
