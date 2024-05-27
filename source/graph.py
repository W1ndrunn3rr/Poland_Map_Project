from os import error, path
from typing import Dict
from source.infrastructure import City, Connection, PathFinder
from source.priority_queue import PriorityQueue


class Graph:
    # zoptymalizować
    def __init__(self, json_file):
        self.city_list = []
        self.graph_dict = {}

        for json_city in json_file["cities"]:

            city = City(
                json_city["name"],
                json_city["id"],
                json_city["latitude"],
                json_city["longitude"],
            )
            self.city_list.append(city)

        for city in self.city_list:
            connection_list = []
            for json_connection in json_file["connections"]:
                if city.id == json_connection["city_1"]:
                    destination = next(
                        (
                            city
                            for city in self.city_list
                            if city.id == json_connection["city_2"]
                        ),
                        None,
                    )
                    if destination is not None:
                        connection_list.append(
                            Connection(
                                destination,
                                json_connection["road_name"],
                                json_connection["road_type"],
                                json_connection["distance"],
                            )
                        )
                elif city.id == json_connection["city_2"]:
                    destination = next(
                        (
                            city
                            for city in self.city_list
                            if city.id == json_connection["city_1"]
                        ),
                        None,
                    )
                    if destination is not None:
                        connection_list.append(
                            Connection(
                                destination,
                                json_connection["road_name"],
                                json_connection["road_type"],
                                json_connection["distance"],
                            )
                        )
            self.graph_dict.update({city: connection_list})

    print("Data loaded")

    def a_star_algorithm(
        self, start_id, end_id, option="shortest", avoid_highways=False
    ):
        try:
            start = next(city for city in self.city_list if city.id == start_id)
            end = next(city for city in self.city_list if city.id == end_id)
        except StopIteration:
            print("Nie znaleziono miasta")
            exit()
        finder = PathFinder()
        open_set = PriorityQueue()
        open_set.put(0, start)
        track = {}
        g_score = {city: float("inf") for city in self.graph_dict}
        g_score[start] = 0
        f_score = {city: float("inf") for city in self.graph_dict}
        f_score[start] = finder.h_score(start, end)
        temp_g_score = 0

        open_set_hash = {start}

        while not open_set.empty():
            current = open_set.get()
            open_set_hash.remove(current)
            if current == end:
                final_path, final_roads = finder.make_path(track, current)
                return finder.total_path(final_path, final_roads)
            for connection in self.graph_dict[current]:
                if connection.road_type == "A" and avoid_highways:
                    continue
                if option == "shortest":
                    temp_g_score = g_score[current] + connection.distance
                elif option == "fastest":
                    temp_g_score = g_score[current] + connection.calculate_time()
                if temp_g_score < g_score[connection.destination]:
                    track[connection.destination] = (current, connection)
                    g_score[connection.destination] = temp_g_score

                    if option == "shortest":
                        f_score[connection.destination] = temp_g_score + finder.h_score(
                            connection.destination, end
                        )
                    elif option == "fastest":
                        f_score[connection.destination] = temp_g_score + finder.h_score(
                            connection.destination, end, "fastest"
                        )

                    if connection.destination not in open_set_hash:
                        open_set.put(
                            f_score[connection.destination],
                            connection.destination,
                        )
                        open_set_hash.add(connection.destination)

        return None
