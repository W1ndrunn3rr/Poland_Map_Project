class City:
    def __init__(self, name, id, longitude, latitude):
        self.name = name
        self.id = id
        self.longitude = longitude
        self.latitude = latitude
        self.connection_list = []

    def add_connection(self, connection):
        self.connection_list.append(connection)

    def get_city(self):
        return self.name, self.id, self.longitude, self.latitude


class Connection:
    velocity_tuple = {
        "A": 140,
        "S": 120,
        "K": 90,
        "P": 90,
        "W": 90,
    }  # do poprawienia przeliczniki

    def __init__(self, destination, road_name, road_type, distance):
        self.destination = destination
        self.road_name = road_name
        self.road_type = road_type
        self.distance = distance

    def calculate_time(self):
        self.time = self.distance / self.velocity_tuple[self.road_type]
        return self.time

    def get_connection(self):
        return self.destination, self.road_name, self.road_type, self.distance
