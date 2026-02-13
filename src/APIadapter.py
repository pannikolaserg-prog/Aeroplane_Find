import json
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Tuple

import requests


class AbstractAdapter(ABC):
    """Абстрактный базовый класс для адаптера API"""

    @abstractmethod
    def get_coordinates(self, country: str) -> List[str]:
        """Получить координаты bounding box для страны"""
        pass

    @abstractmethod
    def get_aeroplanes(self, coordinates: List[str]) -> Optional[Dict[str, Any]]:
        """Получить информацию о самолетах в заданных координатах"""
        pass


class APIAdapter(AbstractAdapter):
    """Адаптер для работы с OpenStreetMap и OpenSky Network API"""

    def __init__(self) -> None:
        self.openstreetmap_url: str = 'https://nominatim.openstreetmap.org/search'
        self.opensky_url: str = 'https://opensky-network.org/api/states/all'
        self.aeroplanes: Optional[Dict[str, Any]] = None

        # Заголовки для Nominatim API (требуются для соблюдения политики использования)
        self.nominatim_headers: Dict[str, str] = {
            'User-Agent': 'test-app/1.0',
        }

    def get_coordinates(self, country: str) -> List[str]:
        """
        Получить bounding box координаты для указанной страны

        Args:
            country: Название страны

        Returns:
            List[str]: Список координат [min_lat, max_lat, min_lon, max_lon]

        Raises:
            requests.RequestException: При ошибке запроса
            IndexError: Если страна не найдена
        """
        params: Dict[str, Any] = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }

        try:
            response = requests.get(
                url=self.openstreetmap_url,
                params=params,
                headers=self.nominatim_headers,
                timeout=10
            )
            response.raise_for_status()

            data: List[Dict[str, Any]] = response.json()

            if not data:
                raise ValueError(f"Страна '{country}' не найдена")

            # Получаем bounding box
            geo_coordinates: List[str] = data[0].get("boundingbox", [])
            return geo_coordinates

        except requests.RequestException as e:
            print(f"Ошибка при запросе к Nominatim API: {e}")
            raise
        except (KeyError, IndexError) as e:
            print(f"Ошибка при обработке ответа от Nominatim API: {e}")
            raise

    def get_aeroplanes(self, coordinates: List[str]) -> Optional[Dict[str, Any]]:
        """
        Получить информацию о самолетах в заданных координатах

        Args:
            coordinates: Список координат [min_lat, max_lat, min_lon, max_lon]

        Returns:
            Optional[Dict[str, Any]]: Информация о самолетах или None при ошибке
        """
        if len(coordinates) < 4:
            raise ValueError("Недостаточно координат. Требуется 4 значения: [min_lat, max_lat, min_lon, max_lon]")

        params: Dict[str, float] = {
            'lamin': float(coordinates[0]),
            'lamax': float(coordinates[1]),
            'lomin': float(coordinates[2]),
            'lomax': float(coordinates[3]),
        }

        try:
            response = requests.get(
                url=self.opensky_url,
                params=params,
                timeout=10
            )
            response.raise_for_status()

            self.aeroplanes = response.json()
            return self.aeroplanes

        except requests.RequestException as e:
            print(f"Ошибка при запросе к OpenSky API: {e}")
            self.aeroplanes = None
            return None
        except ValueError as e:
            print(f"Ошибка при преобразовании координат: {e}")
            self.aeroplanes = None
            return None