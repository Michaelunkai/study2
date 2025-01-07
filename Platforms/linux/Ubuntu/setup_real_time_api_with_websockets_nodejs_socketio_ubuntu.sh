#!/bin/ 

##############################################################
# Script Name: setup_real_time_api_with_websockets_nodejs_socketio_ubuntu.sh
# Description: Automates the setup of a real-time API using WebSockets on Ubuntu with Node.js and Socket.io.
# Tools Used: Node.js, npm, Express, Socket.io
# Functionality: Installs necessary packages, sets up project structure, creates server and client files, and launches the server.
##############################################################

# Exit immediately if a command exits with a non-zero status.
set -e

# Variables
PROJECT_DIR="realtime-api"
NODE_VERSION="18.x" # Specify the Node.js version you want to install
PORT=3000

echo "Starting setup of Real-Time API with WebSockets using Node.js and Socket.io on Ubuntu."

# 1. Install Node.js and npm via NodeSource
echo "Installing Node.js and npm..."

curl -fsSL https://deb.nodesource.com/setup_$NODE_VERSION | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installations
echo "Verifying Node.js and npm installation..."
node_version=$(node -v)
npm_version=$(npm -v)
echo "Node.js Version: $node_version"
echo "npm Version: $npm_version"

# 2. Create Project Directory
echo "Creating project directory: $PROJECT_DIR"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# 3. Initialize npm
echo "Initializing npm..."
npm init -y

# 4. Install Express and Socket.io
echo "Installing Express and Socket.io..."
npm install express socket.io

# 5. Create server.js with necessary code
echo "Creating server.js..."
cat <<EOL > server.js
// Importing required modules
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

// Initialize Express app
const app = express();

// Create HTTP server
const server = http.createServer(app);

// Initialize Socket.io server
const io = new Server(server);

// Define the port
const PORT = process.env.PORT || $PORT;

// Serve static files from the 'public' directory
app.use(express.static('public'));

// Handle Socket.io connections
io.on('connection', (socket) => {
  console.log('A user connected:', socket.id);

  // Listen for 'chat message' events from clients
  socket.on('chat message', (msg) => {
    console.log(\`Message from \${socket.id}: \${msg}\`);
    // Broadcast the message to all connected clients
    io.emit('chat message', msg);
  });

  // Handle disconnections
  socket.on('disconnect', () => {
    console.log('User disconnected:', socket.id);
  });
});

// Start the server
server.listen(PORT, () => {
  console.log(\`Server is running on http://localhost:\${PORT}\`);
});
EOL

# 6. Create public directory and index.html
echo "Creating public directory and index.html..."
mkdir -p public
cat <<EOL > public/index.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Real-Time Chat Application</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f4f4;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    #chat-container {
      background: #fff;
      padding: 20px;
      border-radius: 5px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      width: 500px;
    }
    #messages {
      border: 1px solid #ccc;
      height: 300px;
      overflow-y: scroll;
      padding: 10px;
      margin-bottom: 10px;
    }
    #messages div {
      margin-bottom: 10px;
    }
    #form {
      display: flex;
    }
    #input {
      flex: 1;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 3px;
    }
    #send {
      padding: 10px 20px;
      border: none;
      background-color: #28a745;
      color: #fff;
      border-radius: 3px;
      cursor: pointer;
      margin-left: 10px;
    }
    #send:hover {
      background-color: #218838;
    }
  </style>
</head>
<body>
  <div id="chat-container">
    <h2>Real-Time Chat</h2>
    <div id="messages"></div>
    <form id="form" action="">
      <input id="input" autocomplete="off" placeholder="Type your message here..." />
      <button id="send">Send</button>
    </form>
  </div>

  <!-- Socket.io Client Library -->
  <script src="/socket.io/socket.io.js"></script>
  <script>
    // Initialize Socket.io client
    const socket = io();

    // Select DOM elements
    const form = document.getElementById('form');
    const input = document.getElementById('input');
    const messages = document.getElementById('messages');

    // Handle form submission
    form.addEventListener('submit', function(e) {
      e.preventDefault(); // Prevent form from submitting traditionally
      if (input.value.trim()) {
        // Emit 'chat message' event to the server
        socket.emit('chat message', input.value);
        input.value = ''; // Clear the input field
      }
    });

    // Listen for 'chat message' events from the server
    socket.on('chat message', function(msg) {
      const messageElement = document.createElement('div');
      messageElement.textContent = msg;
      messages.appendChild(messageElement);
      messages.scrollTop = messages.scrollHeight; // Auto-scroll to the latest message
    });

    // Optional: Notify when a user connects or disconnects
    socket.on('connect', () => {
      const connectMsg = document.createElement('div');
      connectMsg.style.color = 'green';
      connectMsg.textContent = 'A user has connected.';
      messages.appendChild(connectMsg);
    });

    socket.on('disconnect', () => {
      const disconnectMsg = document.createElement('div');
      disconnectMsg.style.color = 'red';
      disconnectMsg.textContent = 'A user has disconnected.';
      messages.appendChild(disconnectMsg);
    });
  </script>
</body>
</html>
EOL

# 7. Start the server in the background
echo "Launching the server..."
nohup node server.js > server.log 2>&1 &

echo "Real-Time API setup complete!"
echo "Access the application by navigating to http://localhost:$PORT in your web browser."
echo "Server logs are being written to server.log."
