import numpy as np
import matplotlib.pyplot as plt

class FuzzyVariable:
    def __init__(self, label: str, sets: list = None, value=None):
        """
        Инициализация нечеткой переменной с заданным ярлыком, множеством нечетких множеств и значением.

        :param label: Ярлык нечеткой переменной.
        :param sets: Список нечетких множеств, связанных с данной переменной.
        :param value: Значение, связанное с нечеткой переменной.
        """
        self.label = label  # Установить ярлык для переменной
        self.sets = sets or []  # Список нечетких множеств
        self.value = value  # Значение переменной

    def find_set_by_label(self, label: str):
        """
        Поиск нечеткого множества по его ярлыку.

        :param label: Ярлык нечеткого множества, которое требуется найти.
        :return: Ярлык переменной и найденное нечеткое множество, если оно существует; иначе None.
        """
        for fuzzy_set in self.sets:
            if fuzzy_set.label == label:
                return self.label, fuzzy_set  # Возвращаем ярлык переменной и найденное множество
        return None  # Если не найдено, возвращаем None

    def assign_value(self, value):
        """
        Присвоение значения нечеткой переменной.

        :param value: Значение, которое присваивается переменной.
        :return: Новый экземпляр FuzzyVariable с теми же ярлыком и множествами, но с новым значением.
        """
        return FuzzyVariable(self.label, self.sets, value)  # Создаем и возвращаем новый экземпляр переменной

    def visualize(self, x_min: float, x_max: float, axes=plt):
        """
        Визуализирует нечеткие множества на графике.

        :param x_min: Минимальное значение по оси x для графика.
        :param x_max: Максимальное значение по оси x для графика.
        :param axes: Объект Axes для построения графика (по умолчанию - plt).
        """
        # Создаем значения x для построения графика
        x_values = np.linspace(x_min, x_max, 1000)

        # Проходим по всем нечетким множествам и добавляем их на график
        for fuzzy_set in self.sets:
            # Вычисляем значения членства для текущего нечеткого множества
            membership_values = self.calculate_membership_values(fuzzy_set, x_values)

            # Строим линию и затеняем область под графиком
            self.plot_membership_curve(fuzzy_set.label, x_values, membership_values, axes)

        # Настройка заголовка, легенды и сетки графика
        self.setup_plot(axes)

    def calculate_membership_values(self, fuzzy_set, x_values):
        """
        Вычисляет значения членства для заданного нечеткого множества.

        :param fuzzy_set: Текущее нечеткое множество, для которого вычисляются значения членства.
        :param x_values: Значения по оси x, для которых необходимо вычислить членство.
        :return: Список значений членства для заданных x.
        """
        return [fuzzy_set.calculate_membership(y) for y in x_values]

    def plot_membership_curve(self, label: str, x_values: np.ndarray, membership_values: list, axes):
        """
        Строит кривую членства и заполняет область под ней.

        :param label: Ярлык нечеткого множества для легенды.
        :param x_values: Значения по оси x.
        :param membership_values: Значения членства для соответствующих x.
        :param axes: Объект Axes для построения графика.
        """
        axes.plot(x_values, membership_values, label=label)  # Линия графика
        axes.fill_between(x_values, membership_values, alpha=0.3)  # Заполнение области под графиком

    def setup_plot(self, axes):
        """
        Настраивает заголовок, легенду и сетку для графика.

        :param axes: Объект Axes для настройки графика.
        """
        axes.set_title(f"Лингвистическая переменная \\n {self.label}")  # Установка заголовка
        axes.legend()  # Установка легенды
        axes.grid()  # Включение сетки