from terrain import TerrainMap
from simulator import DroneSimulator
from navigator import Navigator
import matplotlib.pyplot as plt
import numpy as np


def plot_elevation_map(elevation_matrix):  # отображение карты по высотам
    """Отображает карту высот с цветовой шкалой"""
    fig, ax = plt.subplots(figsize=(12, 10))

    # Создаем цветовую карту от синего к красному
    cmap = plt.cm.RdYlBu_r

    # Отображаем матрицу высот
    im = ax.imshow(elevation_matrix, cmap=cmap, aspect='auto')

    # Добавляем цветовую шкалу
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Высота (м)', fontsize=12)

    # Настройки графика
    ax.set_title('Карта высот', fontsize=14)
    ax.set_xlabel('Колонки (пиксели)', fontsize=12)
    ax.set_ylabel('Строки (пиксели)', fontsize=12)

    plt.tight_layout()
    plt.show()

def main():
    elevation_arr_alimeter = [
        {'lat': 45.870537, 'lon': 39.126706, 'alt': 100.0},
        {'lat': 45.870414, 'lon': 39.126909, 'alt': 100.2},
        {'lat': 45.870290, 'lon': 39.127112, 'alt': 99.8},
        {'lat': 45.870167, 'lon': 39.127316, 'alt': 100.5},
        {'lat': 45.870044, 'lon': 39.127519, 'alt': 100.1},
        {'lat': 45.869922, 'lon': 39.127722, 'alt': 101.0},
        {'lat': 45.869860, 'lon': 39.127759, 'alt': 100.7},
        {'lat': 45.869798, 'lon': 39.127796, 'alt': 100.9},
        {'lat': 45.869737, 'lon': 39.127834, 'alt': 100.4},
        {'lat': 45.869675, 'lon': 39.127871, 'alt': 100.3},
        {'lat': 45.869613, 'lon': 39.127908, 'alt': 100.0},
        {'lat': 45.869504, 'lon': 39.127878, 'alt': 99.9},
        {'lat': 45.869394, 'lon': 39.127848, 'alt': 100.2},
        {'lat': 45.869285, 'lon': 39.127818, 'alt': 100.5},
        {'lat': 45.869176, 'lon': 39.127788, 'alt': 100.1}
    ]
    elevation_arr_alimeter2 = [
        {'lat': 45.49900, 'lon': 39.50100, 'alt': 105.2},
        {'lat': 45.49837, 'lon': 39.50190, 'alt': 104.8},
        {'lat': 45.49774, 'lon': 39.50280, 'alt': 105.5},
        {'lat': 45.49711, 'lon': 39.50370, 'alt': 106.1},
        {'lat': 45.49648, 'lon': 39.50460, 'alt': 105.9},
        {'lat': 45.49585, 'lon': 39.50550, 'alt': 106.4},
        {'lat': 45.49522, 'lon': 39.50640, 'alt': 107.0},
        {'lat': 45.49459, 'lon': 39.50730, 'alt': 106.8},
        {'lat': 45.49396, 'lon': 39.50820, 'alt': 107.2},
        {'lat': 45.49333, 'lon': 39.50910, 'alt': 107.5},
        {'lat': 45.49270, 'lon': 39.51000, 'alt': 108.1},
        {'lat': 45.49207, 'lon': 39.51090, 'alt': 107.9},
        {'lat': 45.49144, 'lon': 39.51180, 'alt': 108.3},
        {'lat': 45.49081, 'lon': 39.51270, 'alt': 108.7},
        {'lat': 45.49018, 'lon': 39.51360, 'alt': 109.0}
    ]
    dt = 0.05  # 20 Гц
    speed = 20.0
    # 1. Создаем массив для хранения высот с карты
    map_altitudes = []
    map_altitudes2 = []

    # 1. Инициализация
    try:
        my_map = TerrainMap("data/Copernicus_DSM_10_N45_00_E039_00_DEM.tif")
    except Exception as e:
        print(f"Ошибка загрузки карты: {e}")
        return

    # Получаем данные рельефа через атрибут src
    if hasattr(my_map, 'src'):
        # Читаем данные из src
        elevation_data = my_map.src.read(1)
        # Заменяем NoData на NaN если есть
        if my_map.src.nodata is not None:
            elevation_data[elevation_data == my_map.src.nodata] = np.nan
    else:
        # Пробуем другие варианты
        if hasattr(my_map, 'get_height'):
            # Если get_height - метод, получаем всю матрицу
            elevation_data = my_map.get_height()
        else:
            print("Не удалось получить данные рельефа")
            return

    # Визуализация карты высот
    plot_elevation_map(elevation_data)

    print(f"Границы карты (Left, Bottom, Right, Top): {my_map.src.bounds}")
    # 2. Проходим по каждой точке маршрута
    for point in elevation_arr_alimeter:
        # Используем наш метод, который мы спрятали в классе
        alt = my_map.get_altitude(point['lat'], point['lon'])
        map_altitudes.append(alt)

        print(f"Точка ({point['lat']:.5f}, {point['lon']:.5f}): хуйня сгенерированная ={point['alt']:.2f}м, высота с карты={alt:.2f}м")

    # Теперь map_altitudes - это список с высотами из .tif файла
    print("Список высот с карты:", map_altitudes)

    for point in elevation_arr_alimeter2:
        # Используем наш метод, который мы спрятали в классе
        alt = my_map.get_altitude(point['lat'], point['lon'])
        map_altitudes2.append(alt)

        print(f"Точка ({point['lat']:.5f}, {point['lon']:.5f}): хуйня сгенерированная ={point['alt']:.2f}м, высота с карты={alt:.2f}м")

    # Теперь map_altitudes - это список с высотами из .tif файла
    print("Список высот с карты:", map_altitudes2)



    my_map.close()

if __name__ == "__main__":
    main()