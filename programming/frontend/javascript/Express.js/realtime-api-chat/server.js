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
const PORT = process.env.PORT || 3000;

// Serve static files from the 'public' directory
app.use(express.static('public'));

// Handle Socket.io connections
io.on('connection', (socket) => {
  console.log('A user connected:', socket.id);

  // Listen for 'chat message' events from clients
  socket.on('chat message', (msg) => {
    console.log(`Message from ${socket.id}: ${msg}`);
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
  console.log(`Server is running on http://localhost:${PORT}`);
});
