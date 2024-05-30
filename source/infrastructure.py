import math
from haversine import haversine, Unit

KPH_TO_MPS = 0.277778
AVERAGE_VELOCITY = 130
KILOMETERS_IN_METERS = 1000
SECONDS_IN_HOURS = 3600
R = 6371.0


def convert_time(seconds):
    hours = seconds // 3600
    remaining_seconds = seconds % 3600
    minutes = remaining_seconds / 60

    if minutes >= 60:
        hours += 1
        minutes -= 60

    minutes_decimal = minutes / 60
    total_time = hours + minutes_decimal

    # Formatuj wynik do dwóch miejsc po przecinku
    return f"{total_time:.2f} h"


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
        self.distance = distance * KILOMETERS_IN_METERS

    def calculate_time(self):
        time = (self.distance) / ((self.velocity_dict[self.road_type] * KPH_TO_MPS))
        return time


class PathFinder:
    def h_score(self, start: City, end: City, option="shortest"):
        distance = haversine(
            (start.latitude, start.longitude),
            (end.latitude, end.longitude),
            unit=Unit.METERS,
            normalize=True,
            check=True,
        )
        if option == "fastest":
            return distance / (AVERAGE_VELOCITY * KPH_TO_MPS)
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

    def total_path(self, final_path, final_roads):
        cities = [city.id for city in final_path]
        connections = [connection.road_name for connection in final_roads]
        total_time = sum(connection.calculate_time() for connection in final_roads)
        total_distance = sum(connection.distance for connection in final_roads)
        return (
            convert_time(total_time),
            total_distance / KILOMETERS_IN_METERS,
            connections,
            cities,
        )
