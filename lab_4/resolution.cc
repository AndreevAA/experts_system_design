#include "resolution.h"

#include <cstddef>
#include <iostream>
#include <string_view>
#include <utility>
#include <vector>

#include "atom.h"
#include "clause.h"
#include "io_join.h"  // Подключение заголовочного файла для функций объединения в потоке вывода
#include "resolvent.h"

namespace {

/// Функция добавляет элементы вектора `what` в конец вектора `to`
    template <typename T>
    void Append(std::vector<T>& to, const std::vector<T>& what) {
        to.insert(to.end(), what.begin(), what.end());
    }

/// Функция конкатенации двух векторов
    template <typename T>
    std::vector<T> Concatenate(const std::vector<T>& first,
                               const std::vector<T>& second) {
        std::vector<T> result;
        result.reserve(first.size() + second.size());  // Предварительное выделение памяти для результирующего вектора

        Append(result, first);
        Append(result, second);

        return result;
    }

    void PrintInput(const std::vector<Clause>& axioms,
                    const Clause& inverted_target) {
        std::cout << "Входные данные:\n";
        std::cout << "\tАксиомы:\n";
        for (size_t i = 0; i < axioms.size(); ++i) {
            std::cout << "\t\t" << i + 1 << ". " << axioms[i] << '\n';  // Печать списка аксиом
        }
        std::cout << "\tЦель: " << Negate(inverted_target.front()) << '\n';  // Печать инверсной цели
    }

}  // namespace

std::string_view ToString(ResolutionResult result) {
    switch (result) {
        case ResolutionResult::kProvenByFoundingEmptyClause:
            return "ИСТИНА\nДоказано, найдена контрарная пара";
        case ResolutionResult::kMaxIterationsExceeded:
            return "ЛОЖЬ\nВыход по числу итераций";
        case ResolutionResult::kNoProofFound:
            return "ЛОЖЬ\nНе найдено доказательство";
        case ResolutionResult::kNoNewClausesAdded:
            return "ЛОЖЬ\nНовых дизъюнктов не добавилось";
    }
}

// Основная функция разрешения, использующая полный перебор
ResolutionResult FullResolution(const std::vector<Clause>& axioms,
                                const Clause& inverted_target,
                                size_t max_iterations) {
    std::cout << "[Полный перебор] ";
    PrintInput(axioms, inverted_target);

    auto clause_stack = Concatenate(axioms, {inverted_target});  // Инициализация стека дизъюнктов

    for (size_t iteration = 0, i = 0; i < clause_stack.size() - 1;
         ++i) {  // Перебор всех дизъюнктов

        std::cout << "[Итерация " << iteration << "] Множество дизъюнктов: {";
        join(clause_stack, std::cout);
        std::cout << "}\n";

        for (size_t j = 0; j < clause_stack.size(); ++j) {  // Перебор пар дизъюнктов
            if (i == j) {
                continue;  // Пропускаем пары с одинаковыми индексами
            }

            ++iteration;
            if (iteration > max_iterations) {
                return ResolutionResult::kMaxIterationsExceeded;  // Проверка на превышение максимального числа итераций
            }

            const auto& clause1 = clause_stack[i];
            const auto& clause2 = clause_stack[j];

            // Попытка создать резольвенту
            auto [resolvent, res] = CreateResolvent(clause1, clause2);

            if (res == ResolventResult::kEmptyClause) {  // Если получен пустой дизъюнкт,
                std::cout << "Найдена резольвента дизъюнктов " << clause1 << " и "
                          << clause2 << ": {}\n";  // Вывод сообщения о найденной резольвенте
                return ResolutionResult::kProvenByFoundingEmptyClause;  // Возвращаем результат в случае успеха
            }

            if (res == ResolventResult::kOk) {  // Если резольвента ненулевая,
                std::cout << "Найдена резольвента дизъюнктов " << clause1 << " и "
                          << clause2 << ": " << resolvent;
                auto ignore = false;
                for (const auto& clause : clause_stack) {
                    if (clause == resolvent) {
                        std::cout << " [игнор]";  // Если резольвента уже существует, игнорируем её
                        ignore = true;
                        break;
                    }
                }
                if (!ignore) {
                    clause_stack.push_back(resolvent);  // Добавляем новую резольвенту в стек
                }
                std::cout << '\n';
            }
        }
    }

    return ResolutionResult::kNoProofFound;  // Возврат результата, если доказательство не найдено
}
