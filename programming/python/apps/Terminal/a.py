import tkinter as tk
from tkinter import scrolledtext, font, PhotoImage, ttk
import subprocess
import re
import os
import sys
import datetime
import platform
import socket
import getpass
import time
import threading
import queue
import shlex
import json
import tempfile

class PowerShellEmulator:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.history = []
        self.history_index = 0
        self.current_dir = os.path.expanduser("~")
        self.execution_policy = "RemoteSigned"
        self.ps_version = "5.1.19041.3031"
        self.windows_version = "Microsoft Windows [Version 10.0.19044.1826]"
        self.proc = None
        self.command_queue = queue.Queue()
        self.output_queue = queue.Queue()
        self.running = True
        self.current_command = ""
        self.setup_terminal()
        
        # Initialize profile settings
        self.load_profile()
        
        # Show startup text
        self.show_startup_text()
        self.display_prompt()
        
        # Start threads
        self.output_thread = threading.Thread(target=self.process_output_queue, daemon=True)
        self.output_thread.start()
        self.command_thread = threading.Thread(target=self.command_processor, daemon=True)
        self.command_thread.start()

    def load_profile(self):
        """Load PowerShell profile settings and custom functions"""
        # Define known custom functions (from the provided code)
        self.custom_functions = {
            "cc": "Clear-Host",
            "ubu": "wsl -d Ubuntu --cd ~",
            "stack": 'python "F:\\study\\programming\\python\\apps\\scrapers\\StackOverFlow\\b.py"',
            "ccwsl": 'wsl --shutdown; Optimize-VHD -Path "C:\\wsl2\\ubuntu2\\ext4.vhdx" -Mode Full; Optimize-VHD -Path "C:\\wsl2\\ubuntu2\\ext4.vhdx" -Mode Quick; Optimize-VHD -Path "C:\\wsl2\\ubuntu\\ext4.vhdx" -Mode Full; Optimize-VHD -Path "C:\\wsl2\\ubuntu\\ext4.vhdx" -Mode Quick',
            "text": 'python F:\\study\\programming\\python\\apps\\media2text\\image2text\\a.py',
            "updatepip": 'C:\\Users\\micha\\AppData\\Local\\Microsoft\\WindowsApps\\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\\python.exe -m pip install --upgrade pip',
            "cchrome": 'Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue; Remove-Item -Path "$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\Default\\Cache" -Recurse -Force -ErrorAction SilentlyContinue; Remove-Item -Path "$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\Default\\Cookies" -Force -ErrorAction SilentlyContinue; Start-Process "chrome.exe"',
            "logs2": 'cd F:\\study\\Shells\\powershell\\scripts; ./automate_adding_latest_created_file_to_logs.ps1',
            "ccc": '# Start the WinOptimize application with elevated permissions\nStart-Process -FilePath "F:\\backup\\windowsapps\\installed\\myapps\\compiled_python\\windowsoptimize\\D\\dist\\WinOptimize" -Verb RunAs\n\n# Open all shortcuts in the specified directory except for "IObit Unlocker"\nGet-ChildItem -Path "C:\\Users\\micha\\Desktop\\maintaince" -Filter "*.lnk" | Where-Object { $_.Name -notmatch "IObit Unlocker" } | ForEach-Object { $shortcut = (New-Object -ComObject WScript.Shell).CreateShortcut($_.FullName); Start-Process -FilePath $shortcut.TargetPath -Verb RunAs }',
            "cccc": '# Close WinOptimize if it\'s running\nGet-Process -Name "WinOptimize" -ErrorAction SilentlyContinue | Stop-Process -Force\n\n# Get all shortcuts in the maintenance directory except IObit Unlocker\n$shortcuts = Get-ChildItem -Path "C:\\Users\\micha\\Desktop\\maintaince" -Filter "*.lnk" | Where-Object { $_.Name -notmatch "IObit Unlocker" }\n\n# Create shell object to read shortcuts\n$shell = New-Object -ComObject WScript.Shell',
            "ccleaner": '& "C:\\Program Files\\CCleaner\\CCleaner64.exe"',
            "bcu": '& "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\BCUninstaller\\BCUninstaller.lnk"',
            "ws": 'Start-Process "wt" -ArgumentList "$args"'  # Adding the ws function that seems to be in your profile
        }
        
        # Function helpers
        self.function_helper = {
            "cfun": self.show_function_definition
        }
        
        # Try to load real profile (if available)
        try:
            profile_path = os.path.join(os.path.expanduser("~"), "Documents", "WindowsPowerShell", "Microsoft.PowerShell_profile.ps1")
            if os.path.exists(profile_path):
                # Extract functions from PowerShell profile
                self.extract_profile_functions(profile_path)
        except Exception as e:
            print(f"Error loading profile: {e}")
    
    def extract_profile_functions(self, profile_path):
        """Extract function definitions from PowerShell profile"""
        try:
            with open(profile_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Simple function extraction (basic implementation)
            function_pattern = r'function\s+([a-zA-Z0-9_-]+)\s*\{([^}]*)\}'
            for match in re.finditer(function_pattern, content, re.DOTALL):
                func_name = match.group(1).strip()
                func_body = match.group(2).strip()
                if func_name and func_name not in self.custom_functions:
                    self.custom_functions[func_name] = func_body
                    
            # Extract aliases
            alias_pattern = r'Set-Alias\s+(?:-Name\s+)?([a-zA-Z0-9_-]+)\s+(?:-Value\s+)?([a-zA-Z0-9_-]+)'
            for match in re.finditer(alias_pattern, content):
                alias_name = match.group(1).strip()
                alias_value = match.group(2).strip()
                if alias_name and alias_name not in self.custom_functions:
                    self.custom_functions[alias_name] = alias_value
        except Exception as e:
            print(f"Error parsing profile: {e}")

    def setup_window(self):
        self.root.title("Windows PowerShell")
        self.bg_color = '#012456'
        self.text_color = '#EEEEEE'
        self.cursor_color = '#FFFFFF'
        self.root.configure(bg=self.bg_color)
        
        try:
            self.root.iconbitmap('powershell.ico')
        except tk.TclError:
            pass
            
        # Set window size and position
        window_width = 900
        window_height = 550
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Make window resizable
        self.root.minsize(500, 350)
        
        # Protocol for window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_terminal(self):
        # Create a custom font
        custom_font = font.Font(family="Consolas", size=10)
        
        # Create a frame for the terminal
        terminal_frame = tk.Frame(self.root, bg=self.bg_color)
        terminal_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(terminal_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create the text box
        self.output_box = scrolledtext.ScrolledText(
            terminal_frame, 
            bg=self.bg_color, 
            fg=self.text_color, 
            wrap=tk.WORD, 
            font=custom_font,
            borderwidth=0,
            relief="flat",
            insertbackground=self.cursor_color,
            insertwidth=2,
            insertontime=600,
            insertofftime=300,
            padx=5,
            pady=5,
            yscrollcommand=scrollbar.set
        )
        self.output_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.output_box.yview)
        
        # Set up tags for syntax highlighting
        self.output_box.tag_configure("error", foreground="#FF6B70")
        self.output_box.tag_configure("warning", foreground="#FFD700")
        self.output_box.tag_configure("success", foreground="#66FF66")
        self.output_box.tag_configure("info", foreground="#6A5ACD")
        self.output_box.tag_configure("command", foreground="#E5E500")
        self.output_box.tag_configure("path", foreground="#4EC9B0")
        self.output_box.tag_configure("prompt", foreground="#CCCCCC")
        self.output_box.tag_configure("param", foreground="#9CDCFE")
        self.output_box.tag_configure("output", foreground="#FFFFFF")
        self.output_box.tag_configure("docker", foreground="#00BFFF")
        
        # Bind events
        self.output_box.bind('<Return>', self.on_enter_key)
        self.output_box.bind('<KeyPress>', self.enforce_prompt_readonly)
        self.output_box.bind('<KeyRelease>', self.color_syntax)
        self.output_box.bind('<Up>', self.navigate_history_up)
        self.output_box.bind('<Down>', self.navigate_history_down)
        self.output_box.bind('<Tab>', self.handle_tab_completion)
        self.output_box.bind('<Control-c>', self.handle_ctrl_c)
        
        # Right-click menu
        self.setup_context_menu()
        
    def setup_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0, bg="#2D2D30", fg="white", activebackground="#3E3E40", activeforeground="white")
        self.context_menu.add_command(label="Copy", command=self.copy_selection)
        self.context_menu.add_command(label="Paste", command=self.paste_clipboard)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Select All", command=self.select_all)
        
        self.output_box.bind("<Button-3>", self.show_context_menu)
        
    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
            
    def copy_selection(self):
        if self.output_box.tag_ranges(tk.SEL):
            self.root.clipboard_clear()
            self.root.clipboard_append(self.output_box.get(tk.SEL_FIRST, tk.SEL_LAST))
            
    def paste_clipboard(self):
        try:
            text = self.root.clipboard_get()
            if self.output_box.compare(tk.INSERT, "<", "prompt_end"):
                self.output_box.mark_set(tk.INSERT, tk.END)
            self.output_box.insert(tk.INSERT, text)
        except:
            pass
            
    def select_all(self):
        self.output_box.tag_add(tk.SEL, "1.0", tk.END)
        self.output_box.mark_set(tk.INSERT, tk.END)

    def show_startup_text(self):
        startup_text = """Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Try the new cross-platform PowerShell https://aka.ms/pscore6

Loading personal and system profiles...
"""
        self.output_box.insert(tk.END, startup_text)
        
        # Show a message that profile has been loaded
        self.output_box.insert(tk.END, f"\nLoaded {len(self.custom_functions)} custom functions and aliases.\n")

    def display_prompt(self):
        prompt = f"PS {self.current_dir}> "
        self.output_box.insert(tk.END, prompt)
        self.output_box.tag_add("prompt", f"end-{len(prompt)}c", "end-1c")
        self.output_box.mark_set("prompt_end", "end-1c")
        self.output_box.mark_set("input_end", tk.END)
        self.output_box.mark_gravity("prompt_end", "left")
        self.output_box.see(tk.END)

    def on_enter_key(self, event):
        # Get the command
        command = self.output_box.get("prompt_end", "end-1c").strip()
        self.current_command = command
        
        # Add to history
        if command:
            self.history.append(command)
            self.history_index = len(self.history)
        
        # Add a newline after the command
        self.output_box.insert(tk.END, "\n")
        
        # Process the command
        if command:
            self.command_queue.put(command)
        else:
            # Just show a new prompt for empty commands
            self.display_prompt()
        
        return 'break'

    def command_processor(self):
        """Thread to process commands from the queue"""
        while self.running:
            try:
                command = self.command_queue.get(timeout=0.1)
                if command:
                    self.process_command(command)
                    self.root.after(0, self.display_prompt)
            except queue.Empty:
                pass
            except Exception as e:
                self.output_queue.put((f"Error processing command: {str(e)}\n", "error"))
                self.root.after(0, self.display_prompt)

    def process_output_queue(self):
        """Thread to process output queue and update UI"""
        while self.running:
            try:
                item = self.output_queue.get(timeout=0.1)
                if item:
                    text, tag = item
                    self.root.after(0, lambda t=text, g=tag: self.append_output(t, g))
            except queue.Empty:
                pass

    def append_output(self, text, tag=None):
        """Append text to the output box with optional tag"""
        if text:
            self.output_box.insert(tk.END, text)
            if tag:
                self.output_box.tag_add(tag, f"end-{len(text)}c", "end-1c")
            self.output_box.see(tk.END)
            self.root.update_idletasks()

    def process_command(self, command):
        """Process a command entered by the user"""
        # Handle built-in commands
        cmd_parts = command.split(None, 1)
        cmd_name = cmd_parts[0].lower() if cmd_parts else ""
        args = cmd_parts[1] if len(cmd_parts) > 1 else ""
        
        # Special handling for directory listing commands
        if cmd_name in ['ls', 'dir', 'get-childitem']:
            try:
                # Create the PowerShell command with proper formatting
                ps_command = '''
                Get-ChildItem | Format-Table -AutoSize @{Label="Mode";Expression={$_.Mode};Alignment="Left";Width=20},
                @{Label="LastWriteTime";Expression={$_.LastWriteTime};Alignment="Left";Width=20},
                @{Label="Length";Expression={$_.Length};Alignment="Right";Width=10},
                @{Label="Name";Expression={$_.Name};Alignment="Left"}
                '''
                
                # Execute with pipe to Out-String to get proper formatting
                process = subprocess.run(
                    ['powershell', '-NoProfile', '-Command', f"{ps_command}"],
                    capture_output=True,
                    text=True,
                    cwd=self.current_dir
                )
                
                # Display the directory header
                self.output_queue.put((f"\n    Directory: {self.current_dir}\n\n", "path"))
                
                # Display the formatted output
                if process.stdout:
                    self.output_queue.put((process.stdout, "output"))
                if process.stderr:
                    self.output_queue.put((process.stderr, "error"))
                    
            except Exception as e:
                self.output_queue.put((f"Error listing directory: {str(e)}\n", "error"))
            return
            
        # Check for custom function helper commands
        if cmd_name in self.function_helper:
            self.function_helper[cmd_name](args)
            return
            
        # Handle built-in commands
        if cmd_name == "clear" or cmd_name == "cls" or cmd_name == "clear-host" or cmd_name == "cc":
            self.output_box.delete(1.0, tk.END)
            return
        elif cmd_name == "exit":
            self.running = False
            self.root.after(100, self.root.quit)
            return
        elif cmd_name == "cd" or cmd_name == "chdir" or cmd_name == "set-location":
            self.change_directory(command)
            return
        elif cmd_name == "pwd" or cmd_name == "get-location":
            self.output_queue.put((f"{self.current_dir}\n", "path"))
            return
            
        # Check for custom functions
        if cmd_name in self.custom_functions:
            # Get the function body
            function_body = self.custom_functions[cmd_name]
            
            # Check if it's a reference to another command or a full script
            if function_body.count('\n') == 0 and not function_body.startswith('#'):
                # It's likely a simple alias or command
                self.output_queue.put((f"Executing alias: {cmd_name} -> {function_body}\n", "info"))
                
                # Handle special case for 'ws' command (Windows Terminal)
                if cmd_name == "ws":
                    try:
                        # Use direct subprocess call instead of PowerShell wrapper
                        if args:
                            # Strip quotes from args if present
                            clean_args = args.strip('"\'')
                            full_cmd = f"wt {clean_args}"
                            subprocess.Popen(full_cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            self.output_queue.put((f"Started Windows Terminal with args: {args}\n", "info"))
                        else:
                            subprocess.Popen("wt", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            self.output_queue.put(("Started Windows Terminal\n", "info"))
                    except Exception as e:
                        self.output_queue.put((f"Error starting Windows Terminal: {str(e)}\n", "error"))
                    return
                
                # Execute the aliased command (with args if provided)
                if args:
                    self.execute_powershell(f"{function_body} {args}")
                else:
                    self.execute_powershell(function_body)
            else:
                # It's a complex script function - handle with inline execution instead of temp file
                self.output_queue.put((f"Executing function: {cmd_name}\n", "info"))
                
                # Create a PowerShell command that defines and invokes the function in one step
                ps_command = f"""
                function __TempFunction {{ 
                    {function_body}
                }}
                
                # Call the function with arguments
                __TempFunction {args}
                """
                # Execute the inline function
                self.execute_powershell(ps_command)
            return
            
        # Special handling for docker commands to capture real-time output
        if cmd_name == "docker":
            self.execute_docker_command(command)
            return
            
        # Execute through PowerShell for all other commands
        self.execute_powershell(command)

    def execute_docker_command(self, command):
        """Special handler for docker commands with real-time output"""
        try:
            # Start the process
            process = subprocess.Popen(
                ["powershell", "-Command", command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Function to read output in real-time
            def read_output():
                while process.poll() is None:
                    output = process.stdout.readline()
                    if output:
                        self.output_queue.put((output, "docker"))
                    
                    error = process.stderr.readline()
                    if error:
                        self.output_queue.put((error, "error"))
                
                # Get any remaining output
                output, error = process.communicate()
                if output:
                    self.output_queue.put((output, "docker"))
                if error:
                    self.output_queue.put((error, "error"))
            
            # Start reading output in a separate thread
            output_thread = threading.Thread(target=read_output)
            output_thread.daemon = True
            output_thread.start()
            
            # Keep a reference to the process
            self.proc = process
            
        except Exception as e:
            self.output_queue.put((f"Error executing docker command: {str(e)}\n", "error"))

    def execute_powershell(self, command):
        """Execute a command in PowerShell and capture output"""
        try:
            # Create a full PowerShell command with proper environment
            ps_command = f'''
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User");
            $ErrorActionPreference = "Continue";
            Set-Location '{self.current_dir}';
            {command}
            '''
            
            # Start the process
            process = subprocess.Popen(
                ["powershell", "-NoProfile", "-Command", ps_command],  # Added -NoProfile to avoid loading profile again
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Function to read output in real-time
            def read_output():
                while process.poll() is None:
                    output = process.stdout.readline()
                    if output:
                        self.output_queue.put((output, "output"))
                    
                    error = process.stderr.readline()
                    if error:
                        self.output_queue.put((error, "error"))
                
                # Get any remaining output
                output, error = process.communicate()
                if output:
                    self.output_queue.put((output, "output"))
                if error:
                    self.output_queue.put((error, "error"))
                    
                # Update current directory
                try:
                    location_proc = subprocess.run(
                        ["powershell", "-Command", "(Get-Location).Path"],
                        capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    if location_proc.returncode == 0:
                        new_dir = location_proc.stdout.strip()
                        if new_dir and os.path.isdir(new_dir):
                            self.current_dir = new_dir
                except Exception:
                    pass  # Ignore errors reading current directory
            
            # Start reading output in a separate thread
            output_thread = threading.Thread(target=read_output)
            output_thread.daemon = True
            output_thread.start()
            
            # Keep a reference to the process
            self.proc = process
            
        except Exception as e:
            self.output_queue.put((f"Error executing command: {str(e)}\n", "error"))

    def show_function_definition(self, function_name=None):
        """Show the definition of a function using the cfun command"""
        if not function_name:
            self.output_queue.put(("\nUsage: cfun <function_name>\n", None))
            return
            
        function_name = function_name.strip()
        
        if function_name in self.custom_functions:
            content = self.custom_functions[function_name]
            
            # Format the function definition as displayed in the example
            output = f"\n> function {function_name} {{\n      "
            # Replace newlines with newline + 6 spaces for formatting
            formatted_content = content.replace("\n", "\n      ")
            output += formatted_content
            output += "\n  }\n\n"
            
            self.output_queue.put((output, None))
        else:
            self.output_queue.put((f"\nFunction '{function_name}' not found.\n", None))

    def change_directory(self, command):
        parts = command.split(" ", 1)
        if len(parts) == 1:
            # Just 'cd' with no args shows current directory
            self.output_queue.put((f"{self.current_dir}\n", "path"))
            return
            
        path = parts[1].strip().strip('"').strip("'")
        
        # Handle special paths
        if path == "..":
            # Move up one directory
            parent = os.path.dirname(self.current_dir)
            if parent and parent != self.current_dir:  # Prevent going above C:\
                self.current_dir = parent
            return
        elif path == "~":
            # Home directory
            self.current_dir = os.path.expanduser("~")
            return
        elif path in ["\\", "/"]:
            # Root directory
            self.current_dir = "C:\\"
            return
            
        # Handle absolute paths
        if re.match(r'^[A-Za-z]:\\', path):
            if os.path.isdir(path):
                self.current_dir = path
            else:
                self.output_queue.put((f"The path '{path}' does not exist.\n", "error"))
            return
            
        # Handle relative paths
        if not path.startswith("\\"):
            new_path = os.path.join(self.current_dir, path)
            if os.path.isdir(new_path):
                self.current_dir = new_path
            else:
                self.output_queue.put((f"The path '{new_path}' does not exist.\n", "error"))
            return
            
        # Handle paths starting with \
        new_path = f"{self.current_dir.split(':')[0]}:{path}"
        if os.path.isdir(new_path):
            self.current_dir = new_path
        else:
            self.output_queue.put((f"The path '{new_path}' does not exist.\n", "error"))

    def enforce_prompt_readonly(self, event):
        # Prevent line breaks in command area
        if event.keysym == "Return":
            return # This will be handled by on_enter_key
            
        # Check if trying to edit before prompt
        if event.keysym == "BackSpace" and self.output_box.compare(tk.INSERT, "<=", "prompt_end"):
            return 'break'
        elif event.keysym in ["Left", "Right"] and self.output_box.compare(tk.INSERT, "<", "prompt_end"):
            if event.keysym == "Right":
                self.output_box.mark_set(tk.INSERT, "prompt_end")
            return 'break'
        elif event.keysym == "Home":
            self.output_box.mark_set(tk.INSERT, "prompt_end")
            return 'break'
        elif self.output_box.compare(tk.INSERT, "<", "prompt_end"):
            self.output_box.mark_set(tk.INSERT, "prompt_end")
        
        # Update input_end marker
        if self.output_box.compare(tk.INSERT, ">", "prompt_end"):
            self.output_box.mark_set("input_end", tk.INSERT)

    def color_syntax(self, event=None):
        # Remove all command tags
        self.output_box.tag_remove("command", "prompt_end", "end-1c")
        self.output_box.tag_remove("param", "prompt_end", "end-1c")
        
        # Get the current command
        command_text = self.output_box.get("prompt_end", "end-1c")
        if not command_text.strip():
            return
            
        # Highlight the first word (command)
        first_space = command_text.find(" ")
        if first_space != -1:
            self.output_box.tag_add("command", "prompt_end", f"prompt_end+{first_space}c")
            
            # Highlight parameters (starting with -)
            for match in re.finditer(r'(-\w+)', command_text):
                start, end = match.span()
                self.output_box.tag_add("param", f"prompt_end+{start}c", f"prompt_end+{end}c")
        else:
            self.output_box.tag_add("command", "prompt_end", "end-1c")

    def navigate_history_up(self, event):
        if self.history and self.history_index > 0:
            self.history_index -= 1
            self.replace_current_command(self.history[self.history_index])
        return 'break'
        
    def navigate_history_down(self, event):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.replace_current_command(self.history[self.history_index])
        elif self.history_index == len(self.history) - 1:
            self.history_index = len(self.history)
            self.replace_current_command("")
        return 'break'
        
    def replace_current_command(self, new_command):
        self.output_box.delete("prompt_end", "end-1c")
        self.output_box.insert("prompt_end", new_command)
        self.output_box.mark_set("input_end", "end-1c")
        self.color_syntax()
        
    def handle_tab_completion(self, event):
        current_text = self.output_box.get("prompt_end", "end-1c").strip()
        if not current_text:
            return 'break'
            
        # Simple tab completion for common commands
        commands = ["Get-Process", "Get-Service", "Get-Content", "Get-ChildItem", 
                   "Set-Location", "Write-Output", "Clear-Host", "Get-Help",
                   "Invoke-Expression", "Select-Object", "Where-Object",
                   "docker", "docker-compose", "git", "npm", "python"]
        
        # Add custom functions to tab completion
        commands.extend(self.custom_functions.keys())
        
        # Find partial matches
        if ' ' not in current_text:  # Only complete the command part
            matches = [cmd for cmd in commands if cmd.lower().startswith(current_text.lower())]
            
            if len(matches) == 1:
                self.replace_current_command(matches[0])
            elif len(matches) > 1:
                self.output_box.insert("end-1c", "\n")
                for match in matches:
                    self.output_box.insert("end-1c", match + "\n")
                self.display_prompt()
                self.output_box.insert("prompt_end", current_text)
                
        return 'break'
    
    def handle_ctrl_c(self, event):
        """Handle Ctrl+C to terminate current process or copy selection"""
        # If there's a selection, handle copy
        if self.output_box.tag_ranges(tk.SEL):
            self.copy_selection()
            return 'break'
            
        # If there's a running process, terminate it
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            self.output_queue.put(("\n^C\n", "error"))
            self.proc = None
        else:
            # If no process, just show ^C and new prompt
            self.output_box.insert(tk.END, "\n^C\n")
            self.display_prompt()
        
        return 'break'

    def on_close(self):
        """Clean up when window is closed"""
        self.running = False
        
        # Terminate any running process
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        
        # Stop threads
        if self.output_thread.is_alive():
            self.output_thread.join(timeout=1)
        if self.command_thread.is_alive():
            self.command_thread.join(timeout=1)
            
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = PowerShellEmulator(root)
    root.mainloop()
