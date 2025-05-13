
import React from "react";
import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Gamepad2, ListChecks, Home } from "lucide-react";

const Navbar: React.FC = () => {
  const location = useLocation();
  
  return (
    <div className="border-b">
      <div className="flex h-16 items-center px-4 container mx-auto">
        <div className="flex items-center gap-2 font-bold text-xl text-primary">
          <Gamepad2 className="h-6 w-6" />
          <span>Micha Fedro Gaming Recommendation System</span>
        </div>
        
        <nav className="flex items-center ml-auto gap-4 md:gap-6">
          <Link to="/">
            <Button
              variant={location.pathname === "/" ? "default" : "ghost"}
              className="flex items-center gap-2"
            >
              <Home className="h-4 w-4" />
              <span>Discover</span>
            </Button>
          </Link>
          
          <Link to="/my-lists">
            <Button
              variant={location.pathname === "/my-lists" ? "default" : "ghost"}
              className="flex items-center gap-2"
            >
              <ListChecks className="h-4 w-4" />
              <span>My Lists</span>
            </Button>
          </Link>
        </nav>
      </div>
    </div>
  );
};

export default Navbar;
