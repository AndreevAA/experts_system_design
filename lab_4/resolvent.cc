#include "resolvent.h"

#include <string>
#include <unordered_map>
#include <utility>

#include "clause.h"

namespace {

// Создает быстрый поиск для данной клаузулы, сопоставляя имена атамов и их знаки.
    std::unordered_map<std::string, bool> MakeClauseFastLookup(
            const AbsorbedClause& clause) {
        std::unordered_map<std::string, bool> clause_fast_lookup;
        for (auto&& atom : clause) {
            clause_fast_lookup.emplace(atom.name, atom.sign);
        }
        return clause_fast_lookup;
    }

/// Вспомогательная функция для CreateResolvent.
/// Ищет имя атома из первого дизъюнкта, для которого существует атом,
/// противоположный по знаку во втором дизъюнкте.
    std::string FindOppositeAtomsName(const AbsorbedClause& first_clause,
                                      const AbsorbedClause& second_clause) {
        const auto second_clause_fast_lookup = MakeClauseFastLookup(second_clause);
        for (auto&& atom : first_clause) {
            if (auto it = second_clause_fast_lookup.find(atom.name);
                    it != second_clause_fast_lookup.end()) {
                const auto& [name, sign] = *it;
                if (atom.sign != sign) {
                    return name;
                }
            }
        }
        return {};
    }

}  // namespace

// Создает резольвент двух дизъюнктов и возвращает его результатом.
std::pair<Clause, ResolventResult> CreateResolvent(const Clause& first,
                                                   const Clause& second) {
    auto first_absorbed_clause =
            first.Absorb();  // Приводим первый дизъюнкт к виду, где атомы не повторяются.
    auto second_absorbed_clause =
            second.Absorb();  // То же самое для второго дизъюнкта.

    // Проверяем, если один из дизъюнктов пустой.
    if (first_absorbed_clause.empty() || second_absorbed_clause.empty()) {
        return {{}, ResolventResult::kEmptyClause};
    }

    // Ищем противоположные атомы
    auto mb_opposite_atoms_name =
            FindOppositeAtomsName(first_absorbed_clause, second_absorbed_clause);
    if (mb_opposite_atoms_name.empty()) {
        // Противоположные пары не найдены
        return {{}, ResolventResult::kOppositePairNotFound};
    }

    // Если найдена противоположная пара атомов
    // Заполняем резольвент, исключая противоположные атомы
    Clause resolvent;

    const auto append_resolvent_without_opposite_atom =
            [&mb_opposite_atoms_name, &resolvent](AbsorbedClause& absorbed_clause) {
                for (auto&& atom : absorbed_clause) {
                    if (atom.name != mb_opposite_atoms_name) {
                        resolvent.push_back(std::move(atom));
                    }
                }
            };

    append_resolvent_without_opposite_atom(first_absorbed_clause);
    append_resolvent_without_opposite_atom(second_absorbed_clause);

    auto absorbed_resolvent = resolvent.Absorb();  // Поглощаем резольвент.
    const auto result = absorbed_resolvent.empty() ? ResolventResult::kEmptyClause : ResolventResult::kOk;

    return {Clause{std::move(absorbed_resolvent)}, result}; // Возвращаем окончательный резольвент и результат.
}