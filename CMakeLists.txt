cmake_minimum_required(VERSION 3.25)
project(ESD
        HOMEPAGE_URL https://github.com/AndreevAA/experts_system_design
        LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(cmake/CompileOptions.cmake)

set(CMAKE_CXX_CLANG_TIDY clang-tidy)


add_subdirectory(lab_5)
