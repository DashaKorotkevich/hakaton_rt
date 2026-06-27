from terrain import TerrainMap
from simulator import DroneSimulator
from navigator import Navigator
import matplotlib.pyplot as plt
import numpy as np


def calculate_total_steps(duration_sec, dt):
    """Вычисляет количество итераций для заданного времени и шага."""
    return int(duration_sec / dt)


def main():
    # 1. Инициализация
    try:
        my_map = TerrainMap("data/Copernicus_DSM_10_N45_00_E039_00_DEM.tif")
    except Exception as e:
        print(f"Ошибка загрузки карты: {e}")
        return

    # Инициализация дрона и навигатора
    drone = DroneSimulator(start_lat=45.15, start_lon=39.15, speed_mps=20.0)
    nav = Navigator(start_lat=45.15, start_lon=39.15, speed_mps=20.0)

    print("--- Полет начат ---")

    dt = 0.05  # 20 Гц
    flight_time_sec = 120  # время полета в секунд
    total_steps = calculate_total_steps(flight_time_sec, dt)

    for i in range(total_steps):
        # 1. Движение
        drone.update_position(delta_time=dt, bearing_deg=0)

        # 2. Опрос датчика
        alt = drone.get_radio_altimeter(my_map)

        # Передаем только значение высоты
        print(f"Срабатывание: {i} | Позиция: {drone.lat:.4f}, {drone.lon:.4f} | Высота (радио): {alt:.2f} м")
        nav.add_measurement(alt)

        if i % 20 == 0 and i != 0:
            # Рассчет размера квадрата, где может находится дрон, мы его каждую сек вызывать будем
            size = nav.get_optimal_patch_size_px(my_map.px_w_m)
            # Получаем матрицу высот (наш "кусочек" карты)
            patch = my_map.get_patch_by_latlon(nav.lat, nav.lon, size)
            print(f"Сверка: область {size}x{size} пикселей получена. Размер данных: {patch.shape}")
            # Вызвали "интеллект" навигатора для поиска совпадения
            best_pos, error = nav.find_best_match(patch, nav.second_buffer)
            print(f"Лучшее совпадение в патче: {best_pos}, Ошибка: {error:.2f}")
            get_latlon_from_pixel(best_pos, my_map)
            new_lat, new_lon = my_map.pixel_to_latlon(best_pos[0], best_pos[1], window_row, window_col)
            print(f"Коррекция позиции: было ({nav.lat:.4f}, {nav.lon:.4f}), стало ({new_lat:.4f}, {new_lon:.4f})")

    my_map.close()


if __name__ == "__main__":
    main()