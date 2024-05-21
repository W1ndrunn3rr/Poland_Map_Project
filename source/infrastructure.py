class City:
    def __init__(self, name, id, longitude, latitude):
        self.name = name
        self.id = id
        self.longitude = longitude
        self.latitude = latitude


class Connection:
    velocity_tuple = {
        "A": 140,
        "S": 120,
        "K": 90,
        "P": 90,
        "W": 90,
    }  # do poprawienia przeliczniki

    def __init__(self, city_1, city_2, road_name, road_type, distance):
        self.city_1 = city_1
        self.city_2 = city_2
        self.road_name = road_name
        self.road_type = road_type
        self.distance = distance

    def calculate_time(self):
        self.time = self.distance / self.velocity_tuple[self.road_type]
        return self.time
