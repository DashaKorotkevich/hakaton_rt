from terrain import TerrainMap


def main():
    # 1. Инициализация
    try:
        my_map = TerrainMap("data/Copernicus_DSM_10_N45_00_E039_00_DEM.tif")
    except Exception as e:
        print(f"Ошибка загрузки карты: {e}")
        return

    # Вывод информации о карте (используем обновленный метод)
    print("--- Информация о карте ---")
    my_map.inspect_file()

    # 2. Имитация полета по прямой (проверка высот в точках)
    print("\n--- Имитация полета ---")
    start_x, start_y = 0, 0
    for i in range(5):
        x, y = start_x + i * 20, start_y + i * 20
        h = my_map.get_height(x, y)
        lat, lon = my_map.get_latlon(x, y)
        print(f"Точка {i}: ({lat:.4f}, {lon:.4f}), высота рельефа: {h if h else 0.0:.1f} м")



    # 4. Освобождение ресурсов
    my_map.close()
    print("\nПолет завершен.")


if __name__ == "__main__":
    main()