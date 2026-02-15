import json
import os

import pytest

from src.APIadapter import APIAdapter
from src.File_Saver import JSONFileSaver, XLSFileSaver
from src.planes import Plane
from src.utils import get_object_list


@pytest.mark.slow
def test_with_real_api() -> None:
    """Тест с реальным API (медленный)"""
    api = APIAdapter()
    coords = api.get_coordinates("Russia")
    api.get_aeroplanes(coords)

    planes = get_object_list({"states": api.aeroplanes})

    assert len(planes) > 0
    assert isinstance(planes[0], Plane)
    print(f"Найдено {len(planes)} самолетов")
    print(f"Первый: {planes[0]}")


@pytest.mark.skip(reason="Сначала сохраните данные в tests/fixtures/real_data.json")
def test_with_cached_data() -> None:
    """Тест с сохраненными реальными данными"""
    with open("tests/fixtures/real_data.json", "r") as f:
        real_data = json.load(f)

    planes = get_object_list({"states": real_data})
    assert len(planes) > 0
    print(f"Загружено {len(planes)} самолетов из кэша")


# ТЕСТЫ ДЛЯ JSON
def test_json_save_and_read(temp_file: str, plane: Plane) -> None:
    """Тест: сохранение и чтение JSON"""
    saver = JSONFileSaver(temp_file)
    saver.add_info_in_file(plane)

    assert os.path.exists(temp_file)

    data = saver.read_info_from_file()
    assert len(data) == 1
    assert data[0]["country"] == "Russia"
    assert data[0]["callsign"] == "TEST123"
    assert data[0]["speed"] == 250.5
    assert data[0]["geo_altitude"] == 10000.0


def test_json_no_duplicates(temp_file: str, plane: Plane) -> None:
    """Тест: нет дубликатов"""
    saver = JSONFileSaver(temp_file)

    saver.add_info_in_file(plane)
    saver.add_info_in_file(plane)

    data = saver.read_info_from_file()
    assert len(data) == 1


def test_json_delete(temp_file: str, plane: Plane) -> None:
    """Тест: удаление файла"""
    saver = JSONFileSaver(temp_file)
    saver.add_info_in_file(plane)
    assert os.path.exists(temp_file)

    saver.delete_info_from_file()
    assert not os.path.exists(temp_file)


def test_empty_file_read(temp_file: str) -> None:
    """Тест: чтение пустого/несуществующего файла"""
    saver = JSONFileSaver(temp_file)
    data = saver.read_info_from_file()
    assert data == []


def test_multiple_planes(temp_file: str) -> None:
    """Тест: несколько самолетов"""
    saver = JSONFileSaver(temp_file)

    p1 = Plane("Russia", "AFL101", 250, 10000)
    p2 = Plane("USA", "UAL202", 300, 12000)

    saver.add_info_in_file(p1)
    saver.add_info_in_file(p2)

    data = saver.read_info_from_file()
    assert len(data) == 2

    countries = [item["country"] for item in data]
    assert "Russia" in countries
    assert "USA" in countries


#  ТЕСТЫ ДЛЯ XLS
def test_xls_save_and_read(temp_xls: str, plane: Plane) -> None:
    """Тест: сохранение и чтение XLS"""
    saver = XLSFileSaver(temp_xls)

    saver.add_info_in_file(plane)
    assert os.path.exists(temp_xls)

    data = saver.read_info_from_file()
    assert len(data) == 1
    assert data[0]["country"] == "Russia"
    assert data[0]["callsign"] == "TEST123"


def test_xls_append(temp_xls: str) -> None:
    """Тест: добавление в существующий XLS файл"""
    saver = XLSFileSaver(temp_xls)

    p1 = Plane("Russia", "AFL101", 250, 10000)
    p2 = Plane("USA", "UAL202", 300, 12000)

    saver.add_info_in_file(p1)
    saver.add_info_in_file(p2)

    data = saver.read_info_from_file()
    assert len(data) == 2


def test_xls_read_empty(temp_xls: str) -> None:
    """Тест: чтение пустого XLS файла"""
    saver = XLSFileSaver(temp_xls)
    data = saver.read_info_from_file()
    assert data == []


# ТЕСТЫ ДЛЯ УТИЛИТ
def test_get_object_list_with_empty_data() -> None:
    """Тест: get_object_list с пустыми данными"""
    result = get_object_list({})
    assert result == []


def test_get_object_list_with_sample_data() -> None:
    """Тест: get_object_list с примером данных"""
    sample_data = {
        "states": [
            ["abc123", "AFL101", "Russia", 0, 0, 0, 0, 0, False, 250, 0, 0, None, 10000],
            ["def456", "UAL202", "USA", 0, 0, 0, 0, 0, False, 300, 0, 0, None, 12000],
        ]
    }

    result = get_object_list(sample_data)
    assert len(result) == 2
    assert result[0].country == "Russia"
    assert result[1].country == "USA"
