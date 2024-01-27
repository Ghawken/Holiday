# python3
# auto_installer.py
# v.0.3
# currently using for code test, API 3.4 Indigo when released should do this automatically and can remove this code

import subprocess
from pathlib import Path
import sys

try:
    import indigo
except:
    pass

def update_holidays():
    current_directory = Path.cwd()  # Current directory
    parent_directory = current_directory.parent  # Parent directory
    pip_path = f"/Library/Frameworks/Python.framework/Versions/{sys.version_info.major}.{sys.version_info.minor}/bin/pip{sys.version_info.major}.{sys.version_info.minor}"
    pip_executable = pip_path #e.g. "/Library/Frameworks/Python.framework/Versions/3.11/bin/pip3.11"
    requirements_file = current_directory / "requirements.txt"
    install_dir = parent_directory / "Packages"
    installation_output = f"Updating Holiday Package in '{install_dir}'\n"
    # Execute the pip install command
    indigo.server.log(f"Checking for Holidays Update.")
    indigo.server.log(f"{installation_output}")
    try:
        result = subprocess.run([
            pip_executable, 'install', '--upgrade','holidays', '-t', str(install_dir), '--disable-pip-version-check'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # Save the output to a variable for later use
        installation_output += result.stdout.decode('utf-8', errors='replace')
        # Check if installation was successful
        if result.returncode != 0:
            indigo.server.log("An error occurred while installing packages.")
            indigo.server.log(f"{installation_output}")
            sys.exit(1)
        return installation_output
    except FileNotFoundError as e:
        error_message = f"File not found error: {e}"
        indigo.server.log(f"{error_message}")
        sys.exit(1)
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        indigo.server.log(f"{error_message}")
        sys.exit(1)