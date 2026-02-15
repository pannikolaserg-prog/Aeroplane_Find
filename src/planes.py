from typing import Any


class Plane:
    """Класс для работы с данными о самолетах"""

    # 👇 ДОБАВЛЯЕМ __slots__ для экономии памяти
    __slots__ = ("country", "callsign", "speed", "geo_altitude")

    def __init__(self, country: Any, callsign: Any, speed: Any, geo_altitude: Any) -> None:
        self.country: str = self._validate_str(country, "Не передано")
        self.callsign: str = self._validate_str(callsign, "Не передано")
        self.speed: float = self._validate_float(speed, 0.0)
        self.geo_altitude: float = self._validate_float(geo_altitude, 0.0)

    # 👇 ДОБАВЛЯЕМ ВСЕ МЕТОДЫ СРАВНЕНИЯ ПО ВЫСОТЕ
    def __eq__(self, other: Any) -> bool:
        """Сравнение на равенство по высоте"""
        if not isinstance(other, Plane):
            return NotImplemented
        return self.geo_altitude == other.geo_altitude

    def __ne__(self, other: Any) -> bool:
        """Сравнение на неравенство по высоте"""
        if not isinstance(other, Plane):
            return NotImplemented
        return self.geo_altitude != other.geo_altitude

    def __lt__(self, other: Any) -> bool:
        """Меньше по высоте"""
        if not isinstance(other, Plane):
            return NotImplemented
        return self.geo_altitude < other.geo_altitude

    def __le__(self, other: Any) -> bool:
        """Меньше или равно по высоте"""
        if not isinstance(other, Plane):
            return NotImplemented
        return self.geo_altitude <= other.geo_altitude

    def __gt__(self, other: Any) -> bool:
        """Больше по высоте"""
        if not isinstance(other, Plane):
            return NotImplemented
        return self.geo_altitude > other.geo_altitude

    def __ge__(self, other: Any) -> bool:
        """Больше или равно по высоте"""
        if not isinstance(other, Plane):
            return NotImplemented
        return self.geo_altitude >= other.geo_altitude

    def __str__(self) -> str:
        """Возвращает строку с основными данными о самолетах"""
        return f"Plane({self.country}, {self.callsign}, {self.speed}, {self.geo_altitude})"

    @staticmethod
    def _validate_str(value: Any, default: str) -> str:
        """
        Преобразует value в строку.
        Если value = None, возвращает default.
        """
        return str(value) if value is not None else default

    @staticmethod
    def _validate_float(value: Any, default: float) -> float:
        """
        Преобразует value в число.
        Если ошибка или value = None, возвращает default.
        """
        try:
            return float(value) if value is not None else default
        except (TypeError, ValueError):
            return default
