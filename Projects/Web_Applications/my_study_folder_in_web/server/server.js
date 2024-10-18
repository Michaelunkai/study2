const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const ROOT_PATH = '/mnt/c/study';

function getDirectoryContents(dir) {
  const contents = fs.readdirSync(dir);
  return contents.map(item => {
    const fullPath = path.join(dir, item);
    const stats = fs.statSync(fullPath);
    return {
      name: item,
      isDirectory: stats.isDirectory(),
      path: fullPath.replace(ROOT_PATH, '')
    };
  });
}

wss.on('connection', (ws) => {
  console.log('Client connected');

  ws.on('message', (message) => {
    const data = JSON.parse(message);
    if (data.type === 'getContents') {
      const fullPath = path.join(ROOT_PATH, data.path);
      try {
        const contents = getDirectoryContents(fullPath);
        ws.send(JSON.stringify({ type: 'contents', data: contents }));
      } catch (error) {
        console.error('Error reading directory:', error);
        ws.send(JSON.stringify({ type: 'error', message: 'Error reading directory' }));
      }
    } else if (data.type === 'getFile') {
      const fullPath = path.join(ROOT_PATH, data.path);
      try {
        const content = fs.readFileSync(fullPath, 'utf-8');
        ws.send(JSON.stringify({ type: 'file', data: content }));
      } catch (error) {
        console.error('Error reading file:', error);
        ws.send(JSON.stringify({ type: 'error', message: 'Error reading file' }));
      }
    }
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

const PORT = 3001;
server.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
