
import React, { useState } from "react";
import { useGameContext } from "@/context/GameContext";
import Navbar from "@/components/Navbar";
import ListCard from "@/components/ListCard";
import CreateListModal from "@/components/CreateListModal";
import { Button } from "@/components/ui/button";
import { Plus, ListChecks } from "lucide-react";

const MyLists = () => {
  const { lists } = useGameContext();
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  
  // Split lists into default and custom lists
  const defaultLists = lists.filter(list => list.isDefault);
  const customLists = lists.filter(list => !list.isDefault);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="container mx-auto py-8 px-4">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-2">
              <ListChecks className="h-8 w-8" />
              My Game Lists
            </h1>
            <p className="text-muted-foreground mt-1">
              Manage your custom game collections
            </p>
          </div>
          
          <Button onClick={() => setIsCreateModalOpen(true)}>
            <Plus className="mr-2 h-4 w-4" />
            Create List
          </Button>
        </div>
        
        {/* Default Lists */}
        <h2 className="text-xl font-semibold mb-4">Default Lists</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {defaultLists.map(list => (
            <ListCard key={list.id} list={list} />
          ))}
        </div>
        
        {/* Custom Lists */}
        <div className="mt-8">
          <h2 className="text-xl font-semibold mb-4">Custom Lists</h2>
          {customLists.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {customLists.map(list => (
                <ListCard key={list.id} list={list} />
              ))}
            </div>
          ) : (
            <div className="text-center py-12 bg-card rounded-lg border">
              <h3 className="text-lg font-medium mb-2">No custom lists yet</h3>
              <p className="text-muted-foreground mb-4">
                Create your first custom list to organize your games your way
              </p>
              <Button onClick={() => setIsCreateModalOpen(true)}>
                <Plus className="mr-2 h-4 w-4" />
                Create List
              </Button>
            </div>
          )}
        </div>
      </main>
      
      <CreateListModal 
        isOpen={isCreateModalOpen} 
        onClose={() => setIsCreateModalOpen(false)} 
      />
    </div>
  );
};

export default MyLists;
