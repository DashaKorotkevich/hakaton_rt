from terrain import TerrainMap
from simulator import DroneSimulator
import time

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

    # Инициализируем дрон в стартовой точке
    drone = DroneSimulator(start_lat=45.15, start_lon=39.15, speed_mps=20.0)

    print("--- Полет начат ---")
    dt = 1.0  # 1 секунда шага симуляции

    for i in range(20):
        # 1. Командуем дрону двигаться (например, на Север - 0 градусов)
        drone.update_position(delta_time=dt, bearing_deg=0)

        # 2. Опрашиваем сенсоры дрона
        alt = drone.get_radio_altimeter(my_map)

        print(f"Время: {i}с | Позиция: {drone.lat:.4f}, {drone.lon:.4f} | Высота (радио): {alt:.2f} м")
        time.sleep(0.1)

    # 4. Освобождение ресурсов
    my_map.close()
    print("\nПолет завершен.")


if __name__ == "__main__":
    main()