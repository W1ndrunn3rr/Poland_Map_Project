from source.graph import Graph
import pytest
import json

file = open("data/lubelskie.json", encoding="utf-8")

json_file = json.load(file)
graph = Graph(json_file)

cities = json_file["cities"]


def test_path():
    for i in range(len(cities)):
        city_i_id = cities[i]["id"]
        for j in range(len(cities)):
            city_j_id = cities[j]["id"]

            time_s, road_s, _, _ = graph.a_star_algorithm(city_i_id, city_j_id)
            time_f, road_f, _, _ = graph.a_star_algorithm(
                city_i_id, city_j_id, option="fastest"
            )
            assert (
                road_s <= road_f and time_s >= time_f
            ), "Błąd czasu lub drogi połączeń"


def test_highways():
    for i in range(len(cities)):
        city_i_id = cities[i]["id"]
        for j in range(len(cities)):
            city_j_id = cities[j]["id"]

            _, _, roads_type, _ = graph.a_star_algorithm(
                city_i_id, city_j_id, avoid_highways=True
            )
            for road_type in roads_type:
                assert road_type != "A", "Znaleziono połączenie autostradowe"


def test_dual():
    for i in range(len(cities)):
        city_i_id = cities[i]["id"]
        for j in range(len(cities)):
            city_j_id = cities[j]["id"]

            time1_s, road1_s, _, _ = graph.a_star_algorithm(city_i_id, city_j_id)
            time1_f, road1_f, _, _ = graph.a_star_algorithm(
                city_i_id, city_j_id, option="fastest"
            )
            time2_s, road2_s, _, _ = graph.a_star_algorithm(city_j_id, city_i_id)
            time2_f, road2_f, _, _ = graph.a_star_algorithm(
                city_j_id, city_i_id, option="fastest"
            )

            assert (
                time1_f == time2_f
                or time1_s == time2_s
                or road1_f == road2_f
                or road1_s == road2_s
            ), f"{city_i_id}, {city_j_id}"
