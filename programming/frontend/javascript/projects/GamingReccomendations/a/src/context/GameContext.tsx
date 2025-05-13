
import React, { createContext, useContext, useState, useEffect } from "react";
import { games } from "@/data/games";

export interface Game {
  id: number;
  title: string;
  image: string;
  genre: string[];
  releaseYear: number;
  description: string;
  rating: number;
  youtubeId?: string; // Add youtubeId as optional property
}

export interface GameList {
  id: string;
  name: string;
  games: Game[];
  isDefault?: boolean;
}

interface GameContextType {
  allGames: Game[];
  recommendedGames: Game[];
  lists: GameList[];
  addToList: (gameId: number, listId: string) => void;
  removeFromList: (gameId: number, listId: string) => void;
  createList: (name: string) => void;
  deleteList: (listId: string) => void;
  getGameById: (id: number) => Game | undefined;
  getListById: (id: string) => GameList | undefined;
  isGameInAnyList: (gameId: number) => boolean;
}

const GameContext = createContext<GameContextType | undefined>(undefined);

export const GameProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Load lists from localStorage on initial render
  const [lists, setLists] = useState<GameList[]>(() => {
    try {
      const savedLists = localStorage.getItem("gameLists");
      if (savedLists) {
        return JSON.parse(savedLists);
      }
    } catch (error) {
      console.error("Error loading lists from localStorage:", error);
    }
    // Default lists
    return [
      { id: "favorites", name: "Favorites", games: [], isDefault: true },
      { id: "meh", name: "Meh", games: [], isDefault: true },
      { id: "backlog", name: "Backlog", games: [], isDefault: true },
      { id: "played", name: "Played", games: [], isDefault: true },
    ];
  });

  // Computed recommended games that are not in any list
  const recommendedGames = games.filter((game) => !lists.some(list => list.games.some(g => g.id === game.id)));

  // Save lists to localStorage whenever they change
  useEffect(() => {
    try {
      localStorage.setItem("gameLists", JSON.stringify(lists));
    } catch (error) {
      console.error("Error saving lists to localStorage:", error);
    }
  }, [lists]);

  const getGameById = (id: number) => {
    return games.find(game => game.id === id);
  };

  const getListById = (id: string) => {
    return lists.find(list => list.id === id);
  };

  const isGameInAnyList = (gameId: number) => {
    return lists.some(list => list.games.some(game => game.id === gameId));
  };

  const addToList = (gameId: number, listId: string) => {
    const game = getGameById(gameId);
    if (!game) return;

    setLists(prevLists => {
      return prevLists.map(list => {
        if (list.id === listId) {
          // Check if game is already in the list
          if (list.games.some(g => g.id === gameId)) {
            return list;
          }
          return {
            ...list,
            games: [...list.games, game],
          };
        }
        return list;
      });
    });
  };

  const removeFromList = (gameId: number, listId: string) => {
    setLists(prevLists => {
      return prevLists.map(list => {
        if (list.id === listId) {
          return {
            ...list,
            games: list.games.filter(game => game.id !== gameId),
          };
        }
        return list;
      });
    });
  };

  const createList = (name: string) => {
    const id = name.toLowerCase().replace(/\s+/g, '-');
    const newList: GameList = {
      id,
      name,
      games: [],
    };
    setLists(prevLists => [...prevLists, newList]);
  };

  const deleteList = (listId: string) => {
    // Don't allow deletion of default lists
    const list = getListById(listId);
    if (list?.isDefault) return;
    
    setLists(prevLists => prevLists.filter(list => list.id !== listId));
  };

  const value = {
    allGames: games,
    recommendedGames,
    lists,
    addToList,
    removeFromList,
    createList,
    deleteList,
    getGameById,
    getListById,
    isGameInAnyList,
  };

  return <GameContext.Provider value={value}>{children}</GameContext.Provider>;
};

export const useGameContext = (): GameContextType => {
  const context = useContext(GameContext);
  if (context === undefined) {
    throw new Error("useGameContext must be used within a GameProvider");
  }
  return context;
};
