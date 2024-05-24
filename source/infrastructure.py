from collections.abc import MutableSet
from functools import total_ordering
import math


def convert_time(time):
    hours = int(time)
    minutes = round((time - hours) * 60)

    if minutes >= 60:
        hours += 1
        minutes -= 60
    return f"{hours}.{minutes}h"


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
        "P": 90,
        "W": 90,
    }  # do poprawienia przeliczniki

    def __init__(self, destination, road_name, road_type, distance):
        self.destination = destination
        self.road_name = road_name
        self.road_type = road_type
        self.distance = distance

    def calculate_time(self):
        time = (
            (self.distance * 1000) / (self.velocity_dict[self.road_type] * (5 / 18))
        ) / 3600
        return time


class PathFinder:
    def h_score(self, start: City, end: City):
        return math.sqrt(
            (start.longitude - end.longitude) ** 2
            + (start.latitude - end.latitude) ** 2
        )

    def make_path(self, path, current):
        total_path = [current.id]
        while current in path:
            current = path[current]
            total_path.append(current.id)
        return total_path[::-1]

    # zopytmalizować
    def total_path(self, path: list, graph):
        copied_path: list = path.copy()
        total_path = []
        for city_id in copied_path:
            connections = next(
                connection for city, connection in graph.items() if city.id == city_id
            )
            copied_path.remove(city_id)
            for connection in connections:
                if connection.destination.id in copied_path:
                    total_path.append(connection)

        total_time = sum(connection.calculate_time() for connection in total_path)
        total_road = sum(connection.distance for connection in total_path)
        return f"Total road : {total_road} km, Total time : {convert_time(total_time)}"
