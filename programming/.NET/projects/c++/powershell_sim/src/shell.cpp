#include "../include/shell.h"
#include <iostream>
#include <sstream>
#include <filesystem>
#include <windows.h>
#include <cstdio>
#include <memory>
#include <stdexcept>
#include <string>
#include <array>
#include <algorithm>
#include <vector>
#include <fstream>

namespace fs = std::filesystem;

Shell::Shell() {
    initializeCommands();
}

void Shell::initializeCommands() {
    commands["cd"] = &Shell::changeDirectory;
    commands["dir"] = &Shell::listDirectory;
    commands["ls"] = &Shell::listDirectory;
    commands["clear"] = &Shell::clearScreen;
    commands["cls"] = &Shell::clearScreen;
    commands["help"] = &Shell::showHelp;
    commands["echo"] = &Shell::echo;
    commands["pwd"] = &Shell::printWorkingDirectory;
}

void Shell::executeCommand(const std::string& input) {
    std::istringstream iss(input);
    std::string command;
    iss >> command;

    if (commands.find(command) != commands.end()) {
        std::string args;
        std::getline(iss, args);
        // Trim leading whitespace from args
        args.erase(0, args.find_first_not_of(" \t"));
        (this->*commands[command])(args);
    } else {
        executeSystemCommand(input);
    }
}

void Shell::changeDirectory(const std::string& path) {
    try {
        if (path.empty() || path == " ") {
            // Print current directory if no path specified
            std::cout << fs::current_path().string() << std::endl;
            return;
        }

        fs::path newPath = path;
        fs::current_path(newPath);
    } catch (const fs::filesystem_error& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}

void Shell::listDirectory(const std::string& path) {
    try {
        fs::path dirPath = path.empty() ? fs::current_path() : fs::path(path);
        
        for (const auto& entry : fs::directory_iterator(dirPath)) {
            HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
            
            if (fs::is_directory(entry)) {
                SetConsoleTextAttribute(hConsole, FOREGROUND_BLUE | FOREGROUND_INTENSITY);
                std::cout << "[DIR] ";
            } else {
                SetConsoleTextAttribute(hConsole, FOREGROUND_GREEN | FOREGROUND_INTENSITY);
                std::cout << "[FILE] ";
            }
            
            std::cout << entry.path().filename().string() << std::endl;
            
            // Reset color
            SetConsoleTextAttribute(hConsole, FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE);
        }
    } catch (const fs::filesystem_error& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}

void Shell::clearScreen(const std::string&) {
    system("cls");
}

void Shell::showHelp(const std::string&) {
    std::cout << "Available commands:\n";
    std::cout << "  cd [path]     - Change directory\n";
    std::cout << "  dir/ls [path] - List directory contents\n";
    std::cout << "  clear/cls     - Clear screen\n";
    std::cout << "  echo [text]   - Display text\n";
    std::cout << "  pwd          - Print working directory\n";
    std::cout << "  help         - Show this help message\n";
    std::cout << "  exit         - Exit the shell\n";
}

void Shell::echo(const std::string& message) {
    std::cout << message << std::endl;
}

void Shell::printWorkingDirectory(const std::string&) {
    std::cout << fs::current_path().string() << std::endl;
}

std::string Shell::executeSystemCommand(const std::string& command) {
    std::array<char, 128> buffer;
    std::string result;
    
    // Create a pipe to execute the command
    auto pipe = _popen(command.c_str(), "r");
    
    if (!pipe) {
        throw std::runtime_error("popen() failed!");
    }
    
    // Read the output
    while (fgets(buffer.data(), buffer.size(), pipe) != nullptr) {
        std::cout << buffer.data();
        result += buffer.data();
    }
    
    auto rc = _pclose(pipe);
    
    if (rc != 0) {
        // If the command wasn't found or failed to execute
        if (result.empty()) {
            std::cerr << "'" << command << "' is not recognized as an internal or external command,\n";
            std::cerr << "operable program or batch file.\n";
        }
    }
    
    return result;
}