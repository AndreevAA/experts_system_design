#include <exception>
#include <iostream>
#include <vector>

// Подключаем заголовочные файлы, которые, видимо, содержат определения классов Atom, Clause и функций резолюции.
#include "atom.h"
#include "clause.h"
#include "resolution.h"

// Главная функция программы
int main() {
    try {
        // Создаем несколько атомов с их именами и значениями истинности
        const Atom a = {"A", true};
        const Atom b = {"B", true};
        const Atom c = {"C", true};
        const Atom d = {"D", true};
        const Atom not_a = {"A", false};
        const Atom not_b = {"B", false};
        const Atom not_c = {"C", false};
        const Atom not_d = {"D", false};

        // Создаем несколько дизъюнктов из атомов
        const Clause ax1 = {a, b};
        const Clause ax2 = {not_a, c};
        const Clause ax3 = {not_b, d};
        const Clause ax4 = {not_c};
        const Clause ax5 = {not_d};
        const Clause ax6 = {not_a};

        // Собираем все аксиомы в вектор
        const std::vector<Clause> axioms = {ax1, ax2, ax3, ax4, ax5};

        // Проводим полную резолюцию на базе аксиом (axioms) с противоречием ax6
        // Указываем лимит итераций равный 1000
        const auto res = FullResolution(axioms, ax6, 1000);

        // Выводим результат резолюции на экран
        std::cout << '\n' << ToString(res);
    } catch (const std::exception& exception) {
        // Обработка возможных исключений: выводим сообщение об ошибке и возвращаем код ошибки 1
        std::cerr << "[exception] " << exception.what() << '\n';
        return 1;
    }
}