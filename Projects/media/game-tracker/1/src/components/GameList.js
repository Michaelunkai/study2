import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function GameList() {
  const [games, setGames] = useState([]);

  useEffect(() => {
    const storedGames = localStorage.getItem('games');
    setGames(storedGames ? JSON.parse(storedGames) : []);
  }, []);

  return (
    <div>
      <h2>Game List</h2>
      <ul>
        {games.map((game) => (
          <li key={game.id}>
            <Link to={`/game/${game.id}`}>
              {game.title} ({game.platform})
            </Link>
          </li>
        ))}
      </ul>
      <Link to="/add">Add New Game</Link>
    </div>
  );
}

export default GameList;
