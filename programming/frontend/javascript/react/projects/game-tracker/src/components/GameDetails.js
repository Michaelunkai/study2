import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function GameDetails() {
  const { id } = useParams();
  const [game, setGame] = useState(null);

  useEffect(() => {
    const storedGames = localStorage.getItem('games');
    const gameData = storedGames ? JSON.parse(storedGames).find((g) => g.id === id) : null;
    setGame(gameData);
  }, [id]);

  if (!game) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>{game.title}</h2>
      <p>Platform: {game.platform}</p>
      <p>Rating: {game.rating}</p>
      <p>Review: {game.review}</p>
      <p>Completed: {game.completed ? 'Yes' : 'No'}</p>
      <Link to={`/edit/${game.id}`}>Edit Game</Link>
    </div>
  );
}

export default GameDetails;
