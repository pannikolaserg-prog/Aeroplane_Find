import json
from abc import ABC, abstractmethod

import requests


class AbstractAdapter(ABC):

    @abstractmethod
    def get_coordinates(self, country):
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> None:
        pass

class APIAdapter(AbstractAdapter):

    def __init__(self):
        self.openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
        self.opensky_url = 'https://opensky-network.org/api/states/all'
        self.aeroplanes = None

    def get_coordinates(self, country):

        headers_nominatim = {
            'User-Agent': 'test-app/1.0',
        }

        params_nominatim = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }

        response = requests.get(url=self.openstreetmap_url, params=params_nominatim, headers=headers_nominatim)

        data = response.json()

        # Получаем bounding box
        geo_coordinates = data[0].get("boundingbox")

        return geo_coordinates

    def get_aeroplanes(self, coordinates: list) -> None:

        params = {
            'lamin': coordinates[0],
            'lamax': coordinates[1],
            'lomin': coordinates[2],
            'lomax': coordinates[3],
        }

        response = requests.get(url=self.opensky_url, params=params)

        self.aeroplanes = response.json()


test = APIAdapter()
coordinates = test.get_coordinates("Russia")
test.get_aeroplanes(coordinates)

