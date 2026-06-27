import rasterio
import rasterio.windows
import math


class TerrainMap:
    def __init__(self, path_to_map):
        self.src = rasterio.open(path_to_map)
        self.width = self.src.width
        self.height = self.src.height
        self.transform = self.src.transform

        # 1. Вычисляем физический размер пикселя в метрах (динамически)
        # Получаем разрешение в градусах из метаданных
        deg_res_x = self.transform.a
        deg_res_y = abs(self.transform.e)

        # Определяем среднюю широту области для корректного перевода долготы
        center_lat = (self.src.bounds.top + self.src.bounds.bottom) / 2

        # Константы (метров в 1 градусе)
        m_per_deg_lat = 111132
        m_per_deg_lon = 111320 * math.cos(math.radians(center_lat))

        # Реальные размеры пикселя в метрах
        self.px_w_m = deg_res_x * m_per_deg_lon
        self.px_h_m = deg_res_y * m_per_deg_lat


        # Общие размеры карты в метрах
        self.width_meters = self.width * self.px_w_m
        self.height_meters = self.height * self.px_h_m

    def get_height(self, x, y):
        """Возвращает высоту по пиксельным координатам x (col), y (row)"""
        px, py = int(x), int(y)
        if 0 <= px < self.width and 0 <= py < self.height:
            window = rasterio.windows.Window(px, py, 1, 1)
            data = self.src.read(1, window=window)
            if data[0, 0] == self.src.nodata:
                return None
            return float(data[0, 0])
        return None

    def get_latlon(self, x, y):
        """Перевод пикселей в GPS"""
        lon, lat = self.transform * (x, y)
        return lat, lon

    def get_patch_by_latlon(self, center_lat, center_lon, patch_size_px):
        """
        Возвращает квадратную матрицу высот вокруг заданной точки.
        patch_size_px: сторона квадрата в пикселях.
        """
        # 1. Переводим GPS в пиксели (row, col)
        # ~self.src.transform инвертирует матрицу трансформации
        col, row = ~self.src.transform * (center_lon, center_lat)
        col, row = int(col), int(row)

        # 2. Вычисляем верхний левый угол окна
        half = patch_size_px // 2
        window_col = col - half
        window_row = row - half

        # 3. Создаем окно для чтения (обработка границ - необязательно,
        # но rasterio автоматически обрежет, если выйти за края)
        window = rasterio.windows.Window(window_col, window_row, patch_size_px, patch_size_px)

        # 4. Читаем данные
        data = self.src.read(1, window=window)

        # Если нужно заменить NoData на что-то другое (например, NaN), можно сделать здесь:
        if self.src.nodata is not None:
            data[data == self.src.nodata] = float('nan')

        return data

    def inspect_file(self):
        print(f"Размер в пикселях: {self.width}x{self.height}")
        print(f"Размер в метрах: {self.width_meters:.0f}x{self.height_meters:.0f} м")
        print(f"Размер пикселя: {self.px_w_m:.2f}x{self.px_h_m:.2f} м")
        print(f"Проекция: {self.src.crs}")

    def close(self):
        self.src.close()