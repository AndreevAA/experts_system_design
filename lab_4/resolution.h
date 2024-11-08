#pragma once

#include <utility>
#include <vector>

#include "clause.h"

/// Перечисление возможных результатов процесса резолюции.
enum class ResolutionResult {
    kProvenByFoundingEmptyClause,  // Доказано нахождением пустой клаузулы.
    kMaxIterationsExceeded,        // Превышено максимальное число итераций.
    kNoProofFound,                 // Доказательство не найдено.
    kNoNewClausesAdded,            // Не добавлены новые клаузулы.
};

/// Преобразует результат резолюции в строковое представление.
std::string_view ToString(ResolutionResult result);

/// Полный перебор для поиска доказательства.
ResolutionResult FullResolution(const std::vector<Clause>& axioms,
                                const Clause& inverted_target,
                                size_t max_iterations);

/// Опорное множество для поиска доказательства.
ResolutionResult BasicResolution(const std::vector<Clause>& axioms,
                                 const Clause& inverted_target, size_t max_iterations);