class Navigator:
    def __init__(self, start_lat, start_lon):
        # Сохраняем координаты
        self.lat = start_lat
        self.lon = start_lon

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