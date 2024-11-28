#!/bin/bash
# Script to get the current WSL2 distribution name
python3 -c "import os; print(os.getenv('WSL_DISTRO_NAME'))"
