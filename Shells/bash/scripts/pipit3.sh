#!/bin/bash

# Function to check if a package exists on PyPI (using HTTP status)
check_pypi_package() {
    local package="$1"
    local response_code
    response_code=$(curl -s -o /dev/null -w "%{http_code}" "https://pypi.org/pypi/$package/json" 2>/dev/null)
    [[ "$response_code" == "200" ]]
}

# Find all Python files and extract unique import statements
echo "Scanning Python files for imports..."
imports=$(find . -name "*.py" -type f -exec grep -h "^import\|^from" {} \; 2>/dev/null | sort -u)

# Package mapping for import vs pip install names
declare -A package_mapping=(
    ["PIL"]="pillow"
    ["bs4"]="beautifulsoup4"
    ["yaml"]="pyyaml"
    ["cv2"]="opencv-python"
    ["sklearn"]="scikit-learn"
    ["docx"]="python-docx"
    ["dotenv"]="python-dotenv"
    ["speech_recognition"]="SpeechRecognition"
    ["google_auth_oauthlib"]="google-auth-oauthlib"
    ["googleapiclient"]="google-api-python-client"
    ["pyreadline"]="pyreadline3"
)

# Standard library and common skip modules
skip_modules="abc argparse array ast asyncio base64 bisect builtins calendar collections colorsys concurrent contextlib copy csv ctypes dataclasses datetime decimal difflib enum errno faulthandler filecmp fileinput fnmatch fractions functools gc getopt getpass gettext glob gzip hashlib heapq hmac html http importlib inspect io itertools json keyword linecache locale logging lzma math mmap modulefinder multiprocessing numbers operator os pathlib pickle pkg_resources platform plistlib pprint queue random re secrets select selectors shelve shlex shutil signal socket sqlite3 ssl stat statistics string subprocess sys tarfile tempfile textwrap threading time timeit tkinter token traceback types typing unicodedata unittest urllib uuid warnings wave weakref webbrowser xml zipfile zlib __future__ __main__ __builtin__ pip setup tests src utils app config main views"

# Additional problematic/local modules from previous run
skip_modules="$skip_modules backend background background_images buttons components dialogs docker_commands docker_ops kokoro main_window network_ops persistence tags tabs terminal ui_components workers"

# Platform-specific exclusions
platform=$(uname)
if [[ "$platform" == "Linux" ]]; then
    skip_modules="$skip_modules win32com winreg winshell win32"
elif [[ "$platform" == MINGW* || "$platform" == CYGWIN* || "$platform" == MSYS* ]]; then
    skip_modules="$skip_modules posix"
fi

# Process imports to build package list
echo "Processing imports..."
packages=()
skipped_packages=()
while IFS= read -r line; do
    # Extract package name
    if [[ $line =~ ^import\ ([a-zA-Z0-9_]+) ]] || [[ $line =~ ^from\ ([a-zA-Z0-9_]+) ]]; then
        package="${BASH_REMATCH[1]}"
        
        # Skip standard, excluded, or local modules
        if [[ " $skip_modules " =~ " $package " ]]; then
            skipped_packages+=("$package (standard or local module)")
            continue
        fi
        
        # Skip local directories with __init__.py, setup.py, or pyproject.toml
        if [[ -d "./$package" && (-f "./$package/__init__.py" || -f "./$package/setup.py" || -f "./$package/pyproject.toml") ]]; then
            skipped_packages+=("$package (local directory)")
            continue
        fi
        
        # Map package name if needed
        [[ -n "${package_mapping[$package]}" ]] && package="${package_mapping[$package]}"
        
        # Check if package exists on PyPI
        if check_pypi_package "$package"; then
            packages+=("$package")
        else
            skipped_packages+=("$package (not found on PyPI)")
        fi
    fi
done <<< "$imports"

# Remove duplicates and empty entries
packages=($(echo "${packages[@]}" | tr ' ' '\n' | sort -u | grep .))
skipped_packages=($(echo "${skipped_packages[@]}" | tr ' ' '\n' | sort -u | grep .))

# Print skipped packages (if any)
if [ ${#skipped_packages[@]} -gt 0 ]; then
    echo "Skipped ${#skipped_packages[@]} packages:"
    for pkg in "${skipped_packages[@]}"; do
        echo "  - $pkg"
    done
else
    echo "No packages skipped."
fi

# Generate and execute pip install command
if [ ${#packages[@]} -gt 0 ]; then
    echo "Found ${#packages[@]} valid packages to install:"
    echo "${packages[*]}"
    echo "Installing all packages in one command..."
    
    # Execute pip install with real-time output
    if pip install --disable-pip-version-check --no-cache-dir "${packages[@]}"; then
        echo "All packages installed successfully."
    else
        echo "Some packages failed to install. Try installing individually with:"
        echo "pip install <package_name>"
        echo "Check the error messages above for details."
        exit 1
    fi
else
    echo "No external packages found to install."
fi

echo "Installation process complete."

