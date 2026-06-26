class Navigator:
    def __init__(self):
        self.all_packets = []  # Хранит все пакеты
        self.current_buffer = []  # Накопитель на текущие 5 секунд

    def add_measurement(self, height):
        self.current_buffer.append(height)

        # Если накопилось 5 измерений, сохраняем пакет и очищаем буфер
        if len(self.current_buffer) >= 5:
            self.all_packets.append(list(self.current_buffer))
            print(f"Пакет зафиксирован: {self.current_buffer}")
            self.current_buffer = []  # Очистка для следующей пятисекундки