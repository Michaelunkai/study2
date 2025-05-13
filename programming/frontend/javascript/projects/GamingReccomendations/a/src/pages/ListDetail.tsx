
import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useGameContext } from "@/context/GameContext";
import Navbar from "@/components/Navbar";
import { Button } from "@/components/ui/button";
import { 
  ArrowLeft, 
  Trash2, 
  Star, 
  Clock, 
  ThumbsDown, 
  CheckCheck,
  AlertCircle
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const ListDetail = () => {
  const { listId } = useParams<{ listId: string }>();
  const { getListById, removeFromList } = useGameContext();
  const navigate = useNavigate();
  
  const list = getListById(listId || "");
  
  if (!list) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <main className="container mx-auto py-16 px-4 text-center">
          <AlertCircle className="h-16 w-16 mx-auto text-muted-foreground mb-4" />
          <h1 className="text-2xl font-bold mb-2">List Not Found</h1>
          <p className="text-muted-foreground mb-8">
            The list you're looking for doesn't exist or has been deleted.
          </p>
          <Button onClick={() => navigate("/my-lists")}>
            Go to My Lists
          </Button>
        </main>
      </div>
    );
  }
  
  const getListIcon = () => {
    switch (list.id) {
      case "favorites":
        return <Star className="h-6 w-6 text-yellow-500" />;
      case "backlog":
        return <Clock className="h-6 w-6 text-blue-500" />;
      case "meh":
        return <ThumbsDown className="h-6 w-6 text-gray-500" />;
      case "played":
        return <CheckCheck className="h-6 w-6 text-green-500" />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="container mx-auto py-8 px-4">
        <Button 
          variant="ghost" 
          className="mb-4"
          onClick={() => navigate("/my-lists")}
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Lists
        </Button>
        
        <div className="flex items-center gap-3 mb-6">
          {getListIcon()}
          <h1 className="text-3xl font-bold">{list.name}</h1>
          <Badge variant="secondary" className="ml-2">
            {list.games.length} {list.games.length === 1 ? "game" : "games"}
          </Badge>
        </div>
        
        {list.games.length > 0 ? (
          <Card>
            <CardContent className="p-0">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-[80px]">Image</TableHead>
                    <TableHead>Title</TableHead>
                    <TableHead>Genre</TableHead>
                    <TableHead>Year</TableHead>
                    <TableHead>Rating</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {list.games.map((game) => (
                    <TableRow key={game.id}>
                      <TableCell>
                        <div className="h-12 w-20 overflow-hidden rounded">
                          <img 
                            src={game.image} 
                            alt={game.title} 
                            className="h-full w-full object-cover"
                          />
                        </div>
                      </TableCell>
                      <TableCell className="font-medium">{game.title}</TableCell>
                      <TableCell>
                        <div className="flex flex-wrap gap-1">
                          {game.genre.slice(0, 2).map((genre, index) => (
                            <Badge key={index} variant="outline" className="text-xs">
                              {genre}
                            </Badge>
                          ))}
                          {game.genre.length > 2 && (
                            <Badge variant="outline" className="text-xs">
                              +{game.genre.length - 2}
                            </Badge>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>{game.releaseYear}</TableCell>
                      <TableCell>{game.rating.toFixed(1)}</TableCell>
                      <TableCell className="text-right">
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => removeFromList(game.id, list.id)}
                          className="h-8 w-8 text-destructive"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        ) : (
          <div className="text-center py-16 bg-card rounded-lg border">
            <h2 className="text-xl font-semibold mb-2">No games in this list yet</h2>
            <p className="text-muted-foreground mb-6">
              Browse the recommendations to add games to this list
            </p>
            <Button onClick={() => navigate("/")}>
              Discover Games
            </Button>
          </div>
        )}
      </main>
    </div>
  );
};

export default ListDetail;
