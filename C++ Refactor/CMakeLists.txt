cmake_minimum_required(VERSION 3.16)
project(HCMUS_MMT LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenCV REQUIRED)

add_executable(hcmus_mmt
        src/main.cpp
        src/keyLogger.cpp
        src/webcamRecorder.cpp
        src/scheduler.cpp)

target_include_directories(hcmus_mmt PRIVATE include)
target_link_libraries(hcmus_mmt PRIVATE ${OpenCV_LIBS})
# add pthread on Linux
if (UNIX AND NOT APPLE)
    target_link_libraries(hcmus_mmt PRIVATE pthread)
endif()
