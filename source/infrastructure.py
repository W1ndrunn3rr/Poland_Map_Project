import math
from haversine import haversine, Unit



MAX_VELOCITY = 130

# https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
def convert_seconds(seconds):
    # Oblicz godziny, minuty i sekundy
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Zwróć czas w formacie hh:mm:ss.sss
    return f"{int(hours):02}:{int(minutes):02}:{seconds:06.3f}"

def convert_time(hours):
    """
    @brief Konwertuje czas z formatu liczbowego na format tekstowy.

    @args:
        hours (float): Czas w godzinach.
        interface (bool, optional): Określa, czy zwrócony czas ma być w formacie interfejsowym.
            Domyślnie True.

    @returns:
        str: Skonwertowany czas w formacie tekstowym.
    """
    decimal_hours = int(hours)
    minutes = int((hours - decimal_hours) * 60)
    if decimal_hours == 0:
        if minutes < 10:
            return f"0.0{minutes} h"
        else:
            return f"0.{minutes} h"
    return f"{decimal_hours} h {minutes} min"


class City:
    """
    @brief Klasa reprezentująca miasto
    """

    def __init__(self, name, id, longitude, latitude):
        """
        @brief Inicjalizuje obiekt reprezentujący miasto.

        @args:
            name (str): Nazwa miasta.
            id (int): Identyfikator miasta.
            longitude (float): Długość geograficzna miasta.
            latitude (float): Szerokość geograficzna miasta.
        """
        self.name = name
        self.id = id
        self.longitude = longitude
        self.latitude = latitude


class Connection:
    """
    @brief Klasa reprezentująca połączenie między miastami.
    """

    velocity_dict = {
        "A": 130,
        "S": 110,
        "K": 90,
        "P": 70,
        "W": 70,
    }

    types_dict = {"A": 5, "S": 4, "K": 3, "W": 2, "P": 2}

    def __init__(self, destination, road_name, road_type, distance):
        """
        @brief Inicjalizuje obiekt reprezentujący połączenie między miastami.

        @args:
            destination (City): Miasto docelowe.
            road_name (str): Nazwa drogi.
            road_type (str): Typ drogi.
            distance (float): Odległość między miastami.
        """
        self.destination = destination
        self.road_name = road_name
        self.road_type = road_type
        self.distance = distance

    def calculate_time(self):
        """
        @brief Oblicza czas podróży dla danego połączenia.

        @returns:
            float: Czas podróży w godzinach.
        """
        time = (self.distance) / ((self.velocity_dict[self.road_type]))
        return time

    def road_class(self):
        """
        @brief Zwraca klasę drogi dla danego połączenia.

        @returns:
            int: Klasa drogi.
        """
        return self.types_dict[self.road_type]


class PathFinder:
    """
    @brief Klasa reprezentująca pomocnicze narzędzie do algorytmu A*.
    """

    def h_score(self, start: City, end: City, option="LENGTH"):
        """
        @brief Oblicza heurystykę dla algorytmu A*.

        @args:
            start (City): Miasto początkowe.
            end (City): Miasto docelowe.
            option (str, optional): Określa, czy heurystyka ma być obliczona na podstawie
                długości trasy ("LENGTH") czy czasu podróży ("TIME"). Domyślnie "LENGTH".

        @returns:
            float: Heurystyka.
        """
        distance = haversine(
            (start.latitude, start.longitude),
            (end.latitude, end.longitude),
            unit=Unit.KILOMETERS,
            normalize=True,
            check=True,
        )

        if option == "TIME":
            return distance / (MAX_VELOCITY)
        return distance

    def make_path(self, came_from, current):
        """
        @brief Tworzy ścieżkę i listę dróg na podstawie informacji o poprzednich węzłach.

        @args:
            came_from (dict): Słownik zawierający informacje o poprzednich węzłach.
            current (City): Aktualny węzeł.

        @returns:
            tuple: Krotka zawierająca ścieżkę i listę dróg.
        """
        total_path = [current]
        total_roads = []
        while current in came_from:
            current, road = came_from[current]
            total_path.append(current)
            total_roads.append(road)
        total_roads.reverse()
        total_path.reverse()
        return total_path, total_roads

    def total_path(self, final_path, final_roads, interface=True, option="LENGTH"):
        """
        @brief Oblicza całkowitą trasę i czas podróży na podstawie ścieżki i listy dróg.

        @args:
            final_path (list): Lista miast w ścieżce.
            final_roads (list): Lista dróg w ścieżce.
            interface (bool, optional): Określa, czy zwrócone wartości mają być w formacie
                interfejsowym. Domyślnie True.
            option (str, optional): Określa, czy czas podróży ma być obliczony na podstawie
                długości trasy ("LENGTH") czy czasu podróży ("TIME"). Domyślnie "LENGTH".

        @returns:
            tuple or float: Krotka zawierająca czas podróży, całkowitą odległość, listę dróg
                i listę miast, jeśli interface=True. W przeciwnym razie zwraca czas podróży
                lub całkowitą odległość w zależności od wartości option.
        """
        cities = [(city.latitude, city.longitude, city.name) for city in final_path]
        connections = [connection.road_name for connection in final_roads]
        total_time = sum(connection.calculate_time() for connection in final_roads)
        total_distance = sum(connection.distance for connection in final_roads)
        
        time_in_seconds = sum((connection.distance * 1000 / (connection.velocity_dict[connection.road_type] * 5/18)) for connection in final_roads)
        
        
        
        return (
            (
                (convert_time(total_time), total_time),
                round(total_distance, 2),
                connections,
                cities,
            )
            if interface == True
            else (
                convert_seconds(time_in_seconds)
                if option == "TIME"
                else total_distance
            )
        )
