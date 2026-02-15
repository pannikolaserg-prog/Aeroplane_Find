import pytest

from src.planes import Plane


@pytest.fixture
def plane1() -> Plane:
    """Фикстура: первый самолет"""
    return Plane("Russia", "AFL101", 250.5, 10000.0)


@pytest.fixture
def plane2() -> Plane:
    """Фикстура: второй самолет"""
    return Plane("USA", "UAL202", 300.7, 12000.0)


@pytest.fixture
def plane3() -> Plane:
    """Фикстура: третий самолет (такая же высота как у plane1)"""
    return Plane("France", "AFR303", 280.3, 10000.0)


class TestPlaneCreation:
    """Тесты создания самолета"""

    def test_create_plane_with_valid_data(self) -> None:
        """Тест: создание с валидными данными"""
        p: Plane = Plane("Germany", "DLH456", 350.2, 11000.5)

        assert p.country == "Germany"
        assert p.callsign == "DLH456"
        assert p.speed == 350.2
        assert p.geo_altitude == 11000.5

    def test_create_plane_with_none_values(self) -> None:
        """Тест: создание с None значениями"""
        p: Plane = Plane(None, None, None, None)

        assert p.country == "Не передано"
        assert p.callsign == "Не передано"
        assert p.speed == 0.0
        assert p.geo_altitude == 0.0


class TestPlaneComparison:
    """Тесты сравнения самолетов"""

    def test_equal_height(self, plane1: Plane, plane3: Plane) -> None:
        """Тест: равенство по высоте"""
        assert (plane1 == plane3) is True
        assert (plane1 != plane3) is False

    def test_not_equal_height(self, plane1: Plane, plane2: Plane) -> None:
        """Тест: неравенство по высоте"""
        assert (plane1 == plane2) is False
        assert (plane1 != plane2) is True

    def test_less_than(self, plane1: Plane, plane2: Plane) -> None:
        """Тест: меньше по высоте"""
        assert (plane1 < plane2) is True
        assert (plane2 < plane1) is False

    def test_less_or_equal(self, plane1: Plane, plane2: Plane, plane3: Plane) -> None:
        """Тест: меньше или равно по высоте"""
        assert (plane1 <= plane2) is True
        assert (plane1 <= plane3) is True
        assert (plane2 <= plane1) is False

    def test_greater_than(self, plane1: Plane, plane2: Plane) -> None:
        """Тест: больше по высоте"""
        assert (plane2 > plane1) is True
        assert (plane1 > plane2) is False

    def test_greater_or_equal(self, plane1: Plane, plane2: Plane, plane3: Plane) -> None:
        """Тест: больше или равно по высоте"""
        assert (plane2 >= plane1) is True
        assert (plane3 >= plane1) is True
        assert (plane1 >= plane2) is False


class TestPlaneValidation:
    """Тесты валидации данных"""

    def test_validate_str_with_valid_value(self) -> None:
        """Тест: валидация строки с корректным значением"""
        result: str = Plane._validate_str("test", "default")
        assert result == "test"

    def test_validate_str_with_none(self) -> None:
        """Тест: валидация строки с None"""
        result: str = Plane._validate_str(None, "default")
        assert result == "default"

    def test_validate_str_with_number(self) -> None:
        """Тест: валидация строки с числом"""
        result: str = Plane._validate_str(123, "default")
        assert result == "123"

    def test_validate_float_with_valid_number(self) -> None:
        """Тест: валидация числа с корректным значением"""
        result: float = Plane._validate_float(123.45, 0.0)
        assert result == 123.45

    def test_validate_float_with_string_number(self) -> None:
        """Тест: валидация числа со строкой-числом"""
        result: float = Plane._validate_float("123.45", 0.0)
        assert result == 123.45

    def test_validate_float_with_none(self) -> None:
        """Тест: валидация числа с None"""
        result: float = Plane._validate_float(None, 5.5)
        assert result == 5.5

    def test_validate_float_with_invalid_string(self) -> None:
        """Тест: валидация числа с некорректной строкой"""
        result: float = Plane._validate_float("abc", 7.7)
        assert result == 7.7


class TestPlaneString:
    """Тесты строкового представления"""

    def test_str_method(self, plane1: Plane) -> None:
        """Тест: метод __str__"""
        result: str = str(plane1)
        expected: str = "Plane(Russia, AFL101, 250.5, 10000.0)"
        assert result == expected

    def test_str_with_default_values(self) -> None:
        """Тест: __str__ со значениями по умолчанию"""
        p: Plane = Plane(None, None, None, None)
        result: str = str(p)
        expected: str = "Plane(Не передано, Не передано, 0.0, 0.0)"
        assert result == expected


class TestPlaneSlots:
    """Тесты __slots__"""

    def test_slots_defined(self) -> None:
        """Тест: __slots__ определены правильно"""
        assert Plane.__slots__ == ("country", "callsign", "speed", "geo_altitude")
