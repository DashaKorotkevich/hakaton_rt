import rasterio
import math

class TerrainMap:
    def __init__(self, path_to_map):
        self.src = rasterio.open(path_to_map)
        # Получаем размеры для проверок границ
        self.width = self.src.width
        self.height = self.src.height
        # Матрица трансформации для перевода пикселей в координаты
        self.transform = self.src.transform

    def get_height(self, x, y):
        # Превращаем координаты в целые числа для индексации
        px, py = int(x), int(y)

        # Проверка, что мы не вылетели за края карты
        if 0 <= px < self.width and 0 <= py < self.height:
            # Читаем ровно один пиксель
            window = rasterio.windows.Window(px, py, 1, 1)
            data = self.src.read(1, window=rasterio.windows.Window(px, py, 1, 1))

            # Проверяем, является ли значение значением "нет данных"
            if data[0, 0] == self.src.nodata:
                return None  # Возвращаем None, если данных нет

            return float(data[0, 0])
        return None  # Если мы вне карты, возвращаем 0

    def inspect_file(self):
        print(f"Количество каналов (bands): {self.src.count}")
        print(f"Тип данных: {self.src.dtypes[0]}")
        print(f"Метаданные (теги): {self.src.tags()}")
        print(f"Проекция: {self.src.crs}")

        #Метод для получения GPS-координат из пикселей
    def get_latlon(self, x, y):
        # x, y в rasterio это столбец и строка (col, row)
        lon, lat = self.transform * (x, y)
        return lat, lon

    def get_terrain_profile(terrain_map, start_lat, start_lon, azimuth, distance_meters, step=200):
        """
        Генерирует список высот вдоль заданного азимута
        """
        profile = []
        # Конвертируем метры в градусы (грубо для широты Краснодара)
        lat_step = (step / 111132) * math.cos(math.radians(azimuth))
        lon_step = (step / 111320) * math.sin(math.radians(azimuth))

        current_lat, current_lon = start_lat, start_lon

        for i in range(0, int(distance_meters), step):
            # Перевод GPS в координаты пикселей (обратно к transform)
            # В rasterio: col, row = ~transform * (lon, lat)
            px, py = ~terrain_map.transform * (current_lon, current_lat)
            h = terrain_map.get_height(px, py)
            profile.append((current_lat, current_lon, h))

            current_lat += lat_step
            current_lon += lon_step

        return profile

    def close(self):
        self.src.close()