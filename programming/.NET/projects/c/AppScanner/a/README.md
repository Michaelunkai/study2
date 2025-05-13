# Game Save Manager

A simple C application that scans your PC for game save data, allowing you to backup and delete game saves.

## Features

- Scan your PC for game saves in common locations
- List all detected games and their save locations
- Backup game saves to a location of your choice
- Delete game saves when no longer needed

## Building the Application

### On Windows

#### Using GCC (MinGW)

```
gcc -o game_save_manager.exe game_save_manager.c -lshlwapi
```

or simply:
```
make windows
```

#### Using Visual Studio

1. Create a new C++ console application
2. Add the `game_save_manager.c` file to your project
3. Add "Shlwapi.lib" to your project dependencies
4. Build the solution

### On Linux/WSL

**Note**: This application is designed primarily for Windows and uses Windows-specific APIs. To build on Linux/WSL for Windows usage:

```
make linux
```

The Linux version will have limited functionality as many Windows-specific functions are unavailable.

## Usage

1. Run the compiled executable
2. Select "Scan for game saves" to detect games on your system
3. Use "List detected games" to see what was found
4. Select "Backup game save" to copy a game's save data to another location
5. Select "Delete game save" to remove unwanted save data

## Common Save Locations

The application will scan these common locations for game save data:

- %USERPROFILE%\Documents\My Games
- %USERPROFILE%\Saved Games
- %APPDATA%
- %LOCALAPPDATA%
- %PROGRAMDATA%
- Steam userdata folder
- Epic Games folder

## Notes

- Running the delete function will permanently remove save data
- The application requires administrator privileges when accessing certain system folders
- Some games use unconventional save locations that might not be detected
