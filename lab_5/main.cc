#include <iostream>
#include <exception>

#include "types/atom.h"
#include "types/constant.h"
#include "types/variable.h"
#include "unification.h"

/**
 * Основная функция программы, которая демонстрирует пример
 * выполнения унификации двух логических атомов с использованием
 * переменных и констант.
 */
int main() {
  try {
    // Создание экземпляров переменных
    auto v1 = Variable{"v1"};
    auto v2 = Variable{"v2"};
    auto v3 = Variable{"v3"};
    auto v4 = Variable{"v4"};
    auto v5 = Variable{"v5"};
    auto v6 = Variable{"v6"};
    auto v7 = Variable{"v7"};
    auto v8 = Variable{"v8"};
    auto v9 = Variable{"v9"};
    auto v10 = Variable{"v10"};
    auto v11 = Variable{"v11"};

    // Создание экземпляров констант
    auto c1 = Constant{"1"};
    auto c2 = Constant{"2"};

    // Создание первого атома с именем "A" и списком терминалов
    auto a1 = Atom{
      "A", {&v1, &v3, &v4, &v5, &v1, &v1, &v7, &v9, &v7, &v10, &v8, &v11, &v4}};

    // Создание второго атома с именем "A" и списком терминалов
    auto a2 = Atom{
      "A", {&v2, &v1, &c1, &v4, &v6, &v5, &v8, &v10, &v9, &v7, &v1, &c2, &v11}};

    // Выполнение унификации двух атомов
    const auto res = Unify(a1, a2);

    // Вывод результата унификации: "SUCCESS", если унификация успешна,
    // или "FAILURE", если нет. Отсутствие ошибок в ходе унификации трактуется как успех
    std::cout << '\n' << (res ? "SUCCESS" : "FAILURE") << '\n';
  } catch (const std::exception& exception) {
    // Обработка исключений. В случае возникновения ошибки
    // выводится сообщение об ошибке и программа завершает работу с кодом 1.
    std::cerr << "[exception] " << exception.what() << '\n';
    return 1;
  }
}