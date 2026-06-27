import math

class Navigator:
    def __init__(self, start_lat, start_lon, speed_mps):
        # Сохраняем координаты
        self.lat = start_lat
        self.lon = start_lon

        self.speed_mps = speed_mps  # Скорость дрона (м/с) для рассчета размера квадрата в м

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