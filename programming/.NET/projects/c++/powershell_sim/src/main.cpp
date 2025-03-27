#include <iostream>
#include <string>
#include <filesystem>
#include <windows.h>
#include "../include/shell.h"

void setConsoleColor() {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_INTENSITY);
}

void resetConsoleColor() {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE);
}

std::string getCurrentPath() {
    return std::filesystem::current_path().string();
}

int main() {
    Shell shell;
    std::string input;
    bool running = true;

    // Set console title
    SetConsoleTitle(TEXT("C++ PowerShell Simulator"));

    while (running) {
        setConsoleColor();
        std::cout << "PS " << getCurrentPath() << "> ";
        resetConsoleColor();

        std::getline(std::cin, input);

        if (input == "exit") {
            running = false;
            continue;
        }

        if (!input.empty()) {
            shell.executeCommand(input);
        }
    }

    std::cout << "Exiting shell...\n";
    return 0;
}