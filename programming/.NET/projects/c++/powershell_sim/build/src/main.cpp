#include "../include/shell.h"
#include <iostream>
#include <string>

int main() {
    Shell shell;
    std::string input;

    std::cout << "PowerShell Simulator v1.0\n";
    std::cout << "Type 'help' for available commands. Type 'exit' to quit.\n";

    while (true) {
        std::cout << "PS " << std::filesystem::current_path().string() << "> ";
        std::getline(std::cin, input);

        if (input == "exit") {
            break;
        }

        if (!input.empty()) {
            shell.executeCommand(input);
        }
    }

    return 0;
}
