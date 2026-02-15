import os
import tempfile

from src.File_Saver import JSONFileSaver, XLSFileSaver
from src.planes import Plane
from src.utils import get_object_list


def test_json_file_exists():
    """Тест: проверяем что JSON файл существует"""
    assert os.path.exists("data/planes.json"), "Файл data/planes.json не найден"


def test_xls_file_exists():
    """Тест: проверяем что XLS файл существует"""
    assert os.path.exists("data/planes.xls"), "Файл data/planes.xls не найден"


def test_read_json():
    """Тест: читаем JSON файл"""
    saver = JSONFileSaver("data/planes.json")
    data = saver.read_info_from_file()
    print(f"\nВ JSON файле {len(data)} записей")
    assert isinstance(data, list)


def test_read_xls():
    """Тест: читаем XLS файл"""
    saver = XLSFileSaver("data/planes.xls")
    data = saver.read_info_from_file()
    print(f"\nВ XLS файле {len(data)} записей")
    assert isinstance(data, list)


def test_add_test_plane():
    """Тест: добавляем тестовый самолет"""
    saver = JSONFileSaver("data/planes.json")
    test_plane = Plane("Test", "TEST123", 100, 5000)

    before = len(saver.read_info_from_file())
    saver.add_info_in_file(test_plane)
    after = len(saver.read_info_from_file())

    print(f"\nБыло: {before}, стало: {after}")
    assert after >= before


def test_utils_with_sample_data():
    """Тест: утилита get_object_list"""
    data = {
        "states": [
            ["id1", "SU100", "Russia", 0, 0, 0, 0, 0, False, 250, 0, 0, None, 10000],
        ]
    }
    planes = get_object_list(data)
    assert len(planes) == 1
    assert planes[0].country == "Russia"


def test_delete_info_from_file():
    """Тест: удаление файла"""
    # Создаем временный файл для теста
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp_path = tmp.name

    saver = JSONFileSaver(tmp_path)
    test_plane = Plane("Test", "DEL123", 100, 5000)
    saver.add_info_in_file(test_plane)

    assert os.path.exists(tmp_path)
    saver.delete_info_from_file()
    assert not os.path.exists(tmp_path)


def test_delete_nonexistent_file():
    """Тест: удаление несуществующего файла (не должно быть ошибки)"""
    saver = JSONFileSaver("data/never_created.json")
    saver.delete_info_from_file()  # Просто не должно упасть
    assert True


def test_add_duplicate_plane():
    """Тест: добавление дубликата не должно увеличивать файл"""
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp_path = tmp.name

    saver = JSONFileSaver(tmp_path)
    test_plane = Plane("Test", "DUP123", 100, 5000)

    saver.add_info_in_file(test_plane)
    first_count = len(saver.read_info_from_file())

    saver.add_info_in_file(test_plane)
    second_count = len(saver.read_info_from_file())

    assert first_count == second_count == 1

    # Очистка
    os.unlink(tmp_path)


def test_read_corrupted_json():
    """Тест: чтение поврежденного JSON файла"""
    # Создаем поврежденный JSON
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as tmp:
        tmp.write("Это не JSON")
        tmp_path = tmp.name

    saver = JSONFileSaver(tmp_path)
    data = saver.read_info_from_file()
    assert data == []

    # Очистка
    os.unlink(tmp_path)


def test_xls_with_invalid_lines():
    """Тест: XLS с некорректными строками"""
    # Создаем XLS с плохими данными
    with tempfile.NamedTemporaryFile(suffix=".xls", delete=False, mode="w") as tmp:
        tmp.write("Russia,SU100,250,10000\n")
        tmp.write("это неверная строка\n")
        tmp.write("France,AF200,abc,12000\n")  # скорость не число
        tmp_path = tmp.name

    saver = XLSFileSaver(tmp_path)
    data = saver.read_info_from_file()

    # Должна прочитаться только первая строка
    assert len(data) == 1
    assert data[0]["country"] == "Russia"

    # Очистка
    os.unlink(tmp_path)