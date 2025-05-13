#!/bin/ 

# Script Name: setup_sse_nodejs_realtime_express_project_for_data_streaming.sh
# Description: This script automates the setup of a Node.js Server-Sent Events (SSE) project using Express.
# It installs necessary dependencies, sets up the project files, creates a real-time SSE server, and runs it.

# Step 1: Install Node.js and npm using nvm (Node Version Manager)
if ! command -v nvm &> /dev/null; then
  echo "Installing nvm (Node Version Manager)..."
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash
  source ~/. rc
fi

# Step 2: Install the latest LTS version of Node.js
echo "Installing the latest LTS version of Node.js..."
nvm install --lts

# Step 3: Create the project directory and navigate into it
PROJECT_DIR="$HOME/sse-nodejs-server"
if [ ! -d "$PROJECT_DIR" ]; then
  echo "Creating project directory at $PROJECT_DIR..."
  mkdir "$PROJECT_DIR"
fi
cd "$PROJECT_DIR"

# Step 4: Initialize the Node.js project
echo "Initializing Node.js project..."
npm init -y

# Step 5: Install Express.js as the primary framework
echo "Installing Express.js..."
npm install express

# Step 6: Create the Server-Sent Events (SSE) server file
echo "Creating the SSE server file (server.js)..."
cat <<EOL > server.js
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from the 'public' directory
app.use(express.static('public'));

// SSE route for real-time data streaming
app.get('/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.flushHeaders(); // Flush headers to establish SSE connection

  const sendTimeData = () => {
    const eventData = {
      timestamp: new Date().toISOString(),
      message: 'Real-time data streaming from SSE server',
    };
    res.write(\`data: \${JSON.stringify(eventData)}\n\n\`);
  };

  // Send data every 5 seconds
  const intervalID = setInterval(sendTimeData, 5000);

  // Cleanup when the client disconnects
  req.on('close', () => {
    clearInterval(intervalID);
    res.end();
    console.log('Client disconnected from SSE stream.');
  });
});

// Handle non-SSE routes
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html');
});

// Start the server
app.listen(PORT, () => {
  console.log(\`SSE server is running on port \${PORT}\`);
});
EOL

# Step 7: Create the 'public' directory for serving static assets and the client HTML
echo "Creating client-side HTML file in 'public/index.html'..."
mkdir -p public
cat <<EOL > public/index.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SSE Real-Time Data Streaming</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background-color: #f4f4f9;
    }
    .container {
      background-color: #ffffff;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      max-width: 600px;
      width: 100%;
    }
    h1 {
      text-align: center;
      color: #333;
    }
    #messages {
      margin-top: 20px;
      border: 1px solid #ddd;
      padding: 10px;
      height: 200px;
      overflow-y: auto;
      background-color: #fafafa;
    }
    .message {
      padding: 10px;
      border-bottom: 1px solid #eee;
      font-size: 14px;
    }
    .message:last-child {
      border-bottom: none;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Real-Time Data Streaming with SSE</h1>
    <div id="messages">Waiting for updates...</div>
  </div>

  <script>
    const eventSource = new EventSource('/events');
    const messagesDiv = document.getElementById('messages');

    eventSource.onmessage = function(event) {
      const data = JSON.parse(event.data);
      const messageElement = document.createElement('div');
      messageElement.className = 'message';
      messageElement.textContent = \`[\${data.timestamp}] - \${data.message}\`;
      messagesDiv.appendChild(messageElement);
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    };

    eventSource.onerror = function(err) {
      console.error('EventSource failed:', err);
      eventSource.close();
    };
  </script>
</body>
</html>
EOL

# Step 8: Start the Node.js SSE server
echo "Starting the SSE server..."
node server.js
