const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = 3001;

app.use(cors());

const FOLDER_PATH = '/mnt/c/study/exams/leetcode'; // Adjust this path as needed

app.get('/files', async (req, res) => {
  try {
    const files = await fs.readdir(FOLDER_PATH);
    res.json(files);
  } catch (error) {
    res.status(500).json({ error: 'Error reading directory' });
  }
});

app.get('/file/:filename', async (req, res) => {
  try {
    const filePath = path.join(FOLDER_PATH, req.params.filename);
    const content = await fs.readFile(filePath, 'utf-8');
    res.json({ content });
  } catch (error) {
    res.status(500).json({ error: 'Error reading file' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
