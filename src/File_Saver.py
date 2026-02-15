import json
from abc import ABC, abstractmethod
from json import JSONDecodeError
from typing import Any, Dict, List


class AbstractFileSaver(ABC):
    """Абстрактный базовый класс для работы с файлами"""
    def __init__(self, filename: str) -> None:
        self.filename: str = filename

    @abstractmethod
    def add_info_in_file(self, plane: Any) -> None:
        """Добавить данные в файл"""
        pass

    @abstractmethod
    def read_info_from_file(self) -> List[Dict[str, Any]]:
        """Прочитать данные из файла"""
        pass

    @abstractmethod
    def delete_info_from_file(self) -> None:
        """Удалить данные из файла"""
        pass


class FileSaver(AbstractFileSaver):
    """Класс для работы с файлом"""
    def __init__(self, filename: str) -> None:
        super().__init__(filename)

    def add_info_in_file(self, plane: Any) -> None:
        """Добавить данные о самолетах в файл"""
        try:
            with open(self.filename, "a+", encoding="UTF-8") as file:
                file.seek(0)

                # Читаем существующие данные
                try:
                    data = json.load(file)
                except JSONDecodeError:
                    data = []

                # Создаем словарь самолета
                plane_dict = {
                    "country": plane.country,
                    "callsign": plane.callsign,
                    "speed": plane.speed,
                    "geo_altitude": plane.geo_altitude,
                }

                # Добавляем если такого еще нет
                if plane_dict not in data:
                    data.append(plane_dict)

                # Перезаписываем файл
                file.seek(0)
                file.truncate()
                json.dump(data, file, ensure_ascii=False, indent=4)

        except FileNotFoundError:
            pass

    def read_info_from_file(self) -> List[Dict[str, Any]]:
        """Прочитать данные о самолетах в файле"""
        try:
            with open(self.filename, "r", encoding="UTF-8") as file:
                try:
                    return json.load(file)
                except JSONDecodeError:
                    return []
        except FileNotFoundError:
            return []

    def delete_info_from_file(self) -> None:
        """Удалить данные о самолетах из файла"""
        import os

        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass
