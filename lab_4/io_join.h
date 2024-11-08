#pragma once

#include <experimental/iterator>
#include <ostream>

// Общая шаблонная функция для объединения элементов диапазона [begin, end) с использованием заданного разделителя
template <typename It>
void join(It begin, It end, std::ostream& os, const char* delimiter = ", ") {
    // std::copy копирует элементы из входного диапазона в выходной поток
    // std::experimental::make_ostream_joiner позволяет вставлять элементы в поток вывода os с указанным разделителем
    std::copy(begin, end, std::experimental::make_ostream_joiner(os, delimiter));
}

// Перегрузка функции join для контейнеров, принимает контейнер с элементами для объединения
template <typename Container>
void join(const Container& container,
          std::ostream& os,
          const char* delimiter = ", ") {
    // Вызов первой версии функции join с итераторами контейнера.
    // std::begin(container) и std::end(container) используются для получения итераторов начала и конца контейнера.
    join(std::begin(container), std::end(container), os, delimiter);
}