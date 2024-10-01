import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

function AddEditGame() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [game, setGame] = useState({
    title: '',
    platform: '',
    rating: 0,
    review: '',
    completed: false,
  });

  useEffect(() => {
    if (id) {
      const storedGames = localStorage.getItem('games');
      const gameData = storedGames ? JSON.parse(storedGames).find((g) => g.id === id) : null;
      setGame(gameData || game);
    }
  }, [id, game]);

  const handleChange = (e) => {
    setGame({ ...game, [e.target.name]: e.target.value });
  };

  const handleCheckboxChange = (e) => {
    setGame({ ...game, completed: e.target.checked });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const storedGames = localStorage.getItem('games');
    const games = storedGames ? JSON.parse(storedGames) : [];
    const updatedGames = id
      ? games.map((g) => (g.id === id ? game : g))
      : [...games, { ...game, id: Date.now() }];
    localStorage.setItem('games', JSON.stringify(updatedGames));
    navigate('/');
  };

  return (
    <div>
      <h2>{id ? 'Edit Game' : 'Add New Game'}</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Title:
          <input type="text" name="title" value={game.title} onChange={handleChange} />
        </label>
        <label>
          Platform:
          <input type="text" name="platform" value={game.platform} onChange={handleChange} />
        </label>
        <label>
          Rating:
          <input type="number" name="rating" value={game.rating} onChange={handleChange} />
        </label>
        <label>
          Review:
          <textarea name="review" value={game.review} onChange={handleChange} />
        </label>
        <label>
          Completed:
          <input type="checkbox" name="completed" checked={game.completed} onChange={handleCheckboxChange} />
        </label>
        <button type="submit">{id ? 'Update' : 'Add'}</button>
      </form>
    </div>
  );
}

export default AddEditGame;
