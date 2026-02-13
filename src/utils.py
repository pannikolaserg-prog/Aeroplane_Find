from typing import List, Dict, Any
from src.planes import Plane


def get_object_list(planes_information: Dict[str, Any]) -> List[Plane]:
    """
    Создает список объектов Plane из данных API OpenSky.

    Args:
        planes_information: Словарь с данными о самолетах от OpenSky API

    Returns:
        List[Plane]: Список объектов самолетов
    """
    object_list = []

    for plane in planes_information.get("states", []):
        # Индексы из API OpenSky: [2] - страна, [1] - позывной, [9] - скорость, [13] - высота
        obj = Plane(
            country=plane[2],  # страна
            callsign=plane[1],  # позывной
            speed=plane[9],  # скорость
            geo_altitude=plane[13]  # высота
        )
        object_list.append(obj)

    return object_list