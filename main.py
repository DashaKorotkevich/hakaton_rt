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
    nav = Navigator(start_lat=45.15, start_lon=39.15)

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

    my_map.close()


if __name__ == "__main__":
    main()