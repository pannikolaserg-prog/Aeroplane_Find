import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AbstractFileSaver(ABC):
    def __init__(self, filename: str) -> None:
        self.filename = filename

    @abstractmethod
    def add_info_in_file(self, plane: Any) -> None:
        pass

    @abstractmethod
    def read_info_from_file(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_info_from_file(self) -> None:
        pass


class JSONFileSaver(AbstractFileSaver):
    def __init__(self, filename: str = "data/planes.json") -> None:
        super().__init__(filename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def add_info_in_file(self, plane: Any) -> None:
        try:
            # Читаем или создаем новый список
            try:
                with open(self.filename, "r") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            # Добавляем самолет
            plane_dict = {
                "country": plane.country,
                "callsign": plane.callsign,
                "speed": plane.speed,
                "geo_altitude": plane.geo_altitude,
            }

            if plane_dict not in data:
                data.append(plane_dict)

                # Сразу записываем
                with open(self.filename, "w") as f:
                    json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении в JSON: {e}")

    def read_info_from_file(self) -> List[Dict[str, Any]]:
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
        except Exception as e:
            print(f"Ошибка при чтении JSON: {e}")
            return []

    def delete_info_from_file(self) -> None:
        try:
            if os.path.exists(self.filename):
                os.remove(self.filename)
        except Exception as e:
            print(f"Ошибка при удалении JSON: {e}")


class XLSFileSaver(AbstractFileSaver):
    def __init__(self, filename: str = "data/planes.xls") -> None:
        super().__init__(filename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def add_info_in_file(self, plane: Any) -> None:
        try:
            with open(self.filename, "a") as f:
                f.write(f"{plane.country},{plane.callsign},{plane.speed},{plane.geo_altitude}\n")
        except Exception as e:
            print(f"Ошибка при сохранении в XLS: {e}")

    def read_info_from_file(self) -> List[Dict[str, Any]]:
        result = []
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 4:
                        try:
                            result.append(
                                {
                                    "country": parts[0],
                                    "callsign": parts[1],
                                    "speed": float(parts[2]),
                                    "geo_altitude": float(parts[3]),
                                }
                            )
                        except ValueError:
                            continue
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Ошибка при чтении XLS: {e}")
            return []
        return result

    def delete_info_from_file(self) -> None:
        try:
            if os.path.exists(self.filename):
                os.remove(self.filename)
        except Exception as e:
            print(f"Ошибка при удалении XLS: {e}")
