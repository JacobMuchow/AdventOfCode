cmake_minimum_required(VERSION 3.12)
include(FetchContent)

project(advent2015 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Automatically find sources because I'm lazy
file(GLOB_RECURSE SOURCES
    RELATIVE ${CMAKE_SOURCE_DIR}
    CONFIGURE_DEPENDS
    "*.h"
    "*.cpp"
)

# Set up exe & sources
add_executable(advent2015 main.cpp
    ${SOURCES}
)

# Json parsing repo
FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz)
FetchContent_MakeAvailable(json)

target_link_libraries(advent2015 PRIVATE nlohmann_json::nlohmann_json)

# Include resources in binary dir
file(GLOB_RECURSE RESOURCE_FILES
    RELATIVE ${CMAKE_SOURCE_DIR}
    "*.txt"
)
file(GLOB_RECURSE EXCLUDE_FILES
    RELATIVE ${CMAKE_SOURCE_DIR}
    "CMakeLists*"
)
list(REMOVE_ITEM RESOURCE_FILES ${EXCLUDE_FILES})

foreach(RESOURCE ${RESOURCE_FILES})
    configure_file(${RESOURCE} ${RESOURCE})
endforeach()

# Install dest
install(TARGETS advent2015
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)


