import math
from haversine import haversine, Unit

AVERAGE_VELOCITY = 100


def convert_time(hours, interface=True):
    decimal_hours = int(hours)
    minutes = int((hours - decimal_hours) * 60)
    if not interface:
        return f"{decimal_hours}.{minutes}"
    if decimal_hours == 0:
        if minutes < 10:
            return f"0.0{minutes} h"
        else:
            return f"0.{minutes} h"
    return f"{decimal_hours} h {minutes} min"


class City:
    def __init__(self, name, id, longitude, latitude):
        self.name = name
        self.id = id
        self.longitude = longitude
        self.latitude = latitude


class Connection:
    velocity_dict = {
        "A": 130,
        "S": 110,
        "K": 90,
        "P": 70,
        "W": 90,
    }

    types_dict = {"A": 5, "S": 4, "K": 3, "W": 3, "P": 2}

    def __init__(self, destination, road_name, road_type, distance):
        self.destination = destination
        self.road_name = road_name
        self.road_type = road_type
        self.distance = distance

    def calculate_time(self):
        time = (self.distance) / ((self.velocity_dict[self.road_type]))
        return time

    def road_class(self):
        return self.types_dict[self.road_type]


class PathFinder:
    def h_score(self, start: City, end: City, option="LENGTH"):
        distance = haversine(
            (start.latitude, start.longitude),
            (end.latitude, end.longitude),
            unit=Unit.KILOMETERS,
            normalize=True,
            check=True,
        )

        if option == "TIME":
            return distance / (AVERAGE_VELOCITY)
        return distance

    def make_path(self, came_from, current):
        total_path = [current]
        total_roads = []
        while current in came_from:
            current, road = came_from[current]
            total_path.append(current)
            total_roads.append(road)
        total_roads.reverse()
        total_path.reverse()
        return total_path, total_roads  # zopytmalizować

    def total_path(self, final_path, final_roads, interface=True, option="LENGTH"):
        cities = [(city.latitude, city.longitude, city.name) for city in final_path]
        connections = [connection.road_name for connection in final_roads]
        total_time = sum(connection.calculate_time() for connection in final_roads)
        total_distance = sum(connection.distance for connection in final_roads)
        return (
            (
                (convert_time(total_time), total_time),
                round(total_distance, 2),
                connections,
                cities,
            )
            if interface == True
            else (
                convert_time(total_time, interface)
                if option == "TIME"
                else total_distance
            )
        )
