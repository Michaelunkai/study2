#ifndef SHELL_H
#define SHELL_H

#include <string>
#include <map>
#include <functional>
#include <vector>

class Shell {
public:
    Shell();
    void executeCommand(const std::string& input);

private:
    // Map of command names to member functions
    std::map<std::string, void (Shell::*)(const std::string&)> commands;
    
    // Command history
    std::vector<std::string> commandHistory;
    
    // Initialize command map
    void initializeCommands();
    
    // Built-in commands
    void changeDirectory(const std::string& path);
    void listDirectory(const std::string& path);
    void clearScreen(const std::string& args);
    void showHelp(const std::string& args);
    void echo(const std::string& message);
    void printWorkingDirectory(const std::string& args);
    
    // Execute external system commands
    std::string executeSystemCommand(const std::string& command);
};

#endif // SHELL_H