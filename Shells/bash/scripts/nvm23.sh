#!/bin/bash

# Install or update nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Export nvm directory and load nvm into the current shell
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# Install and use Node.js version 23
nvm install 23
nvm alias default 23  # Set Node.js v23 as the default version for new shells
nvm use 23

# Display Node.js and npm versions to confirm
node -v
npm -v
