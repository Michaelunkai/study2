
import React, { useState, useEffect } from "react";
import { useGameContext } from "@/context/GameContext";
import GameCard from "@/components/GameCard";
import Navbar from "@/components/Navbar";
import { Button } from "@/components/ui/button";
import { SlidersHorizontal, Gamepad2, Search, X } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";

const Index = () => {
  const { recommendedGames } = useGameContext();
  const [searchTerm, setSearchTerm] = useState("");
  const [activeGenres, setActiveGenres] = useState<string[]>([]);
  const [showFilters, setShowFilters] = useState(false);
  const [displayCount, setDisplayCount] = useState(12);
  
  // Get unique genres across all games
  const allGenres = Array.from(
    new Set(
      recommendedGames.flatMap(game => game.genre)
    )
  ).sort();

  // Filter games based on search term and active genres
  const filteredGames = recommendedGames.filter(game => {
    const matchesSearch = searchTerm === "" || 
      game.title.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesGenre = activeGenres.length === 0 || 
      game.genre.some(genre => activeGenres.includes(genre));
    
    return matchesSearch && matchesGenre;
  });

  // Reset filters when returning to the page
  useEffect(() => {
    return () => {
      setSearchTerm("");
      setActiveGenres([]);
      setDisplayCount(12);
    };
  }, []);

  // Toggle genre filter
  const toggleGenre = (genre: string) => {
    setActiveGenres(prev => 
      prev.includes(genre) 
        ? prev.filter(g => g !== genre) 
        : [...prev, genre]
    );
  };

  // Load more games
  const loadMore = () => {
    setDisplayCount(prev => Math.min(prev + 12, filteredGames.length));
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="container mx-auto py-8 px-4 max-w-7xl">
        <div className="bg-gradient-to-br from-purple-900/30 to-indigo-900/30 rounded-2xl p-8 mb-8 shadow-xl backdrop-blur-sm border border-purple-800/20">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <h1 className="text-4xl font-bold flex items-center gap-3 text-white">
                <Gamepad2 className="h-10 w-10 text-primary" />
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-indigo-300">
                  Game Explorer
                </span>
              </h1>
              <p className="text-muted-foreground mt-2 text-lg">
                Discover new games that match your interests
              </p>
            </div>
            
            <div className="w-full md:w-auto relative">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search games..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full md:w-[300px] pl-10 pr-10 py-6 bg-background/80 backdrop-blur-sm border-purple-800/30 focus-visible:ring-purple-500"
                />
                {searchTerm && (
                  <Button 
                    variant="ghost" 
                    size="icon" 
                    className="absolute right-2 top-1/2 transform -translate-y-1/2 h-6 w-6 text-muted-foreground hover:text-foreground"
                    onClick={() => setSearchTerm("")}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                )}
              </div>
            </div>
          </div>
          
          <div className="mt-6 flex gap-2 flex-wrap">
            <Button 
              variant={showFilters ? "default" : "outline"} 
              onClick={() => setShowFilters(!showFilters)}
              className="gap-2"
            >
              <SlidersHorizontal className="h-4 w-4" />
              Filters {activeGenres.length > 0 && `(${activeGenres.length})`}
            </Button>
            
            {activeGenres.length > 0 && (
              <Button
                variant="outline"
                className="gap-2 border-destructive/30 text-destructive hover:bg-destructive/10"
                onClick={() => setActiveGenres([])}
              >
                <X className="h-4 w-4" />
                Clear Filters
              </Button>
            )}
            
            {activeGenres.map(genre => (
              <Badge 
                key={genre} 
                className="px-3 py-1.5 cursor-pointer bg-primary/20 hover:bg-primary/30 text-primary-foreground"
                onClick={() => toggleGenre(genre)}
              >
                {genre} <X className="h-3 w-3 ml-1" />
              </Badge>
            ))}
          </div>
        </div>
        
        {showFilters && (
          <div className="mb-8 bg-card rounded-xl shadow-lg border p-4 animate-fade-in">
            <h2 className="font-semibold mb-3 text-lg">Genre Filters</h2>
            <ScrollArea className="h-[200px]">
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2 p-1">
                {allGenres.map(genre => (
                  <Badge
                    key={genre}
                    variant={activeGenres.includes(genre) ? "default" : "outline"}
                    className="cursor-pointer py-1.5 justify-center"
                    onClick={() => toggleGenre(genre)}
                  >
                    {genre}
                  </Badge>
                ))}
              </div>
            </ScrollArea>
          </div>
        )}
        
        {/* Game Grid */}
        <div>
          {filteredGames.length > 0 ? (
            <>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {filteredGames.slice(0, displayCount).map(game => (
                  <div key={game.id} className="animate-fade-in">
                    <GameCard game={game} />
                  </div>
                ))}
              </div>
              
              {displayCount < filteredGames.length && (
                <div className="mt-10 text-center">
                  <Button 
                    size="lg" 
                    onClick={loadMore}
                    className="px-8 py-6 text-lg"
                  >
                    Load More Games
                  </Button>
                  <p className="text-muted-foreground mt-2">
                    Showing {displayCount} of {filteredGames.length} games
                  </p>
                </div>
              )}
            </>
          ) : (
            <div className="text-center py-20 bg-card rounded-lg border">
              <h2 className="text-2xl font-semibold mb-2">No games found</h2>
              <p className="text-muted-foreground">
                Try adjusting your filters or search term
              </p>
              <Button
                variant="default"
                onClick={() => {
                  setSearchTerm("");
                  setActiveGenres([]);
                }}
                className="mt-6"
              >
                Clear all filters
              </Button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Index;
