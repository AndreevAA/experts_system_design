import warnings
from scipy.integrate import IntegrationWarning
import matplotlib.pyplot as plt
from fuzzyset import *
from fuzzyrule import *
from fuzzyvar import *
from mathlb import *

# Игнорируем предупреждения об интеграции
warnings.filterwarnings("ignore", category=IntegrationWarning)

def perform_inference(variables: list[FuzzyVariable], rules=list[FuzzyRule]):
    activated_functions = []
    activated_terms = []
    for rule in rules:
        activation_value = 1
        for variable in variables:
            activation_value = min(rule.evaluate(variable.label, variable.value), activation_value)

        if activation_value > 0:
            activated_functions.append(rule.output_function(activation_value))
            activated_terms.append((rule.output_set.label, rule.output_function(activation_value)))
            print("Activated: ", rule)

    if len(activated_functions) == 0:
        return lambda x: 0, []
    elif len(activated_functions) == 1:
        return activated_functions[0], activated_terms

    return Math().maximum_function(activated_functions), activated_terms

# Определение переменных
humidity_var = FuzzyVariable('Влажность', [
    FuzzySet('Очень низкая', Math().create_trapezoid(0, 20, 25, 30)),
    FuzzySet('Низкая', Math().create_trapezoid(25, 40, 45, 60)),
    FuzzySet('Средняя', Math().create_trapezoid(50, 60, 65, 80)),
    FuzzySet('Высокая', Math().create_trapezoid(70, 85, 90, 100)),
])

temperature_var = FuzzyVariable('Температура', [
    FuzzySet('Холодная', Math().interpolate_points((-10, 1), (5, 0.3), (20, 0))),
    FuzzySet('Комфортная', Math().interpolate_points((15, 0), (20, 1), (25, 0))),
    FuzzySet('Горячая', Math().interpolate_points((25, 0), (30, 1), (45, 1))),
])

# Правила вывода
rules_list = [
    FuzzyRule({humidity_var.label: humidity_var.sets[0]}, temperature_var.label, temperature_var.sets[0]),
    FuzzyRule({humidity_var.label: humidity_var.sets[1]}, temperature_var.label, temperature_var.sets[1]),
    FuzzyRule({humidity_var.label: humidity_var.sets[2]}, temperature_var.label, temperature_var.sets[2]),
    FuzzyRule({humidity_var.label: humidity_var.sets[3]}, temperature_var.label, temperature_var.sets[1]),
]

# Визуализация температурных и влажностных множества
fig, ax = plt.subplots(1, 2, figsize=(16, 4))
humidity_var.visualize(0, 100, ax[0])
ax[0].set_title('Влажность')
temperature_var.visualize(-10, 45, ax[1])
ax[1].set_title('Температура')
plt.show()

# Скорость вентилятора и качество воздуха
fan_speed_var = FuzzyVariable('Скорость вентилятора', [
    FuzzySet('Медленно', Math().interpolate_points((0, 1), (25, 0))),
    FuzzySet('Средне', Math().interpolate_points((20, 0), (30, 1), (40, 0))),
    FuzzySet('Быстро', Math().interpolate_points((30, 0), (50, 1), (60, 1))),
])

air_quality_var = FuzzyVariable('Качество воздуха', [
    FuzzySet('Очень плохое', Math().interpolate_points((0, 1), (20, 0))),
    FuzzySet('Плохое', Math().interpolate_points((20, 0), (40, 1), (60, 0))),
    FuzzySet('Среднее', Math().interpolate_points((40, 0), (60, 1), (80, 0))),
    FuzzySet('Хорошее', Math().interpolate_points((70, 0), (85, 1), (100, 0))),
])

rules_set2 = [
    FuzzyRule({fan_speed_var.find_set_by_label('Медленно'): 1, air_quality_var.find_set_by_label('Плохое'): 1}, fan_speed_var.label, fan_speed_var.find_set_by_label('Быстро')),
    FuzzyRule({fan_speed_var.find_set_by_label('Средне'): 1, air_quality_var.find_set_by_label('Среднее'): 1}, fan_speed_var.label, fan_speed_var.find_set_by_label('Средне')),
    FuzzyRule({fan_speed_var.find_set_by_label('Быстро'): 1, air_quality_var.find_set_by_label('Хорошее'): 1}, fan_speed_var.label, fan_speed_var.find_set_by_label('Медленно')),
]

# Создание графиков для скорости вентилятора и качества воздуха
fig, ax = plt.subplots(1, 2, figsize=(16, 4))
fan_speed_var.visualize(0, 100, ax[0])
ax[0].set_title('Скорость вентилятора')
air_quality_var.visualize(0, 100, ax[1])
ax[1].set_title('Качество воздуха')
plt.show()

# Выполнение вывода по заданным переменным
result, output_funcs = perform_inference(
    [humidity_var.assign_value(65), temperature_var.assign_value(28)],
    rules_list
)

# Вычисление центра масс для температуры
centroid = Math().get_centroid(result, -10, 45)
print("Новое значение температуры:", centroid)

# Вывод для скорости вентилятора
result2, output_funcs2 = perform_inference(
    [fan_speed_var.assign_value(50), air_quality_var.assign_value(30)],
    rules_set2
)

# Вычисление центра масс для скорости вентилятора
centroid2 = Math().get_centroid(result2, 0, 100)
print("Новое значение скорости вентилятора:", centroid2)

# Сохранение графиков
fig.savefig('humidity_temperature.png')
plt.close(fig)

fig.savefig('fan_speed_air_quality.png')
plt.close(fig)