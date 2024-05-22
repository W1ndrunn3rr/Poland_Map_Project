from source.infrastructure import City, Connection


class Graph:

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

        for json_connection in json_file["connections"]:
            for city in self.city_list:
                if city.id == json_connection["city_1"]:
                    city.add_connection(
                        Connection(
                            json_connection["city_2"],
                            json_connection["road_name"],
                            json_connection["road_type"],
                            json_connection["distance"],
                        )
                    )
                elif city.id == json_connection["city_2"]:
                    city.add_connection(
                        Connection(
                            json_connection["city_1"],
                            json_connection["road_name"],
                            json_connection["road_type"],
                            json_connection["distance"],
                        )
                    )
        for city in self.city_list:
            self.graph_dict.update({city.id: city.connection_list})

    def print_graph(self):
        for city_id, connections in self.graph_dict.items():
            print(f"City ID: {city_id}")
            for conn in connections:
                print(
                    f"Destination : {conn.destination} {conn.road_name} ({conn.road_type}) - {conn.distance} km"
                )
