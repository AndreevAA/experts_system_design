#include "clause.h"

#include <unordered_map>  // Для хранения информации о уже обработанных атомах
#include <utility>
#include <ostream>
#include <string>
#include <vector>

#include "atom.h"
#include "io_join.h"

// Конструктор, который инициирует Clause из AbsorbedClause, перемещая его данные
Clause::Clause(AbsorbedClause&& absorbed_clause) noexcept
        : std::vector<Atom>(std::move(absorbed_clause)) {}

// Метод, который возвращает дизъюнкт без дублирующихся атомов.
// Если обнаружены противоречащие атомы (одинаковое имя, разные знаки), возвращается пустой.
AbsorbedClause Clause::Absorb() const {
    AbsorbedClause absorbed;  // Дизъюнкт без дублей
    std::unordered_map<std::string, bool> processed_atoms;  // Отслеживание обработанных атомов

    for (auto&& atom : *this) {
        // Проверка на существование атома в processed_atoms
        if (auto it = processed_atoms.find(atom.name);
                it != processed_atoms.end()) {
            const auto& [name, sign] = *it;
            // Если знаки отличаются, значит имеется противоречие, возвращаем пустой дизъюнкт
            if (atom.sign != sign) {
                return {};
            }
            // Если знаки совпадают, пропускаем добавление, так как атом уже учтен
            continue;
        }
        // Атом добавляется в дизъюнкт, если его ещё не было
        absorbed.push_back(atom);
        processed_atoms.emplace(atom.name, atom.sign);
    }

    return absorbed;
}

// Переопределенный оператор вывода для Clause
std::ostream& operator<<(std::ostream& os, const Clause& clause) {
    os << "{";
    join(clause, os);  // Функция join используется для форматирования вывода
    return os << "}";
}

// Переопределенный оператор вывода для AbsorbedClause
std::ostream& operator<<(std::ostream& os, const AbsorbedClause& clause) {
    // Приведение AbsorbedClause к базовому типу Clause для использования переопределенного оператора вывода
    return os << reinterpret_cast<const Clause&>(clause);
}