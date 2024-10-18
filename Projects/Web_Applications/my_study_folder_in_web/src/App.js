import React, { useState, useEffect } from 'react';
import './App.css';

function FileExplorer() {
  const [currentPath, setCurrentPath] = useState('');
  const [contents, setContents] = useState([]);
  const [fileContent, setFileContent] = useState('');
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:3001');
    setWs(websocket);

    websocket.onopen = () => {
      console.log('WebSocket connected');
      websocket.send(JSON.stringify({ type: 'getContents', path: currentPath }));
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'contents') {
        setContents(data.data);
      } else if (data.type === 'file') {
        setFileContent(data.data);
      }
    };

    return () => {
      websocket.close();
    };
  }, []);

  useEffect(() => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'getContents', path: currentPath }));
    }
  }, [currentPath, ws]);

  const handleItemClick = (item) => {
    if (item.isDirectory) {
      setCurrentPath(item.path);
      setFileContent('');
    } else {
      ws.send(JSON.stringify({ type: 'getFile', path: item.path }));
    }
  };

  const goBack = () => {
    setCurrentPath(currentPath.split('/').slice(0, -1).join('/'));
    setFileContent('');
  };

  return (
    <div className="file-explorer">
      <h1>My Study Folder</h1>
      <div className="content">
        <div className="file-list">
          {currentPath && <div className="file-item back" onClick={goBack}>📁 ..</div>}
          {contents.map((item, index) => (
            <div key={index} className={`file-item ${item.isDirectory ? 'folder' : 'file'}`} onClick={() => handleItemClick(item)}>
              {item.isDirectory ? '📁' : '📄'} <span className="item-name">{item.name}</span>
            </div>
          ))}
        </div>
        {fileContent && (
          <div className="file-content">
            <h2>File Content</h2>
            <pre>{fileContent}</pre>
          </div>
        )}
      </div>
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <FileExplorer />
    </div>
  );
}

export default App;
