CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -Wno-format-truncation
TARGET = game_save_manager

# Detect OS
ifeq ($(OS),Windows_NT)
    # Windows-specific settings
    LIBS = -lshlwapi
    RM = del
    EXT = .exe
    DEFS = -D_WIN32
else
    # Linux/WSL settings
    LIBS = 
    RM = rm -f
    EXT = 
    DEFS = -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -D_GNU_SOURCE
endif

all: $(TARGET)

$(TARGET): main.c
	$(CC) $(CFLAGS) $(DEFS) -o $(TARGET)$(EXT) main.c $(LIBS)

clean:
	$(RM) $(TARGET)$(EXT)

windows:
	$(CC) $(CFLAGS) -D_WIN32 -o $(TARGET).exe main.c -lshlwapi

linux:
	$(CC) $(CFLAGS) -o $(TARGET) main.c -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -D_GNU_SOURCE
