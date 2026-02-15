from typing import Any, Dict, List

from src.planes import Plane
from src.utils import get_object_list


def test_returns_list_of_planes() -> None:
    """Тест: возвращает список объектов Plane"""
    data: Dict[str, Any] = {
        "states": [
            ["id1", "AFL101", "Russia", 0, 0, 0, 0, 0, False, 250.5, 0, 0, None, 10000.0],
            ["id2", "UAL202", "USA", 0, 0, 0, 0, 0, False, 300.7, 0, 0, None, 12000.0],
        ]
    }

    result: List[Plane] = get_object_list(data)

    assert len(result) == 2
    assert isinstance(result[0], Plane)
    assert result[0].country == "Russia"
    assert result[0].callsign == "AFL101"
    assert result[0].speed == 250.5
    assert result[0].geo_altitude == 10000.0


def test_empty_data() -> None:
    """Тест: пустые данные"""
    data: Dict[str, Any] = {"states": []}
    result: List[Plane] = get_object_list(data)
    assert result == []


def test_missing_states_key() -> None:
    """Тест: нет ключа states"""
    data: Dict[str, Any] = {}
    result: List[Plane] = get_object_list(data)
    assert result == []
