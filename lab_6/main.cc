#include <algorithm>
#include <cassert>
#include <cstddef>
#include <cstdint>
#include <exception>
#include <iostream>
#include <map>
#include <string>
#include <tuple>
#include <unordered_set>
#include <utility>
#include <vector>

// Загрузка пользовательских типов Atom, Clause, Formula и Terminal
#include "types/atom.h"
#include "types/clause.h"
#include "types/formula.h"
#include "types/terminal.h"

// Класс ResolutionSolver решает задачу доказательства путем разрешения
class ResolutionSolver {
private:
    // Внутреннее хранилище для всех дизъюнктов, участвующих в процессе
    std::vector<Clause> clauses_;
    // Хранит уникальные идентификаторы уже рассмотренных пар атрибутов
    std::unordered_set<size_t> seen_;

    // Проверяет, была ли уже рассмотрена комбинация атомов указанных индексов
    bool IsSeen(const size_t x, const size_t i, const size_t y, const size_t j) {
        // Генерирует уникальный индекс для пары (x, i) и (y, j)
        const auto xx = static_cast<uint64_t>(x);
        const auto yy = static_cast<uint64_t>(y);
        const auto ii = static_cast<uint64_t>(i);
        const auto jj = static_cast<uint64_t>(j);
        const auto idx = (xx << 48ULL) + (ii << 32ULL) + (yy << 16ULL) + jj;
        // Проверка наличия индекса в наборе seen_
        if (seen_.contains(idx)) {
            return true;
        }
        // Добавление индекса в набор для других проверок
        seen_.emplace(idx);
        return false;
    }

    // Замена всех вхождений переменной (или константы) old_name на new_name
    void SubstituteTerminals(const std::string& old_name,
                             const std::string& new_name,
                             const bool do_make_const) {
        std::cout << "  Замена: " << old_name << " -> " << new_name
                  << (do_make_const ? " const" : "") << '\n';
        // Переход по каждому дизъюнкту
        for (auto& clause : clauses_) {
            // Переход по каждому атому в дизъюнкте
            for (auto& atom : clause.atoms()) {
                // Переход по каждому термину в атоме
                for (auto& terminal : atom.terminals()) {
                    // Пропустить, если имя не совпадает
                    if (terminal.name() != old_name) {
                        continue;
                    }

                    assert(!terminal.IsConstant());
                    // Установка нового имени для термина
                    terminal.set_name(new_name);
                    // Установить как константу, если do_make_const = true
                    if (do_make_const) {
                        terminal.MakeConstant();
                    }
                }
            }
        }
    }

    // Создает новый дизъюнкт, комбинируя атомы из a1 и a2, исключая i и j
    static Clause GetNewClause(const std::vector<Atom>& a1, size_t i,
                               const std::vector<Atom>& a2, size_t j) {
        assert(!a1.empty());
        assert(a1.size() > i);
        assert(!a2.empty());
        assert(a2.size() > j);

        Clause new_clause;
        auto& new_atoms = new_clause.atoms();
        // Резервируем необходимое место для атомов
        new_atoms.reserve(a1.size() + a2.size() - 2);

        // Добавляем атомы из первого списка, за исключением i
        for (size_t k = 0; k < a1.size(); ++k) {
            if (k != i) {
                new_atoms.push_back(a1[k]);
            }
        }
        // Добавляем атомы из второго списка, за исключением j
        for (size_t m = 0; m < a2.size(); ++m) {
            if (m != j) {
                new_atoms.push_back(a2[m]);
            }
        }

        return new_clause;
    }

    // Добавляет новый дизъюнкт в список и проверяет, является ли он финалом
    bool AddNewClause(Clause new_clause, bool& is_final_result) {
        if (new_clause.atoms().empty()) {
            is_final_result = true;
        }

        clauses_.push_back(std::move(new_clause));
        return true;
    }

    // Пытается унифицировать два атома; возвращает true, если унификация успешна
    bool UnifyAtoms(const Atom& a1, const Atom& a2) {
        assert(a1.name() == a2.name());
        assert(a1.terminals().size() == a2.terminals().size());
        assert(a1.is_negative() != a2.is_negative());

        // Временное хранение для замены терминалов
        using Mapping = std::vector<std::pair<std::string, std::string>>;
        Mapping consts_mappings;
        Mapping linked_vars;

        // Сравниваем и сопоставляем терминалы между атомами
        for (size_t i = 0; i < a1.terminals().size(); ++i) {
            const auto* t1 = &a1.terminals()[i];
            const auto* t2 = &a2.terminals()[i];

            if (t1->IsConstant() && t2->IsConstant()) {  // Оба терминала константы.
                if (t1->name() != t2->name()) {
                    return false;  // Унификация невозможна, если константы различны.
                }
            } else if (t1->IsVariable() && t2->IsVariable()) {  // Оба терминала переменные.
                if (t1->name() != t2->name()) {
                    linked_vars.emplace_back(t1->name(), t2->name());
                }
            } else {  // Одна переменная, другая константа
                if (t1->IsConstant()) {
                    std::swap(t1, t2);  // Обмен значений, чтобы t1 была всегда переменной
                }
                consts_mappings.emplace_back(t1->name(), t2->name());
            }
        }

        // Реализация унификации для связанных переменных
        static int counter = 1;
        std::map<std::string, int> new_vars;
        for (auto& [var1, var2] : linked_vars) {
            auto it1 = new_vars.find(var1);
            auto it2 = new_vars.find(var2);
            if (it1 != new_vars.end() && it2 != new_vars.end()) {
                const int num1 = it1->second;
                const int num2 = it2->second;
                for (auto& [var, num] : new_vars) {
                    if (num == num2) {
                        num = num1;
                    }
                }
            } else if (it1 != new_vars.end()) {
                new_vars.emplace(std::move(var2), it1->second);
            } else if (it2 != new_vars.end()) {
                new_vars.emplace(std::move(var1), it2->second);
            } else {
                const int new_num = counter++;
                new_vars.emplace(std::move(var1), new_num);
                new_vars.emplace(std::move(var2), new_num);
            }
        }

        // Применение значений из связанного списка переменных к константным маппингам
        for (const auto& [var, num] : new_vars) {
            for (auto& [old_v, new_v] : consts_mappings) {
                if (old_v == var) {
                    old_v = "@" + std::to_string(num);
                }
            }
        }

        // Проверка корректности унификации констант на основе маппинга
        std::map<std::string, std::string> vars_vals;
        for (auto& [old_v, new_v] : consts_mappings) {
            if (auto it = vars_vals.find(old_v); it != vars_vals.end()) {
                if (it->second != new_v) {
                    return false;
                }
            } else {
                vars_vals.emplace(std::move(old_v), std::move(new_v));
            }
        }

        // Применение замен связанных переменных
        for (auto const& [var, num] : new_vars) {
            const std::string new_name = "@" + std::to_string(num);
            SubstituteTerminals(var, new_name, false);
        }
        // Применение замен констант
        for (auto const& [old_v, new_v] : vars_vals) {
            SubstituteTerminals(old_v, new_v, true);
        }
        return true;
    }

    // Проверяет пару дизъюнктов на возможность унификации и производит её в случае успеха
    bool CheckClauses(const size_t x, const size_t y, bool& is_final_result) {
        const auto& a1 = clauses_[x].atoms();
        const auto& a2 = clauses_[y].atoms();

        for (size_t i = 0; i < a1.size(); ++i) {
            for (size_t j = 0; j < a2.size(); ++j) {
                if (IsSeen(x, i, y, j)) {
                    continue;
                }

                const auto& atom1 = a1[i];
                const auto& atom2 = a2[j];

                // Проверяем, имеют ли два атома одинаковое имя, но противоположную полярность
                if (atom1.name() != atom2.name() ||
                    atom1.is_negative() == atom2.is_negative()) {
                    continue;
                }

                std::cout << "Унификация: " << atom1 << " [" << x + 1 << "] И " << atom2
                          << " [" << y + 1 << "]\n";
                if (!UnifyAtoms(atom1, atom2)) {
                    std::cout << "  Невозможна" << '\n';
                    continue;
                }

                // Создаем новый дизъюнкт путем объединения оставшихся атомов (без i и j)
                auto new_clause = GetNewClause(a1, i, a2, j);
                std::cout << "Новый дизъюнкт:\n  " << new_clause << " =====>\n";

                //[Этапы упрощения нового дизъюнкта]

                // Устраняем дубликаты термов
                new_clause.Distinct();

                // Убираем противоположные термы
                new_clause.RemoveOpposites();

                // Сортируем термы для упорядоченности
                new_clause.Sort();

                std::cout << "  " << new_clause << '\n';

                // Проверяем, есть ли уже такой дизъюнкт в списке
                const auto is_present = std::any_of(clauses_.begin(), clauses_.end(), [&new_clause](const Clause& clause) {
                    return clause == new_clause;
                });
                if (is_present) {
                    std::cout << "Дизъюнкт уже имеется в списке\n";
                    continue;
                }

                std::cout << "Добавили дизъюнкт\n";
                AddNewClause(std::move(new_clause), is_final_result);
                return true;
            }
        }
        return false;
    }

    // Метод для вывода текущих дизъюнктов в консоль
    void PrintClauses() const {
        std::cout << "Дизъюнкты:\n";
        const auto len = std::to_string(clauses_.size() + 1).length() + 1;
        for (size_t i = 0; i < clauses_.size(); ++i) {
            const auto j = std::to_string(i + 1);
            const auto sp = std::string(len - j.size(), ' ');
            std::cout << "  " << j << '.' << sp << clauses_[i] << "\n";
        }
        std::cout << "=======================================" << '\n';
    }

public:
    // Конструктор принимает первоначальное множество формул и отрицание цели
    ResolutionSolver(const std::vector<Formula>& formulas,
                     const Formula& neg_target) {
        for (const auto& formula : formulas) {
            for (const auto& clause : formula.clauses()) {
                clauses_.push_back(clause);
            }
        }
        for (const auto& clause : neg_target.clauses()) {
            clauses_.push_back(clause);
        }
    }

    // Основной метод разрешения; пытается вывести противоречие
    void Solve() {
        // (пустая дизъюнкция)
        auto is_final_result = false;
        // (новая дизъюнкция добавлена)
        auto is_iter_changed = true;

        // Пока изменения в списке дизъюнктов происходят и результат не достигнут
        while (is_iter_changed && !is_final_result) {
            PrintClauses();

            is_iter_changed = false;

            for (size_t x = 0; x + 1 < clauses_.size(); ++x) {
                for (size_t y = x + 1; y < clauses_.size(); ++y) {
                    // Проверка, могут ли данные две дизъюнкции быть объединены
                    // Если новая дизъюнкция получена, то is_iter_changed станет true
                    if (CheckClauses(x, y, is_final_result)) {
                        is_iter_changed = true;
                        // Выход из внутреннего цикла, чтобы начать новую итерацию
                        break;
                    }
                }
                // Выход из внешнего цикла, если что-то изменилось
                if (is_iter_changed) {
                    break;
                }
            }
        }

        // Финальный вывод дизъюнктов
        PrintClauses();

        // Вывод результата: было ли доказательство успешным
        if (is_iter_changed) {
            std::cout << "Доказано" << '\n';
        } else {
            std::cout << "He доказано" << '\n';
        }
    }
};

int main() {
    try {
        constexpr auto kNegative = true;

        // Определяем множества формул и цель для доказательства
        const Formula f2_1{
                Clause{
                        Atom{"P2", {Terminal::Variable("x1"), Terminal::Variable("y1")}},
                        Atom{"P5", {Terminal::Variable("w1")}},
                        Atom{"P6", {Terminal::Variable("z1")}, kNegative},
                },
                Clause{
                        Atom{"P3", {Terminal::Constant("C")}},
                        Atom{"P4", {Terminal::Variable("z1")}, kNegative},
                        Atom{"P1",
                             {Terminal::Variable("x1"), Terminal::Variable("y1"),
                              Terminal::Variable("z1")}},
                },
        };

        // Далее инициализируются еще две формулы
        const Formula f2_2{
                Clause{
                        Atom{"P2",
                             {Terminal::Constant("A"), Terminal::Constant("B")},
                             kNegative},
                        Atom{"P5", {Terminal::Variable("w2")}},
                        Atom{"P6", {Terminal::Variable("z2")}},
                },
                Clause{
                        Atom{"P4", {Terminal::Variable("z2")}},
                        Atom{"P3", {Terminal::Variable("z2")}, kNegative},
                },
        };

        // Теперь определяем отрицание целевой формулы
        const Formula neg_target{
                Clause{
                        Atom{"P1",
                             {Terminal::Constant("A"), Terminal::Constant("B"),
                              Terminal::Constant("C")},
                             kNegative},
                },
        };

        // Инициализируем и начинаем процесс разрешения
        ResolutionSolver({f2_1, f2_2}, neg_target).Solve();
        return 0;
    }
        // Ловим исключения и выводим их
    catch (const std::exception& exception) {
        std::cout << "[exception] " << exception.what() << '\n';
        return 1;
    }
}