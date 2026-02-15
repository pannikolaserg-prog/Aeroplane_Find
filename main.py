import os
from src.APIadapter import APIAdapter
from src.planes import Plane
from src.File_Saver import FileSaver


def main():
    print("ПОИСК САМОЛЕТОВ")

    # Получаем данные
    api = APIAdapter()
    country = input("Страна (например: Russia, USA, Germany): ")

    coordinates = api.get_coordinates(country)
    api.get_aeroplanes(coordinates)

    # Создаем список самолетов
    planes = []
    for p in api.aeroplanes["states"]:
        planes.append(Plane(p[1], p[2], p[9], p[13]))

    print(f"Найдено: {len(planes)}")

    if not os.path.exists("data"):
        os.makedirs("data")

    saver = FileSaver("data/planes.json")

    # СОЗДАЕМ ПЕРЕМЕННУЮ
    current_results = []

    while True:
        print("\n1. Все самолеты")
        print("2. Топ N по высоте")
        print("3. Топ N по скорости")
        print("4. Поиск по стране регистрации (Примеры: Russia, USA, Germany, France, China, UK)")
        print("5. Диапазон высот")
        print("6. Сохранить найденное в файл")
        print("7. Выход")

        cmd = input("> ")

        if cmd == "1":
            for p in planes[:10]:
                print(f"{p.country} | Высота: {p.geo_altitude}")
            current_results = planes  # СОХРАНЯЕМ ВСЕ

        elif cmd == "2":
            n = int(input("N: "))
            top = sorted(planes, key=lambda x: x.geo_altitude, reverse=True)[:n]
            for i, p in enumerate(top, 1):
                print(f"{i}. {p.country} - {p.geo_altitude}")
            current_results = top

        elif cmd == "3":
            n = int(input("N: "))
            # Сортируем по скорости (от большей к меньшей)
            top_speed = sorted(planes, key=lambda x: x.speed, reverse=True)[:n]
            print(f"\nТОП-{n} ПО СКОРОСТИ:")
            print("-" * 60)
            for i, p in enumerate(top_speed, 1):
                print(f"{i}. {p.country} | {p.callsign} | Скорость: {p.speed} м/с | Высота: {p.geo_altitude}м")
            current_results = top_speed

        elif cmd == "4":
            f = input("Страна: ")
            found = [p for p in planes if p.country and f.lower() in p.country.lower()]
            print(f"\nНайдено: {len(found)}")

            for p in found[:10]:
                print(f"{p.callsign} | {p.country} | {p.geo_altitude}м")

            if not found:
                print("Ничего не найдено. Попробуйте:")
                print("Russia, USA, Germany, France, China, UK")

            current_results = found  # СОХРАНЯЕМ НАЙДЕННЫЕ

        elif cmd == "5":
            try:
                min_h = float(input("Высота ОТ (м): "))
                max_h = float(input("Высота ДО (м): "))
                range_planes = [p for p in planes if min_h <= p.geo_altitude <= max_h]
                print(f"\nСамолеты на высоте {min_h}-{max_h}м: {len(range_planes)}")

                for p in range_planes[:10]:
                    print(f"{p.callsign} | {p.country} | {p.geo_altitude}м")

                current_results = range_planes  # СОХРАНЯЕМ ПО ДИАПАЗОНУ

            except:
                print("Ошибка! Введите числа")

        elif cmd == "6":
            if current_results:
                # Очищаем файл перед сохранением
                if os.path.exists("data/planes.json"):
                    os.remove("data/planes.json")

                # Создаем новый saver
                saver = FileSaver("data/planes.json")

                # Сохраняем текущие результаты
                for p in current_results:
                    saver.add_info_in_file(p)

                print(f"Сохранено {len(current_results)} самолетов в data/planes.json")
            else:
                print("Сначала найдите самолеты (пункты 1-4)")

        elif cmd == "7":
            print("До свидания!")
            break

        else:
            print("❌ Неверный пункт. Введите 1-7")


if __name__ == "__main__":
    main()