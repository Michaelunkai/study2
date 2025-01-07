import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState('');

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const response = await axios.get('http://localhost:3001/files');
      setFiles(response.data);
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  };

  const fetchFileContent = async (filename) => {
    try {
      const response = await axios.get(`http://localhost:3001/file/${filename}`);
      setFileContent(response.data.content);
      setSelectedFile(filename);
    } catch (error) {
      console.error('Error fetching file content:', error);
    }
  };

  return (
    <div className="App">
      <h1>My Leetcode Answers</h1>
      <h2>Amount of answers: {files.length}</h2>
      <div className="container">
        <div className="file-list">
          <h3>Files</h3>
          <ul>
            {files.map((file) => (
              <li key={file} onClick={() => fetchFileContent(file)}>
                {file}
              </li>
            ))}
          </ul>
        </div>
        <div className="file-content">
          <h3>{selectedFile || 'Select a file'}</h3>
          <pre>{fileContent}</pre>
        </div>
      </div>
    </div>
  );
}

export default App;
