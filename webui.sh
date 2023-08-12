#!/usr/bin/env bash

# Checks to see if variable is set and non-empty.
# This is defined first, so we can use the function for some default variable values
env_var_exists() {
  if [[ -n "${!1}" ]]; then
    return 0
  else
    return 1
  fi
}

# If it is run with the sudo command, get the complete LD_LIBRARY_PATH environment variable of the system and assign it to the current environment,
# because it will be used later.
if [ -n "$SUDO_USER" ] || [ -n "$SUDO_COMMAND" ]; then
    echo "The sudo command resets the non-essential environment variables, we keep the LD_LIBRARY_PATH variable."
    export LD_LIBRARY_PATH=$(sudo -i printenv LD_LIBRARY_PATH)
fi

# This gets the directory the script is run from so pathing can work relative to the script where needed.
SCRIPT_DIR=$(cd -- "$(dirname -- "$0")" && pwd)

# Step into GUI local directory
cd "$SCRIPT_DIR" || exit 1

if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate" || exit 1
else
    echo "venv folder does not exist. Not activating..."
fi

# Determine the requirements file based on the system
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"

# Validate the requirements and run the script if successful
if python "$SCRIPT_DIR/setup/validate_requirements.py" -r "$REQUIREMENTS_FILE"; then
    python "$SCRIPT_DIR/webui/webui.py" "$@"
fi
