#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <ctype.h>
#include <limits.h>
#include <signal.h>
#include <time.h>
#include <sys/types.h>  // NEW: Add this include for lstat declaration

#ifdef _WIN32
// Windows-specific includes
#include <windows.h>
#include <shlwapi.h>
#include <direct.h>
#pragma comment(lib, "shlwapi.lib")
#define DIR_SEPARATOR '\\'
#define MKDIR(dir) _mkdir(dir)
#else
// Linux-specific includes
#include <unistd.h>
#include <dirent.h>
#include <libgen.h>
#include <strings.h>
#define DIR_SEPARATOR '/'
#define MKDIR(dir) mkdir(dir, 0755)
#endif

#define MAX_PATH_LENGTH 512
#define MAX_GAMES 100

typedef struct {
    char name[256];
    char save_path[MAX_PATH_LENGTH];
    unsigned long long size;
    int is_game;
    int valid;
} GameSave;

GameSave detected_games[MAX_GAMES];
int game_count = 0;

#ifdef _WIN32
const char* common_save_locations[] = {
    "%USERPROFILE%\\Documents\\My Games",
    "%USERPROFILE%\\Saved Games",
    "%APPDATA%\\",
    "%LOCALAPPDATA%\\",
    "%PROGRAMDATA%\\",
    "C:\\Program Files (x86)\\Steam\\userdata",
    "C:\\Program Files\\Epic Games",
    "C:\\Program Files\\",
    "C:\\Program Files (x86)\\",
    "%USERPROFILE%\\Documents\\",
    NULL
};
#else
const char* common_save_locations[] = {
    "/mnt/c/Users/*/Documents/My Games",
    "/mnt/c/Users/*/Saved Games",
    "/mnt/c/Users/*/AppData/Roaming",
    "/mnt/c/Users/*/AppData/Local",
    "/mnt/c/ProgramData",
    "/mnt/c/Program Files (x86)/Steam/userdata",
    "/mnt/c/Program Files/Epic Games",
    "/mnt/c/Program Files/",
    "/mnt/c/Program Files (x86)/",
    "/mnt/c/Users/*/Documents/",
    "~/.steam/steam/userdata",
    "~/.local/share/",
    "~/.config/",
    "/usr/local/",
    "/opt/",
    NULL
};
#endif

int str_case_cmp(const char *s1, const char *s2) {
#ifdef _WIN32
    return _stricmp(s1, s2);
#else
    return strcasecmp(s1, s2);
#endif
}

char* str_to_lower(char* s) {
    for(char *p = s; *p; p++) {
        *p = tolower((unsigned char)*p);
    }
    return s;
}

void expand_path(const char* path, char* expanded, size_t size) {
#ifdef _WIN32
    ExpandEnvironmentStrings(path, expanded, MAX_PATH_LENGTH);
#else
    if (path[0] == '~' && (path[1] == '/' || path[1] == '\0')) {
        const char *home = getenv("HOME");
        if (home) {
            snprintf(expanded, size, "%s%s", home, path+1);
            return;
        }
    }
    strncpy(expanded, path, size);
    expanded[size-1] = '\0';
#endif
}

int directory_exists(const char* path) {
    struct stat info;
    if (stat(path, &info) != 0) return 0;
    return S_ISDIR(info.st_mode);
}

int is_save_directory(const char* path) {
    char possible_extensions[][10] = {".sav", ".save", ".dat", "savegame"};
    DIR* dir = opendir(path);
    if (!dir) return 0;
    struct dirent* entry;
    int is_save = 0;
    while ((entry = readdir(dir)) != NULL) {
#ifdef _WIN32
        if (entry->d_type == DT_REG) {
#else
        struct stat st;
        char full_path[MAX_PATH_LENGTH];
        snprintf(full_path, sizeof(full_path), "%s/%s", path, entry->d_name);
        if (stat(full_path, &st) == 0 && S_ISREG(st.st_mode)) {
#endif
            char name[256];
            strncpy(name, entry->d_name, sizeof(name)-1);
            name[sizeof(name)-1] = '\0';
            char* ext = strrchr(name, '.');
            if (ext) {
                for (int i = 0; i < sizeof(possible_extensions)/sizeof(possible_extensions[0]); i++) {
                    if (str_case_cmp(ext, possible_extensions[i]) == 0) {
                        is_save = 1;
                        break;
                    }
                }
            }
            char* lowername = str_to_lower(name);
            if (strstr(lowername, "save") || strstr(lowername, "profile")) {
                is_save = 1;
            }
        }
        if (is_save) break;
    }
    closedir(dir);
    return is_save;
}

void extract_game_name(const char* path, char* name, size_t size) {
#ifdef _WIN32
    const char* last_slash = strrchr(path, '\\');
#else
    const char* last_slash = strrchr(path, '/');
#endif
    if (last_slash) {
        strncpy(name, last_slash + 1, size - 1);
        name[size-1] = '\0';
    } else {
        strncpy(name, path, size - 1);
        name[size-1] = '\0';
    }
}

void safe_path_join(char* dest, size_t dest_size, const char* path1, const char* path2, char separator) {
    size_t path1_len = strlen(path1);
    size_t path2_len = strlen(path2);
    size_t available = dest_size - path1_len - 2;
    size_t copy_len = (path2_len <= available) ? path2_len : available;
    strncpy(dest, path1, dest_size-1);
    dest[dest_size-1] = '\0';
    if (path1_len > 0 && path1[path1_len-1] != separator && path1_len+1 < dest_size) {
        dest[path1_len] = separator;
        dest[path1_len+1] = '\0';
    }
    strncat(dest, path2, copy_len);
    dest[dest_size-1] = '\0';
}

const char* known_game_patterns[] = {
    "minecraft", "skyrim", "fallout", "witcher", "doom", "destiny",
    "borderlands", "gta", "grand theft auto", "halo", "bioshock", 
    "call of duty", "battlefield", "fortnite", "league of legends",
    "assassin's creed", "assassins creed", "far cry", "mass effect", "dark souls",
    "civilization", "final fantasy", "resident evil", "portal", "half-life",
    "counter-strike", "tomb raider", "crysis", "diablo", "world of warcraft",
    "warcraft", "starcraft", "overwatch", "rocket league", "red dead",
    "monster hunter", "street fighter", "fifa", "madden", "nba 2k",
    "elder scrolls", "cyberpunk", "pokemon", "zelda", "mario", 
    "sims", "rainbow six", "nier", "persona", "kingdom hearts",
    "god of war", "uncharted", "metal gear", "demon souls", "bloodborne",
    "sekiro", "horizon zero dawn", "death stranding", "control", "dishonored",
    "prey", "deus ex", "xcom", "dragon age", "mortal kombat",
    "tekken", "souls", "elden ring", "forza", "flight simulator",
    "age of empires", "total war", "valheim", "terraria", "stardew valley",
    "hollow knight", "hades", "subnautica", "among us", "factorio",
    NULL
};

const char* app_patterns[] = {
    "adobe", "microsoft", "autodesk", "office", "visual studio", "photoshop",
    "premiere", "aftereffects", "illustrator", "indesign", "acrobat",
    "blender", "unity", "unreal", "android studio", "xcode", "intellij",
    "webstorm", "pycharm", "phpstorm", "rider", "clion", "goland",
    "spotify", "itunes", "chrome", "firefox", "edge", "brave",
    "vlc", "media player", "davinci", "virtualbox", "vmware", "docker",
    "node", "java", "python", "ruby", "php", "mysql", "postgres", 
    "mongodb", "oracle", "sql server", "teams", "slack", "discord",
    "whatsapp", "telegram", "skype", "zoom", "dropbox", "onedrive",
    "google drive", "icloud", "creative cloud", "lightroom", "autocad",
    "revit", "maya", "3dsmax", "fusion", "inventor", "solidworks",
    NULL
};

unsigned long long get_directory_size(const char* path) {
    unsigned long long total_size = 0;
    char full_path[MAX_PATH_LENGTH];
    DIR* dir = opendir(path);
    if (!dir) return 0;
    struct dirent* entry;
    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            continue;
        if (strlen(entry->d_name) > 200)
            continue;
        if (strlen(path) + strlen(entry->d_name) + 2 >= MAX_PATH_LENGTH)
            continue;
#ifdef _WIN32
        safe_path_join(full_path, sizeof(full_path), path, entry->d_name, '\\');
#else
        safe_path_join(full_path, sizeof(full_path), path, entry->d_name, '/');
        struct stat lst;
        if (lstat(full_path, &lst) == 0 && S_ISLNK(lst.st_mode)) {
            continue;
        }
#endif
        struct stat st;
        if (stat(full_path, &st) == 0) {
            if (S_ISDIR(st.st_mode)) {
                if (strcmp(full_path, path) != 0) {
                    unsigned long long dir_size = get_directory_size(full_path);
                    if (ULLONG_MAX - total_size > dir_size) {
                        total_size += dir_size;
                    } else {
                        total_size = ULLONG_MAX;
                    }
                }
            } else if (S_ISREG(st.st_mode)) {
                if (ULLONG_MAX - total_size > (unsigned long long)st.st_size) {
                    total_size += (unsigned long long)st.st_size;
                } else {
                    total_size = ULLONG_MAX;
                }
            }
        }
    }
    closedir(dir);
    return total_size;
}

void format_size(unsigned long long size, char* buffer, size_t buffer_size) {
    const char* units[] = {"B", "KB", "MB", "GB", "TB"};
    int unit_index = 0;
    double size_d = (double)size;
    while (size_d >= 1024.0 && unit_index < 4) {
        size_d /= 1024.0;
        unit_index++;
    }
    snprintf(buffer, buffer_size, "%.2f %s", size_d, units[unit_index]);
}

int is_app_directory(const char* path) {
    if (strlen(path) >= MAX_PATH_LENGTH - 10)
        return 0;
    char dir_name[256];
    extract_game_name(path, dir_name, sizeof(dir_name));
    str_to_lower(dir_name);
    for (int i = 0; known_game_patterns[i] != NULL; i++) {
        if (strstr(dir_name, known_game_patterns[i])) {
            return 1;
        }
    }
    for (int i = 0; app_patterns[i] != NULL; i++) {
        if (strstr(dir_name, app_patterns[i])) {
            return 2;
        }
    }
    DIR* dir = opendir(path);
    if (!dir) return 0;
    struct dirent* entry;
    int app_indicators = 0;
    while ((entry = readdir(dir)) != NULL && app_indicators < 5) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            continue;
        if (strlen(entry->d_name) >= 250)
            continue;
        char filename[256];
        strncpy(filename, entry->d_name, sizeof(filename) - 1);
        filename[sizeof(filename) - 1] = '\0';
        str_to_lower(filename);
        if (strstr(filename, ".exe") || strstr(filename, ".dll") ||
            strstr(filename, ".app") || strstr(filename, ".msi") ||
            strstr(filename, "uninstall") || strstr(filename, "install") ||
            strstr(filename, "setup") || strstr(filename, "config") ||
            strstr(filename, "program") || strstr(filename, "application")) {
            app_indicators++;
        }
    }
    closedir(dir);
    if (app_indicators > 0) {
        return 2;
    }
    char *slash_count = strpbrk(path, "/\\");
    int slashes = 0;
    while (slash_count != NULL) {
        slashes++;
        slash_count = strpbrk(slash_count + 1, "/\\");
    }
    if (slashes > 7)
        return 0;
    if (strstr(path, "/proc") || strstr(path, "/sys") ||
        strstr(path, "/dev") || strstr(path, "/run") ||
        strstr(path, "System Volume Information"))
        return 0;
    unsigned long long dir_size = get_directory_size(path);
    if (dir_size > 52428800) {
        return 3;
    }
    return 0;
}

int is_game_save_directory(const char* path) {
    if (!is_save_directory(path)) {
        return 0;
    }
    char dir_name[256];
    extract_game_name(path, dir_name, sizeof(dir_name));
    str_to_lower(dir_name);
    for (int i = 0; known_game_patterns[i] != NULL; i++) {
        if (strstr(dir_name, known_game_patterns[i])) {
            return 1;
        }
    }
    if (strstr(dir_name, "game") || strstr(dir_name, "save") ||
        strstr(dir_name, "profile") || strstr(dir_name, "data") ||
        strstr(dir_name, "progress")) {
        DIR* dir = opendir(path);
        if (!dir) return 0;
        struct dirent* entry;
        int has_game_files = 0;
        while ((entry = readdir(dir)) != NULL) {
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
                continue;
            }
            char filename[256];
            strncpy(filename, entry->d_name, sizeof(filename) - 1);
            filename[sizeof(filename) - 1] = '\0';
            str_to_lower(filename);
            if (strstr(filename, "save") || strstr(filename, "profile") ||
                strstr(filename, "character") || strstr(filename, "slot") ||
                strstr(filename, "progress") || strstr(filename, "config.") ||
                strstr(filename, "options.") || strstr(filename, "game")) {
                has_game_files = 1;
                break;
            }
            char* ext = strrchr(filename, '.');
            if (ext) {
                if (strcmp(ext, ".dat") == 0 || strcmp(ext, ".sav") == 0 ||
                    strcmp(ext, ".save") == 0 || strcmp(ext, ".bin") == 0 ||
                    strcmp(ext, ".json") == 0 || strcmp(ext, ".xml") == 0 ||
                    strcmp(ext, ".cfg") == 0 || strcmp(ext, ".ini") == 0 ||
                    strcmp(ext, ".slot") == 0 || strcmp(ext, ".gamesave") == 0) {
                    has_game_files = 1;
                    break;
                }
            }
        }
        closedir(dir);
        return has_game_files;
    }
    return 0;
}

// Add a global variable to track scan start time and timeout
time_t scan_start_time = 0;
const int SCAN_TIMEOUT_SECONDS = 100;

void scan_directory(const char* base_path, int depth) {
    if (scan_start_time && (time(NULL) - scan_start_time) > SCAN_TIMEOUT_SECONDS) {
        return;
    }
    // Increased depth limit to ensure scanning all folders
    if (depth > 100) return;  // was: if (depth > 3) return;
    char path[MAX_PATH_LENGTH];
    strncpy(path, base_path, sizeof(path) - 1);
    path[sizeof(path) - 1] = '\0';
    DIR* dir = opendir(path);
    if (!dir) return;
    struct dirent* entry;
    while ((entry = readdir(dir)) != NULL && game_count < MAX_GAMES) {
        if (scan_start_time && (time(NULL) - scan_start_time) > SCAN_TIMEOUT_SECONDS) {
            break;
        }
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            continue;
        if (strlen(entry->d_name) > 200)
            continue;
        char full_path[MAX_PATH_LENGTH];
#ifdef _WIN32
        safe_path_join(full_path, sizeof(full_path), path, entry->d_name, '\\');
#else
        safe_path_join(full_path, sizeof(full_path), path, entry->d_name, '/');
        struct stat lst;
        if (lstat(full_path, &lst) == 0 && S_ISLNK(lst.st_mode)) {
            continue;
        }
#endif
        struct stat st;
        if (stat(full_path, &st) == 0 && S_ISDIR(st.st_mode)) {
            if (strlen(full_path) < MAX_PATH_LENGTH - 50) {
                int app_type = is_app_directory(full_path);
                if (app_type > 0 && game_count < MAX_GAMES - 1) {
                    extract_game_name(full_path, detected_games[game_count].name, sizeof(detected_games[game_count].name));
                    strncpy(detected_games[game_count].save_path, full_path, sizeof(detected_games[game_count].save_path) - 1);
                    detected_games[game_count].save_path[sizeof(detected_games[game_count].save_path) - 1] = '\0';
                    detected_games[game_count].valid = 1;
                    detected_games[game_count].is_game = (app_type == 1);
                    unsigned long long dir_size = get_directory_size(full_path);
                    detected_games[game_count].size = dir_size;
                    char size_str[20];
                    format_size(detected_games[game_count].size, size_str, sizeof(size_str));
                    printf("Found %s: %s (%s)\n", app_type == 1 ? "game" : "application",
                           detected_games[game_count].name, size_str);
                    game_count++;
                } else {
                    if (depth < 2) {
                        scan_directory(full_path, depth + 1);
                    }
                }
            }
        }
    }
    closedir(dir);
}

void scan_directory_old(const char* base_path, int depth) {
    if (scan_start_time && (time(NULL) - scan_start_time) > SCAN_TIMEOUT_SECONDS) {
        return;
    }
    if (depth > 100) return;  // was: if (depth > 3) return;
    char path[MAX_PATH_LENGTH];
    strncpy(path, base_path, sizeof(path) - 1);
    path[sizeof(path) - 1] = '\0';
    DIR* dir = opendir(path);
    if (!dir) return;
    struct dirent* entry;
    while ((entry = readdir(dir)) != NULL && game_count < MAX_GAMES) {
        if (scan_start_time && (time(NULL) - scan_start_time) > SCAN_TIMEOUT_SECONDS) {
            break;
        }
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            continue;
        char full_path[MAX_PATH_LENGTH];
#ifdef _WIN32
        safe_path_join(full_path, sizeof(full_path), path, entry->d_name, '\\');
#else
        safe_path_join(full_path, sizeof(full_path), path, entry->d_name, '/');
#endif
#ifdef _WIN32
        if (entry->d_type == DT_DIR) {
#else
        struct stat st;
        if (stat(full_path, &st) == 0 && S_ISDIR(st.st_mode)) {
#endif
            if (is_game_save_directory(full_path)) {
                extract_game_name(full_path, detected_games[game_count].name, sizeof(detected_games[game_count].name));
                strncpy(detected_games[game_count].save_path, full_path, sizeof(detected_games[game_count].save_path) - 1);
                detected_games[game_count].save_path[sizeof(detected_games[game_count].save_path) - 1] = '\0';
                detected_games[game_count].valid = 1;
                game_count++;
                printf("Found game save: %s\n", detected_games[game_count-1].name);
            } else {
                scan_directory(full_path, depth + 1);
            }
        }
    }
    closedir(dir);
}

void process_path_with_wildcards(const char* path, void (*callback)(const char*)) {
#ifndef _WIN32
    if (strstr(path, "*") != NULL) {
        char base_path[MAX_PATH_LENGTH];
        strncpy(base_path, path, sizeof(base_path) - 1);
        base_path[sizeof(base_path) - 1] = '\0';
        char* last_slash = strrchr(base_path, '/');
        if (!last_slash) return;
        *last_slash = '\0';
        const char* pattern = last_slash + 1;
        DIR* dir = opendir(base_path);
        if (!dir) return;
        struct dirent* entry;
        while ((entry = readdir(dir)) != NULL) {
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
                continue;
            if (strcmp(pattern, "*") == 0 || 
                (strncmp(pattern, "*", 1) == 0 && 
                 strstr(entry->d_name, pattern + 1) != NULL)) {
                char full_path[MAX_PATH_LENGTH];
                safe_path_join(full_path, sizeof(full_path), base_path, entry->d_name, '/');
                struct stat st;
                if (stat(full_path, &st) == 0 && S_ISDIR(st.st_mode)) {
                    char* second_wildcard = strchr(pattern, '/');
                    if (second_wildcard) {
                        char extended_path[MAX_PATH_LENGTH];
                        char temp_path[MAX_PATH_LENGTH];
                        safe_path_join(temp_path, sizeof(temp_path), base_path, entry->d_name, '/');
                        safe_path_join(extended_path, sizeof(extended_path), temp_path, second_wildcard + 1, '/');
                        callback(extended_path);
                    } else {
                        callback(full_path);
                    }
                }
            }
        }
        closedir(dir);
        return;
    }
#endif
    callback(path);
}

void process_single_path(const char* path) {
    if (scan_start_time && (time(NULL) - scan_start_time) > SCAN_TIMEOUT_SECONDS) {
        return;
    }
    char expanded_path[MAX_PATH_LENGTH];
    expand_path(path, expanded_path, sizeof(expanded_path));
    if (directory_exists(expanded_path)) {
        printf("Scanning %s for game saves...\n", expanded_path);
        scan_directory(expanded_path, 0);
    }
}

void scan_for_apps() {
    scan_start_time = time(NULL);
    printf("Scanning for applications and games...\n");
    game_count = 0;
    for (int i = 0; common_save_locations[i] != NULL; i++) {
        process_path_with_wildcards(common_save_locations[i], process_single_path);
    }
    int real_count = 0;
    unsigned long long total_size = 0;
    for (int i = 0; i < game_count; i++) {
        if (detected_games[i].valid) {
            real_count++;
            total_size += detected_games[i].size;
        }
    }
    char total_size_str[20];
    format_size(total_size, total_size_str, sizeof(total_size_str));
    printf("\nFound %d applications/games totaling %s.\n", real_count, total_size_str);
    // Sort detected apps from lightest to heaviest before printing details.
    sort_apps_by_size();
    if (real_count > 0) {
        printf("\nDetailed Application Information (sorted from lightest to heaviest):\n");
        printf("-------------------------------\n");
        for (int i = 0; i < game_count; i++) {
            if (detected_games[i].valid) {
                char size_str[20];
                format_size(detected_games[i].size, size_str, sizeof(size_str));
                printf("App %d: %s (%s)\n", i + 1, detected_games[i].name,
                       detected_games[i].is_game ? "Game" : "Application");
                printf("   Location: %s\n", detected_games[i].save_path);
                printf("   Size: %s\n\n", size_str);
            }
        }
        printf("-------------------------------\n");
    } else {
        printf("No applications or games were found.\n");
    }
}

void sort_apps_by_size(void) {
    for (int i = 0; i < game_count - 1; i++) {
        for (int j = 0; j < game_count - i - 1; j++) {
            if (detected_games[j].size > detected_games[j + 1].size) {
                GameSave temp = detected_games[j];
                detected_games[j] = detected_games[j + 1];
                detected_games[j + 1] = temp;
            }
        }
    }
}

int copy_directory(const char* src, const char* dst) {
    char command[MAX_PATH_LENGTH * 2];
#ifdef _WIN32
    snprintf(command, sizeof(command), "xcopy \"%s\" \"%s\" /E /I /H /Y", src, dst);
#else
    snprintf(command, sizeof(command), "cp -r \"%s\" \"%s\"", src, dst);
#endif
    return system(command);
}

int delete_directory(const char* path) {
    char command[MAX_PATH_LENGTH];
#ifdef _WIN32
    snprintf(command, sizeof(command), "rmdir /S /Q \"%s\"", path);
#else
    snprintf(command, sizeof(command), "rm -rf \"%s\"", path);
#endif
    return system(command);
}

void backup_game_save(int game_index, const char* backup_dir) {
    if (game_index < 0 || game_index >= game_count) {
        printf("Invalid game index.\n");
        return;
    }
    if (!directory_exists(backup_dir)) {
        printf("Creating backup directory...\n");
        MKDIR(backup_dir);
    }
    char game_backup_dir[MAX_PATH_LENGTH];
#ifdef _WIN32
    snprintf(game_backup_dir, sizeof(game_backup_dir), "%s\\%s", backup_dir, detected_games[game_index].name);
#else
    snprintf(game_backup_dir, sizeof(game_backup_dir), "%s/%s", backup_dir, detected_games[game_index].name);
#endif
    printf("Backing up '%s' to '%s'...\n", detected_games[game_index].name, game_backup_dir);
    if (copy_directory(detected_games[game_index].save_path, game_backup_dir) == 0) {
        printf("Backup completed successfully.\n");
    } else {
        printf("Backup failed.\n");
    }
}

void uninstall_application(int app_index) {
    if (app_index < 0 || app_index >= game_count) {
        printf("Invalid application index.\n");
        return;
    }
    printf("WARNING: This will attempt to uninstall '%s' and delete its data.\n", 
           detected_games[app_index].name);
    printf("Are you sure you want to continue? (y/n): ");
    char confirmation;
    scanf(" %c", &confirmation);
    if (confirmation == 'y' || confirmation == 'Y') {
        printf("Attempting to uninstall '%s'...\n", detected_games[app_index].name);
        int uninstaller_found = 0;
        char uninstaller_path[MAX_PATH_LENGTH];
        DIR* dir = opendir(detected_games[app_index].save_path);
        if (dir) {
            struct dirent* entry;
            while ((entry = readdir(dir)) != NULL) {
                char filename[256];
                strncpy(filename, entry->d_name, sizeof(filename) - 1);
                filename[sizeof(filename) - 1] = '\0';
                str_to_lower(filename);
                if (strstr(filename, "uninstall") || strstr(filename, "setup") || 
                    strstr(filename, "remove") || strstr(filename, "installer")) {
                    char* ext = strrchr(filename, '.');
                    if (ext && (strcmp(ext, ".exe") == 0 || strcmp(ext, ".msi") == 0)) {
                        char full_path[MAX_PATH_LENGTH];
#ifdef _WIN32
                        safe_path_join(full_path, sizeof(full_path), 
                                     detected_games[app_index].save_path, entry->d_name, '\\');
#else
                        safe_path_join(full_path, sizeof(full_path), 
                                     detected_games[app_index].save_path, entry->d_name, '/');
#endif
                        strcpy(uninstaller_path, full_path);
                        uninstaller_found = 1;
                        break;
                    }
                }
            }
            closedir(dir);
        }
        if (uninstaller_found) {
            printf("Found uninstaller. Running: %s\n", uninstaller_path);
#ifdef _WIN32
            ShellExecute(NULL, "open", uninstaller_path, NULL, NULL, SW_SHOW);
            printf("Uninstaller launched. Please follow the on-screen instructions.\n");
            printf("After uninstallation completes, do you want to delete any remaining files? (y/n): ");
            scanf(" %c", &confirmation);
            if (confirmation == 'y' || confirmation == 'Y') {
                if (delete_directory(detected_games[app_index].save_path) == 0) {
                    printf("Remaining files deleted successfully.\n");
                    detected_games[app_index].valid = 0;
                } else {
                    printf("Failed to delete remaining files.\n");
                }
            }
#else
            printf("Cannot run Windows uninstaller in Linux/WSL.\n");
            printf("Do you want to delete the application directory? (y/n): ");
            scanf(" %c", &confirmation);
            if (confirmation == 'y' || confirmation == 'Y') {
                if (delete_directory(detected_games[app_index].save_path) == 0) {
                    printf("Application files deleted successfully.\n");
                    detected_games[app_index].valid = 0;
                } else {
                    printf("Failed to delete application files.\n");
                }
            }
#endif
        } else {
            printf("No uninstaller found. Delete application directory? (y/n): ");
            scanf(" %c", &confirmation);
            if (confirmation == 'y' || confirmation == 'Y') {
                if (delete_directory(detected_games[app_index].save_path) == 0) {
                    printf("Application files deleted successfully.\n");
                    detected_games[app_index].valid = 0;
                } else {
                    printf("Failed to delete application files.\n");
                }
            } else {
                printf("Operation canceled.\n");
            }
        }
    } else {
        printf("Operation canceled.\n");
    }
}

void delete_game_save(int game_index) {
    if (game_index < 0 || game_index >= game_count) {
        printf("Invalid game index.\n");
        return;
    }
    printf("WARNING: This will permanently delete the save data for '%s'.\n", detected_games[game_index].name);
    printf("Are you sure you want to continue? (y/n): ");
    char confirmation;
    scanf(" %c", &confirmation);
    if (confirmation == 'y' || confirmation == 'Y') {
        printf("Deleting save data for '%s'...\n", detected_games[game_index].name);
        if (delete_directory(detected_games[game_index].save_path) == 0) {
            printf("Save data deleted successfully.\n");
            detected_games[game_index].valid = 0;
        } else {
            printf("Failed to delete save data.\n");
        }
    } else {
        printf("Operation canceled.\n");
    }
}

void quick_scan() {
    scan_start_time = time(NULL);
    printf("Running quick scan - only checking common Windows locations...\n");
    game_count = 0;
    const char* quick_locations[] = {
        "/mnt/c/Program Files",
        "/mnt/c/Program Files (x86)",
        "/mnt/c/ProgramData/Microsoft",
        "/mnt/c/Users/*/AppData/Local/Microsoft",
        "/mnt/c/Users/*/AppData/Roaming/Microsoft",
        "/mnt/c/Users/*/AppData/Local/Temp",
        NULL
    };
    for (int i = 0; quick_locations[i] != NULL; i++) {
        printf("Checking %s\n", quick_locations[i]);
        process_path_with_wildcards(quick_locations[i], process_single_path);
    }
    printf("\nQuick scan complete - found %d applications\n", game_count);
    if (game_count > 0) {
        sort_apps_by_size();
        printf("Top smallest items found:\n");
        printf("-------------------------------\n");
        int shown = 0;
        for (int i = 0; game_count && shown < 10; i++) {
            if (detected_games[i].valid) {
                char size_str[20];
                format_size(detected_games[i].size, size_str, sizeof(size_str));
                printf("%d. %s (%s)\n", shown + 1, detected_games[i].name, size_str);
                shown++;
            }
        }
        printf("-------------------------------\n");
    }
}

void show_menu() {
    int choice = 0;
    char backup_dir[MAX_PATH_LENGTH];
    while (1) {
        printf("\n=== Application Data Manager ===\n");
        printf("1. Scan for apps and games\n");
        printf("2. Quick scan (faster, WSL focused)\n");
        printf("3. List detected apps\n");
        printf("4. Sort apps by size (smallest first)\n");
        printf("5. Backup app/game data\n");
        printf("6. Uninstall app/game\n");
        printf("0. Exit\n");
        printf("Enter your choice: ");
        if (scanf("%d", &choice) != 1) {
            while (getchar() != '\n');
            continue;
        }
        switch (choice) {
            case 0:
                printf("Exiting...\n");
                return;
            case 1:
                game_count = 0;
                scan_for_apps();
                break;
            case 2:
                quick_scan();
                break;
            case 3:
                sort_apps_by_size();  // ensure lightest to heaviest order
                printf("\nDetected Applications and Games (sorted from lightest to heaviest):\n");
                if (game_count == 0) {
                    printf("No apps detected. Please scan first.\n");
                } else {
                    printf("-------------------------------\n");
                    for (int i = 0; i < game_count; i++) {
                        if (detected_games[i].valid) {
                            char size_str[20];
                            format_size(detected_games[i].size, size_str, sizeof(size_str));
                            printf("App %d: %s (%s)\n", i + 1, detected_games[i].name,
                                   detected_games[i].is_game ? "Game" : "Application");
                            printf("   Location: %s\n", detected_games[i].save_path);
                            printf("   Size: %s\n\n", size_str);
                        }
                    }
                    printf("-------------------------------\n");
                }
                break;
            case 4:
                if (game_count == 0) {
                    printf("No apps detected. Please scan first.\n");
                } else {
                    sort_apps_by_size();
                    printf("\nApplications Sorted by Size (Smallest First):\n");
                    printf("-------------------------------\n");
                    for (int i = 0; i < game_count; i++) {
                        if (detected_games[i].valid) {
                            char size_str[20];
                            format_size(detected_games[i].size, size_str, sizeof(size_str));
                            printf("App %d: %s (%s)\n", i + 1, detected_games[i].name, 
                                   detected_games[i].is_game ? "Game" : "Application");
                            printf("   Size: %s\n", size_str);
                            printf("   Location: %s\n\n", detected_games[i].save_path);
                        }
                    }
                    printf("-------------------------------\n");
                }
                break;
            case 5:
                if (game_count == 0) {
                    printf("No apps detected. Please scan first.\n");
                    break;
                }
                printf("\nSelect app/game to backup (1-%d): ", game_count);
                int backup_index;
                scanf("%d", &backup_index);
                backup_index--;
                if (backup_index >= 0 && backup_index < game_count && detected_games[backup_index].valid) {
                    printf("Enter backup directory path: ");
                    scanf(" %511[^\n]", backup_dir);
                    backup_game_save(backup_index, backup_dir);
                } else {
                    printf("Invalid selection.\n");
                }
                break;
            case 6:
                if (game_count == 0) {
                    printf("No apps detected. Please scan first.\n");
                    break;
                }
                printf("\nSelect app/game to uninstall (1-%d): ", game_count);
                int delete_index;
                scanf("%d", &delete_index);
                delete_index--;
                if (delete_index >= 0 && delete_index < game_count && detected_games[delete_index].valid) {
                    uninstall_application(delete_index);
                } else {
                    printf("Invalid selection.\n");
                }
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }
}

int main() {
    printf("Application Data Manager v1.1\n");
    printf("This program will scan your PC for applications and games,\n");
    printf("allowing you to find large apps, back them up, or remove them to save space.\n\n");
    show_menu();
    return 0;
}
