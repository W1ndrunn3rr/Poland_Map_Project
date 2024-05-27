from collections.abc import MutableSet
from functools import total_ordering
import math
from typing import Dict, Tuple, final

DEGREES_FOR_METER = 111320
KPH_TO_MPS = 5 / 18
MAX_VELOCITY = 130
KILOMETERS_IN_METERS = 1000
SECONDS_IN_HOURS = 3600


def convert_time(time):
    divided_time = time / 3600
    hours = int(divided_time)
    minutes = round((divided_time - hours) * 60)

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
        "P": 70,
        "W": 90,
    }  # do poprawienia przeliczniki

    def __init__(self, destination, road_name, road_type, distance):
        self.destination = destination
        self.road_name = road_name
        self.road_type = road_type
        self.distance = distance

    def calculate_time(self):
        time = (self.distance * KILOMETERS_IN_METERS) / (
            self.velocity_dict[self.road_type] * KPH_TO_MPS
        )
        return time


class PathFinder:
    def h_score(self, start: City, end: City, option="shortest"):
        euklides_distance = math.sqrt(
            (start.longitude - end.longitude) ** 2
            + (start.latitude - end.latitude) ** 2
        )
        if option == "shortest":
            return euklides_distance * DEGREES_FOR_METER
        elif option == "fastest":
            return (euklides_distance * DEGREES_FOR_METER) / (MAX_VELOCITY * KPH_TO_MPS)

        return -1

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

    def total_path(self, final_path, final_roads):
        cities = []
        connections = []
        for city in final_path:
            cities.append(city.id)
        for connection in final_roads:
            connections.append(connection.road_name)
        total_time = sum(connection.calculate_time() for connection in final_roads)
        total_road = sum(connection.distance for connection in final_roads)
        return f"Cities : {cities}]\nTotal road : {total_road} km\nTotal time : {convert_time(total_time)}\nRoads : {connections}\n"
