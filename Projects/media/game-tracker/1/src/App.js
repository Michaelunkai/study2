import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import GameList from './components/GameList';
import GameDetails from './components/GameDetails';
import AddEditGame from './components/AddEditGame';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Game Tracker</h1>
        </header>
        <Routes>
          <Route path="/" element={<GameList />} />
          <Route path="/game/:id" element={<GameDetails />} />
          <Route path="/add" element={<AddEditGame />} />
          <Route path="/edit/:id" element={<AddEditGame />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
