#include "atom.h"  // Подключаем заголовочный файл, содержащий объявление структуры Atom

#include <ostream>  // Подключаем заголовочный файл для работы с потоками вывода

// Функция Negate принимает Atom и возвращает новый Atom с обратным атомным знаком
Atom Negate(const Atom& atom) {
    return {atom.name, !atom.sign};  // Создаем новый Atom с тем же именем, но переворачиваем знак
}

// Переопределяем оператор равенства для структур Atom
bool operator==(const Atom& lhs, const Atom& rhs) {
    // Сравниваем название и знак двух атомов, возвращая true, если оба совпадают
    return lhs.name == rhs.name && lhs.sign == rhs.sign;
}

// Переопределяем оператор вывода в поток для структур Atom
std::ostream& operator<<(std::ostream& os, const Atom& atom) {
    if (!atom.sign) {  // Если атом находится в отрицательной форме
        os << "¬";  // Выводим символ отрицания
    }
    return os << atom.name;  // Выводим имя атома
}