cmake_minimum_required(VERSION 3.10)
project(powershell_sim VERSION 1.0)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add source files
set(SOURCES
    src/main.cpp
    src/shell.cpp
)

# Add header files
set(HEADERS
    include/shell.h
)

# Add executable
add_executable(powershell_sim ${SOURCES} ${HEADERS})

# Include directories
target_include_directories(powershell_sim PRIVATE include)

# Set output directory
set_target_properties(powershell_sim PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)

# Add compiler flags
if(MSVC)
    target_compile_options(powershell_sim PRIVATE /W4)
else()
    target_compile_options(powershell_sim PRIVATE -Wall -Wextra -pedantic)
endif()

# Link libraries
if(WIN32)
    target_link_libraries(powershell_sim PRIVATE stdc++fs)
endif()

# Install target
install(TARGETS powershell_sim DESTINATION bin)

# Enable testing
enable_testing()

# Print status message
message(STATUS "PowerShell Simulator configuration complete")