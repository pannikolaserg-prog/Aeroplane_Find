from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

import requests


class AbstractAdapter(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def _connect(self, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[requests.Response]:
        """Приватный метод подключения к API"""
        pass

    @abstractmethod
    def get_coordinates(self, country: str) -> Dict[str, float]:
        """Получает координаты страны"""
        pass

    @abstractmethod
    def get_aeroplanes(self, coordinates: Dict[str, float]) -> None:
        """Получает информацию о самолетах"""
        pass


class APIAdapter(AbstractAdapter):
    """Класс для работы с nominatim.openstreetmap и opensky-network"""

    def __init__(self) -> None:
        """Приватные атрибуты"""
        self.__aeroplanes: List[List[Any]] = []
        self.__nom_url: str = "https://nominatim.openstreetmap.org/search"
        self.__sky_url: str = "https://opensky-network.org/api/states/all"
        self.__session: requests.Session = requests.Session()
        self.__session.headers.update({"User-Agent": "AeroplanFind/1.0"})

    @property
    def aeroplanes(self) -> List[List[Any]]:
        """Геттер для приватного атрибута"""
        return self.__aeroplanes

    def _connect(self, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[requests.Response]:
        """
        Приватный метод подключения к API.
        Отправляет запрос и проверяет статус-код.
        """
        try:
            response: requests.Response = self.__session.get(url, params=params, timeout=10)

            # Проверка статус-кода
            if response.status_code == 200:
                return response
            else:
                print(f"Ошибка: статус {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            print("Ошибка: Таймаут запроса")
            return None
        except requests.exceptions.ConnectionError:
            print("Ошибка: Проблемы с подключением")
            return None
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return None

    def get_coordinates(self, country: str) -> Dict[str, float]:
        """Получает координаты страны от nominatim.openstreetmap"""
        # Вызываем метод подключения
        params: Dict[str, Union[str, int]] = {"q": country, "format": "json", "limit": 1}
        response: Optional[requests.Response] = self._connect(self.__nom_url, params)

        if response:
            try:
                data: List[Dict[str, Any]] = response.json()
                if data:
                    bbox: List[str] = data[0].get("boundingbox", [])
                    if len(bbox) == 4:
                        return {
                            "min_lat": float(bbox[0]),
                            "max_lat": float(bbox[1]),
                            "min_lon": float(bbox[2]),
                            "max_lon": float(bbox[3]),
                        }
            except (ValueError, KeyError, IndexError) as e:
                print(f"Ошибка при обработке координат: {e}")

        # Координаты по умолчанию
        return {"min_lat": 40.0, "max_lat": 50.0, "min_lon": 30.0, "max_lon": 40.0}

    def get_aeroplanes(self, coordinates: Dict[str, float]) -> None:
        """Получает информацию о самолетах от opensky-network"""
        params: Dict[str, float] = {
            "lamin": coordinates["min_lat"],
            "lamax": coordinates["max_lat"],
            "lomin": coordinates["min_lon"],
            "lomax": coordinates["max_lon"],
        }

        # Вызываем метод подключения
        response: Optional[requests.Response] = self._connect(self.__sky_url, params)

        if response:
            try:
                data: Dict[str, Any] = response.json()
                self.__aeroplanes = data.get("states", [])
                print(f"Получено {len(self.__aeroplanes)} самолетов")
            except (ValueError, KeyError) as e:
                print(f"Ошибка при обработке данных: {e}")
                self.__aeroplanes = []
        else:
            self.__aeroplanes = []
