
import React from "react";
import { GameList } from "@/context/GameContext";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  Star,
  Clock,
  ThumbsDown,
  CheckCheck,
  MoreHorizontal,
  Trash2
} from "lucide-react";
import { 
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { useGameContext } from "@/context/GameContext";
import { useNavigate } from "react-router-dom";

interface ListCardProps {
  list: GameList;
}

const ListCard: React.FC<ListCardProps> = ({ list }) => {
  const { deleteList } = useGameContext();
  const navigate = useNavigate();

  const getListIcon = () => {
    switch (list.id) {
      case "favorites":
        return <Star className="h-5 w-5 text-yellow-500" />;
      case "backlog":
        return <Clock className="h-5 w-5 text-blue-500" />;
      case "meh":
        return <ThumbsDown className="h-5 w-5 text-gray-500" />;
      case "played":
        return <CheckCheck className="h-5 w-5 text-green-500" />;
      default:
        return null;
    }
  };

  const handleViewList = () => {
    navigate(`/list/${list.id}`);
  };

  return (
    <Card className="overflow-hidden transition-all hover:shadow-lg flex flex-col h-full">
      <CardHeader className="p-4 pb-2 flex flex-row items-center justify-between">
        <div className="flex items-center gap-2">
          {getListIcon()}
          <CardTitle className="text-lg">{list.name}</CardTitle>
        </div>
        {!list.isDefault && (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem 
                onClick={() => deleteList(list.id)}
                className="text-destructive cursor-pointer"
              >
                <Trash2 className="mr-2 h-4 w-4" />
                Delete List
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )}
      </CardHeader>
      <CardContent className="p-4 pt-0 pb-2 flex-grow">
        <Badge variant="secondary" className="mt-2">
          {list.games.length} {list.games.length === 1 ? "game" : "games"}
        </Badge>
        
        <div className="mt-3 grid grid-cols-3 gap-2">
          {list.games.slice(0, 3).map((game) => (
            <div key={game.id} className="aspect-square overflow-hidden rounded-md bg-secondary">
              <img 
                src={game.image} 
                alt={game.title} 
                className="w-full h-full object-cover"
              />
            </div>
          ))}
          {list.games.length === 0 && (
            <div className="col-span-3 py-4 text-sm text-muted-foreground text-center">
              No games added yet
            </div>
          )}
        </div>
      </CardContent>
      <CardFooter className="p-4 pt-2">
        <Button 
          variant="outline" 
          className="w-full"
          onClick={handleViewList}
        >
          View List
        </Button>
      </CardFooter>
    </Card>
  );
};

export default ListCard;
