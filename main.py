import os
from src.APIadapter import APIAdapter
from src.planes import Plane
from src.File_Saver import JSONFileSaver, XLSFileSaver


def main():
    print("ПОИСК САМОЛЕТОВ")

    # Получаем данные
    api = APIAdapter()
    country = input("Страна (например: Russia, USA, Germany): ")

    coordinates = api.get_coordinates(country)
    api.get_aeroplanes(coordinates)

    # Создаем список самолетов
    planes = []
    for p in api.aeroplanes:
        planes.append(Plane(p[1], p[2], p[9], p[13]))

    print(f"Найдено: {len(planes)}")

    # Создаем папку data
    if not os.path.exists("data"):
        os.makedirs("data")

    json_saver = JSONFileSaver("data/planes.json")
    xls_saver = XLSFileSaver("data/planes.xls")

    # Переменная для хранения результатов последнего поиска
    current_results = []

    while True:
        print("\n1. Все самолеты")
        print("2. Топ N по высоте")
        print("3. Топ N по скорости")
        print("4. Поиск по стране регистрации")
        print("5. Диапазон высот")
        print("6. Сохранить найденное в файл")
        print("7. Выход")

        cmd = input("> ")

        if cmd == "1":
            for p in planes[:10]:
                print(f"{p.country} | Скорость: {p.speed} | Высота: {p.geo_altitude}")
            current_results = planes

        elif cmd == "2":
            n = int(input("N: "))
            top = sorted(planes, key=lambda x: x.geo_altitude, reverse=True)[:n]
            print(f"\nТОП-{n} ПО ВЫСОТЕ:")
            for i, p in enumerate(top, 1):
                print(f"{i}. {p.country} | {p.callsign} | Высота: {p.geo_altitude}м | Скорость: {p.speed}м/с")
            current_results = top

        elif cmd == "3":
            n = int(input("N: "))
            top_speed = sorted(planes, key=lambda x: x.speed, reverse=True)[:n]
            print(f"\nТОП-{n} ПО СКОРОСТИ:")
            for i, p in enumerate(top_speed, 1):
                print(f"{i}. {p.country} | {p.callsign} | Скорость: {p.speed} м/с | Высота: {p.geo_altitude}м")
            current_results = top_speed

        elif cmd == "4":
            f = input("Страна: ")
            found = [p for p in planes if p.country and f.lower() in p.country.lower()]
            print(f"\nНайдено самолетов из {f}: {len(found)}")

            for p in found[:10]:
                print(f"{p.callsign} | {p.country} | Скорость: {p.speed}м/с | Высота: {p.geo_altitude}м")

            if not found:
                print("Ничего не найдено. Попробуйте:")
                print("Russia, USA, Germany, France, China, UK")

            current_results = found

        elif cmd == "5":
            try:
                min_h = float(input("Высота ОТ (м): "))
                max_h = float(input("Высота ДО (м): "))
                range_planes = [p for p in planes if min_h <= p.geo_altitude <= max_h]
                print(f"\nСамолеты на высоте {min_h}-{max_h}м: {len(range_planes)}")

                for p in range_planes[:10]:
                    print(f"{p.callsign} | {p.country} | Высота: {p.geo_altitude}м | Скорость: {p.speed}м/с")

                current_results = range_planes

            except:
                print("Ошибка! Введите числа")

        elif cmd == "6":
            if current_results:
                # Очищаем файлы перед сохранением
                if os.path.exists("data/planes.json"):
                    os.remove("data/planes.json")
                if os.path.exists("data/planes.xls"):
                    os.remove("data/planes.xls")

                # 👇 СОХРАНЯЕМ В ОБА ФАЙЛА
                for p in current_results:
                    json_saver.add_info_in_file(p)
                    xls_saver.add_info_in_file(p)

                print(f"Сохранено {len(current_results)} самолетов:")
                print(f"   - JSON: data/planes.json")
                print(f"   - XLS: data/planes.xls")
            else:
                print("Сначала найдите самолеты (пункты 1-5)")

        elif cmd == "7":
            print("До свидания!")
            break

        else:
            print("Неверный пункт. Введите 1-7")


if __name__ == "__main__":
    main()