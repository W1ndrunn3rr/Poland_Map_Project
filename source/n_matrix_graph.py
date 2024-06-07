from source.infrastructure import City, Connection, PathFinder
from source.priority_queue import PriorityQueue


class NeighborMatrixGraph:
    """
    @brief Klasa reprezentująca graf sąsiedztwa w postaci macierzy sąsiedztwa.
    """

    def __init__(self, json_file):
        """
        @brief Inicjalizuje obiekt klasy NeighborMatrixGraph.

        @args:
        - json_file: Plik JSON zawierający informacje o miastach i połączeniach.
        """
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

    def a_star_algorithm(
        self,
        start_id,
        end_id,
        option="LENGTH",
        avoid_highways=False,
        max_class=0,
        min_class=0,
        interface=True,
    ):
        """
        @brief Implementuje algorytm A* do znalezienia najkrótszej ścieżki między dwoma miastami.
        @args:
        - start_id: Identyfikator początkowego miasta.
        - end_id: Identyfikator docelowego miasta.
        - option: Opcja wyboru kryterium (LENGTH lub TIME), domyślnie LENGTH.
        - avoid_highways: Flaga określająca, czy należy unikać autostrad, domyślnie False.
        - min_class: Minimalna klasa drogi, domyślnie 0.
        - max_class: Maksymalna klasa drogi, domyślnie 5.
        - interface: Flaga określająca, czy zwracać wynik w postaci interfejsu, domyślnie True.

        @returns: Najkrótsza ścieżka między miastami lub informacja o braku ścieżki.
        """

        neighbours = 0
        if not interface:
            try:
                start = next(city for city in self.city_list if city.id == start_id)
                end = next(city for city in self.city_list if city.id == end_id)  
            except StopIteration:
                return "NOTFOUND" + " " + str(neighbours)
        elif interface:
            try:
                start = next(city for city in self.city_list if city.name == start_id)
                end = next(city for city in self.city_list if city.name == end_id)  
            except StopIteration:
                return "NOTFOUND" + " " + str(neighbours)

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
                return_string = " ".join(city.id for city in final_path)

                total_path = finder.total_path(
                    final_path, final_roads, interface, option
                )

                if not interface:
                    return_string += " " + str(total_path) + " " + str(neighbours)

                return total_path if interface else return_string

            for connection in self.n_matrix[self.city_index[current.id]]:
                if (connection == 0) or (
                    connection.road_type == "A" and avoid_highways
                ):
                    continue
                if (connection.road_class() < min_class and min_class != 0) or (
                    connection.road_class() > max_class and max_class != 0
                ):
                    continue
                if option == "LENGTH":
                    temp_g_score = g_score[current] + connection.distance
                elif option == "TIME":
                    temp_g_score = g_score[current] + connection.calculate_time()

                if temp_g_score < g_score[connection.destination]:
                    track[connection.destination] = (current, connection)
                    g_score[connection.destination] = temp_g_score
                    if option == "LENGTH":
                        f_score[connection.destination] = temp_g_score + finder.h_score(
                            connection.destination, end
                        )
                    elif option == "TIME":
                        f_score[connection.destination] = temp_g_score + finder.h_score(
                            connection.destination, end, "TIME"
                        )
                    if connection.destination not in closed_set:
                        neighbours = neighbours + 1
                        open_set.put(
                            connection.destination,
                            f_score[connection.destination],
                            g_score[connection.destination],
                        )

        return "NOTFOUND" + " " + str(neighbours)
    
    
    def get_cities(self):
        """
        @brief Zwraca listę miast w grafie.
        """
        return self.city_list
