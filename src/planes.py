class Plane:

    def __init__(self, country, callsign, speed, geo_altitude):
        self.country = self.__validate_str(country)
        self.callsign = self.__validate_str(callsign)
        self.speed = self.__validate_float(speed)
        self.geo_altitude = self.__validate_float(geo_altitude)

    def __ge__(self, other):
        if not isinstance(other, Plane):
            return NotImplemented
        return self.speed >= other.speed

    def __le__(self, other):
        if not isinstance(other, Plane):
            return NotImplemented
        return self.geo_altitude  <= other.geo_altitude


    @staticmethod
    def __validate_str(string):
        if not isinstance(string, str):
            country = "Не передано"
        else:
            string = string
        return string

    @staticmethod
    def __validate_float(my_float):
        if not isinstance(my_float, float | int):
            my_float = 0

        else:
            my_float = my_float
        return my_float