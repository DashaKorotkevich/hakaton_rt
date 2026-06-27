import math
import numpy as np

class Navigator:
    def __init__(self, start_lat, start_lon, speed_mps):

        self.elevationArrAlimeter = [
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

        # Сохраняем координаты
        self.lat = start_lat
        self.lon = start_lon

        self.speed_mps = speed_mps  # Скорость дрона (м/с) для рассчета размера квадрата в м

        # История полета
        # Каждый элемент: {'lat': float, 'lon': float, 'course': float, 'alt': float}
        self.history = []
        self.second_buffer = []

        self.all_minute_packets = []  # История для минут (1200 точек)
        self.all_second_packets = []  # История для секунд (20 точек)

        self.second_buffer = []  # Текущий буфер на 1 сек
        self.minute_buffer = []  # Текущий буфер на 1 мин

    def add_measurement(self, height): # работа с пакетами (радиовысотометром)
        self.second_buffer.append(height)
        self.minute_buffer.append(height)

        # 1. Проверка на секунду (20 записей)
        if len(self.second_buffer) == 20:
            packet = list(self.second_buffer)
            self.all_second_packets.append(packet)
            print(f"--- Пакет за секунду готов: {len(packet)} записей ---")
            self.second_buffer = []

        # 2. Проверка на минуту (1200 записей)
        if len(self.minute_buffer) == 1200:
            packet = list(self.minute_buffer)
            self.all_minute_packets.append(packet)
            print(f"--- ПАКЕТ ЗА МИНУТУ ГОТОВ: {len(packet)} записей ---")
            self.minute_buffer = []

    def get_optimal_patch_size_px(self, map_px_size_m):
        """
        Рассчитывает размер стороны квадрата (в пикселях) с учетом скорости
        и минимально необходимого размера области для корреляции.
        """
        # Минимальная область, чтобы алгоритм "видел" рельеф (в метрах)
        min_patch_meters = 100.0

        # Расчет необходимого размера для "взгляда вперед" на 1 секунду
        look_ahead_meters = self.speed_mps * 1

        # Берем максимум из "взгляда вперед" и "минимального рабочего обзора"
        final_meters = max(look_ahead_meters, min_patch_meters)

        # Переводим в пиксели
        size_px = math.ceil(final_meters / map_px_size_m)

        # Гарантируем нечетность для корректного определения центра
        if size_px % 2 == 0:
            size_px += 1

        # Вывод данных для отладки
        print(f"--- [DEBUG: Оптимизация размера патча] ---")
        print(f"Итоговая область поиска: {final_meters:.2f} м")
        print(f"Размер стороны квадрата (px): {size_px}")
        print(f"Физический размер патча: {size_px * map_px_size_m:.2f} м")

        return size_px

    def calculate_mse(self, profile, patch_slice):  # Добавили self
        profile = np.array(profile)
        patch_slice = np.array(patch_slice)
        mse = np.mean((profile - patch_slice) ** 2)
        return mse

    def find_best_match(self, patch, buffer):  # Добавили self
        min_error = float('inf')
        best_pos = (0, 0)
        buf_len = len(buffer)
        patch_size = patch.shape[0]

        for row in range(patch_size):
            for col in range(patch_size - buf_len + 1):
                patch_slice = patch[row, col: col + buf_len]

                # ВАЖНО: вызываем через self.calculate_mse
                error = self.calculate_mse(buffer, patch_slice)

                if error < min_error:
                    min_error = error
                    best_pos = (row, col)

        return best_pos, min_error