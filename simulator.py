import numpy as np
import math


class DroneSimulator:
    def __init__(self, start_lat, start_lon, speed_mps=15.0):
        # Характеристики дрона
        self.lat = start_lat
        self.lon = start_lon
        self.speed = speed_mps  # м/с
        self.alt_sensor_freq = 5.0  # Гц
        self.noise_level = 0.5  # метров погрешности

        # Состояние
        self.start_time = None

    def update_position(self, delta_time, bearing_deg):
        """
        Рассчитывает новые координаты на основе скорости и направления (bearing)
        """
        # Перевод скорости в изменение координат (грубая проекция)
        dist_meters = self.speed * delta_time

        lat_change = (dist_meters * math.cos(math.radians(bearing_deg))) / 111132
        lon_change = (dist_meters * math.sin(math.radians(bearing_deg))) / (111320 * math.cos(math.radians(self.lat)))

        self.lat += lat_change
        self.lon += lon_change

    def get_radio_altimeter(self, terrain_map):
        """Возвращает высоту с учетом шума радиовысотомера"""
        # Получаем пиксели из GPS
        px, py = ~terrain_map.transform * (self.lon, self.lat)
        true_height = terrain_map.get_height(px, py) or 0.0

        # Накладываем шум сенсора
        noise = np.random.normal(0, self.noise_level)
        return true_height + noise