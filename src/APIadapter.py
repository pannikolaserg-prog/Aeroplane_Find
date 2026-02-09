import json
from abc import ABC, abstractmethod

import requests


class AbstractAdapter(ABC):

    @abstractmethod
    def get_aeroplanes(self, country: str) -> None:
        pass

class APIAdapter(AbstractAdapter):
    def __init__(self):
        self.openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
        self.opensky_url = 'https://opensky-network.org/api'
        self.aeroplanes = None
    def get_aeroplanes(self, country: str) -> None:
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

        return json.dumps(data, indent=4)

test = APIAdapter()
print(test.get_aeroplanes("Russia"))