from math import inf
from source.infrastructure import Connection
from source.infrastructure import City

if __name__ == "__main__":

    city = City("A", "A", 21.37, 22.34)
    print(city.name)

    connection = Connection("A", "A", "W", "W", 90)

    print(connection.calculate_time())
