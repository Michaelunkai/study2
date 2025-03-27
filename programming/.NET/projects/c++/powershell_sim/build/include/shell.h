#pragma once
#include <string>
#include <map>
#include <functional>
#include <filesystem>

class Shell {
public:
    Shell();
    void executeCommand(const std::string& input);

private:
    typedef void (Shell::*CommandFunction)(const std::string&);
    std::map<std::string, CommandFunction> commands;

    void initializeCommands();
    void changeDirectory(const std::string& path);
    void listDirectory(const std::string& path);
    void clearScreen(const std::string& path);
    void showHelp(const std::string& path);
    void echo(const std::string& message);
    void printWorkingDirectory(const std::string& path);
    std::string executeSystemCommand(const std::string& command);
};
