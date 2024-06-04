from source.infrastructure import City, Connection, PathFinder
from source.priority_queue import PriorityQueue


class NeighborMatrixGraph:
    def __init__(self, json_file):
        self.city_list = []
        self.city_index = {}
        self.cities_num = len(json_file["cities"])
        self.n_matrix = [[0] * self.cities_num for i in range(self.cities_num)]

        for idx, json_city in enumerate(json_file["cities"]):
            city = City(
                json_city["name"],
                json_city["id"],
                json_city["longitude"],
                json_city["latitude"],
            )
            self.city_list.append(city)
            self.city_index[city.id] = idx

        for json_connection in json_file["connections"]:
            city_1_index = self.city_index[json_connection["city_1"]]
            city_2_index = self.city_index[json_connection["city_2"]]
            distance = json_connection["distance"]

            self.n_matrix[city_1_index][city_2_index] = Connection(
                next(
                    (
                        city
                        for city in self.city_list
                        if city.id == json_connection["city_2"]
                    ),
                    None,
                ),
                json_connection["road_name"],
                json_connection["road_type"],
                distance,
            )
            self.n_matrix[city_2_index][city_1_index] = Connection(
                next(
                    (
                        city
                        for city in self.city_list
                        if city.id == json_connection["city_1"]
                    ),
                    None,
                ),
                json_connection["road_name"],
                json_connection["road_type"],
                distance,
            )

        print("Data loaded")

    def a_star_algorithm(
        self, start_id, end_id, option="shortest", avoid_highways=False
    ):
        try:
            start = next(city for city in self.city_list if city.id == start_id)
            end = next(city for city in self.city_list if city.id == end_id)
        except StopIteration:
            return Exception("Brak podanego miasta w bazie")

        finder = PathFinder()
        open_set = PriorityQueue()
        open_set.put(start, 0, 0)
        track = {}

        g_score = {city: float("inf") for city in self.city_list}
        g_score[start] = 0
        f_score = {city: float("inf") for city in self.city_list}

        f_score[start] = finder.h_score(start, end)
        temp_g_score = 0

        closed_set = set()
        while not open_set.empty():
            current = open_set.get()
            closed_set.add(current)

            if current == end:
                final_path, final_roads = finder.make_path(track, current)
                return finder.total_path(final_path, final_roads)
            for connection in self.n_matrix[self.city_index[current.id]]:
                if connection == 0 or connection.road_type == "A" and avoid_highways:
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
                    if connection.destination not in closed_set:
                        open_set.put(
                            connection.destination,
                            f_score[connection.destination],
                            g_score[connection.destination],
                        )

        return None