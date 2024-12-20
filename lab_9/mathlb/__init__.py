from scipy.integrate import IntegrationWarning
import matplotlib.pyplot as plt
from scipy.integrate import quad


class InterpolationFunction:
    def __init__(self, sorted_coordinates: list[tuple[float, float]]):
        """
        Инициализация функции интерполяции с отсортированными координатами.

        :param sorted_coordinates: Список координат, представляющих точки для интерполяции.
        """
        self.sorted_coordinates = sorted_coordinates

    def __call__(self, x: float) -> float:
        """
        Позволяет вызывать объект класса как функцию.

        :param x: Значение, для которого нужно рассчитать интерполированное значение.
        :return: Интерполированное значение для заданного x.
        """
        # Проверка, находится ли x ниже минимального значения координат
        if x <= self.sorted_coordinates[0][0]:
            return self.handle_below_min(self.sorted_coordinates[0])
        # Проверка, находится ли x выше максимального значения координат
        elif x >= self.sorted_coordinates[-1][0]:
            return self.handle_above_max(self.sorted_coordinates[-1])

        # Интерполяция между двумя точками
        return self.interpolate_between_points(x, self.sorted_coordinates)

    def handle_below_min(self, point: tuple[float, float]) -> float:
        """
        Обрабатывает ситуацию, когда x меньше минимального значения.

        :param point: Точка, где x меньше минимума.
        :return: Значение соответствующее y минимального значения.
        """
        return point[1]

    def handle_above_max(self, point: tuple[float, float]) -> float:
        """
        Обрабатывает ситуацию, когда x больше максимального значения.

        :param point: Точка, где x больше максимума.
        :return: Значение соответствующее y максимального значения.
        """
        return point[1]

    def interpolate_between_points(self, x: float, sorted_coordinates: list[tuple[float, float]]) -> float:
        """
        Выполняет линейную интерполяцию между двумя точками.

        :param x: Значение, для которого нужно вычислить значения.
        :param sorted_coordinates: Список отсортированных координат.
        :return: Интерполированное значение для заданного x.
        """
        for i in range(len(sorted_coordinates) - 1):
            # Проверка, находится ли x между двумя соседними точками
            if sorted_coordinates[i][0] <= x < sorted_coordinates[i + 1][0]:
                # Вычисление углового коэффициента (наклона)
                slope = (sorted_coordinates[i + 1][1] - sorted_coordinates[i][1]) / (
                        sorted_coordinates[i + 1][0] - sorted_coordinates[i][0])
                # Возврат интерполированного значения
                return sorted_coordinates[i][1] + slope * (x - sorted_coordinates[i][0])

        return None  # Если x не попадает в диапазон, возвращаем None


class Math:
    def __get_sort_coordinates_by_first_elem(self, coordinates: tuple[float, float]):
        """
        Сортирует данные по первому элементу каждой координаты.

        :param coordinates: Набор координат для сортировки.
        :return: Отсортированный список координат.
        """
        return sorted(coordinates, key=lambda point: point[0])

    def __create_interpolation_function(self, sorted_coordinates: list[tuple[float, float]]):
        """
        Создает объект InterpolationFunction на основе отсортированного списка координат.

        :param sorted_coordinates: Отсортированный список координат.
        :return: Объект InterpolationFunction.
        """
        return InterpolationFunction(sorted_coordinates)

    def interpolate_points(self, *coordinates: tuple[float, float]):
        """
        Создает функцию интерполяции для набора координат.

        :param coordinates: Координаты для интерполяции.
        :return: Функция интерполяции.
        """
        return self.__create_interpolation_function(
            self.__get_sort_coordinates_by_first_elem(coordinates)
        )

    def create_trapezoid(self, t1, t2, t3, t4):
        """
        Создает функцию интерполяции, представляющую трапецию.

        :param t1: Координата первого угла.
        :param t2: Координата второго угла.
        :param t3: Координата третьего угла.
        :param t4: Координата четвертого угла.
        :return: Функция интерполяции трапеции.
        """
        return self.interpolate_points((t1, 0), (t2, 1), (t3, 1), (t4, 0))

    def create_triangle(self, t1, t2, t3):
        """
        Создает функцию интерполяции, представляющую треугольник.

        :param t1: Координата первой вершины.
        :param t2: Координата второй вершины.
        :param t3: Координата третьей вершины.
        :return: Функция интерполяции треугольника.
        """
        return self.create_trapezoid(t1, t2, t2, t3)

    def minimum_function(self, functions):
        """
        Создает минимальную функцию для списка функций.

        :param functions: Список функций, от которых нужно взять минимум.
        :return: Функция, возвращающая минимум из входящих функций.
        """
        def combine(x: float):
            return min(func(x) for func in functions)

        return combine

    def maximum_function(self, functions):
        """
        Создает максимальную функцию для списка функций.

        :param functions: Список функций, от которых нужно взять максимум.
        :return: Функция, возвращающая максимум из входящих функций.
        """
        def combine(x: float):
            return max(func(x) for func in functions)

        return combine

    def get_centroid(self, func, a, b):
        """
        Вычисляет центроид (центр масс) фигуры, заданной функцией func на интервале [a, b].

        :param func: Функция, представляющая форму фигуры.
        :param a: Начало интервала.
        :param b: Конец интервала.
        :return: Координата x центроида.
        """
        num, _ = quad(lambda x: x * func(x), a, b)  # Вычисление числителя интеграла
        denom, _ = quad(func, a, b)  # Вычисление знаменателя интеграла

        if denom == 0:
            raise ZeroDivisionError("Функция f(x) равна нулю на всем интервале")

        return num / denom  # Возвращаем координату x центроида