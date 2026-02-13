import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from json import JSONDecodeError


class AbstractFileSaver(ABC):
    def __init__(self, filename: str) -> None:
        self.filename: str = filename

    @abstractmethod
    def add_info_in_file(self, plane: Any) -> None:
        pass

    @abstractmethod
    def read_info_from_file(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_info_from_file(self) -> None:
        pass


class FileSaver(AbstractFileSaver):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)

    def add_info_in_file(self, plane: Any) -> None:
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
                    "geo_altitude": plane.geo_altitude
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
        try:
            with open(self.filename, "r", encoding="UTF-8") as file:
                try:
                    return json.load(file)
                except JSONDecodeError:
                    return []
        except FileNotFoundError:
            return []

    def delete_info_from_file(self) -> None:
        """Удаляет файл"""
        import os
        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass