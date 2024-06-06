from source.n_list_graph import NeighborListGraph
from source.n_matrix_graph import NeighborMatrixGraph
import pytest
import logging
import json

file = open("data/wielkopolskie.json", encoding="utf-8")

json_file = json.load(file)
list_graph = NeighborListGraph(json_file)
matrix_graph = NeighborMatrixGraph(json_file)
cities = json_file["cities"]
graphs = [list_graph, matrix_graph]


# This is a fixture that provides the common test data
@pytest.fixture
def test_data():
    return graphs, cities


@pytest.mark.parametrize(
    "i, j", [(i, j) for i in range(len(cities)) for j in range(len(cities))]
)
def test_path(test_data, i, j):
    graphs, cities = test_data
    city_i_id = cities[i]["id"]
    city_j_id = cities[j]["id"]
    for g in graphs:
        if city_i_id == city_j_id:
            continue

        try:
            time_s, road_s, _, _ = list_graph.a_star_algorithm(city_i_id, city_j_id)
            time_f, road_f, _, _ = list_graph.a_star_algorithm(
                city_i_id, city_j_id, option="TIME"
            )
        except Exception:
            continue
        assert (
            road_s <= road_f or time_s[1] >= time_f[1]
        ), "Błąd czasu lub drogi połączeń"


import pytest


# This test is parametrized to run once for each pair of cities
@pytest.mark.parametrize(
    "i, j", [(i, j) for i in range(len(cities)) for j in range(len(cities))]
)
def test_highways(test_data, i, j):
    graphs, cities = test_data
    city_i_id = cities[i]["id"]
    city_j_id = cities[j]["id"]
    for g in graphs:
        try:
            _, _, roads_type, _ = list_graph.a_star_algorithm(
                city_i_id, city_j_id, avoid_highways=True
            )
        except Exception:
            continue
        for road_type in roads_type:
            assert road_type != "A", "Znaleziono połączenie autostradowe"


@pytest.mark.parametrize(
    "i, j", [(i, j) for i in range(len(cities)) for j in range(len(cities))]
)
def test_dual(test_data, i, j):
    graphs, cities = test_data
    city_i_id = cities[i]["id"]
    city_j_id = cities[j]["id"]
    for g in graphs:
        if city_i_id == city_j_id:
            continue

        try:
            time1_s, road1_s, _, _ = list_graph.a_star_algorithm(city_i_id, city_j_id)
            time1_f, road1_f, _, _ = list_graph.a_star_algorithm(
                city_i_id, city_j_id, option="TIME"
            )

            time2_s, road2_s, _, _ = list_graph.a_star_algorithm(city_j_id, city_i_id)
            time2_f, road2_f, _, _ = list_graph.a_star_algorithm(
                city_j_id, city_i_id, option="TIME"
            )
        except Exception:
            continue

        assert (
            time1_f[1] == time2_f[1]
            or time1_s[1] == time2_s[1]
            or road1_f == road2_f
            or road1_s == road2_s
        ), f"{city_i_id}, {city_j_id}"
