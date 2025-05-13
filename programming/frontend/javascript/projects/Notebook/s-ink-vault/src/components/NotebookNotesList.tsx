
import React from 'react';
import { Card } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Button } from '@/components/ui/button';
import { useNotebook } from '@/context/NotebookContext';
import { formatDistanceToNow } from 'date-fns';
import { PlusCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

export function NotebookNotesList() {
  const { 
    activeTabId, 
    activeNoteId, 
    setActiveNoteId, 
    getNotesByTabId, 
    createNote, 
    deleteNote,
    tabs
  } = useNotebook();
  
  const activeTab = tabs.find(tab => tab.id === activeTabId);
  const notes = getNotesByTabId(activeTabId);
  
  const handleCreateNote = () => {
    if (activeTabId) {
      createNote(activeTabId);
    }
  };
  
  if (!activeTab) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center p-4">
        <h3 className="text-lg font-medium mb-2">Select a tab</h3>
        <p className="text-muted-foreground mb-4">Choose a tab to view or create notes</p>
      </div>
    );
  }
  
  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between p-4 border-b border-white/10">
        <h2 className="text-xl font-semibold">
          {activeTab?.name}: Notes ({notes.length})
        </h2>
        <Button onClick={handleCreateNote} size="sm" className="gap-1">
          <PlusCircle className="h-4 w-4" />
          New Note
        </Button>
      </div>
      
      <ScrollArea className="flex-1 px-4 py-2">
        {notes.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-40 text-center">
            <p className="text-muted-foreground mb-4">No notes yet</p>
            <Button onClick={handleCreateNote} variant="outline" className="gap-2">
              <PlusCircle className="h-4 w-4" />
              Create your first note
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-3 pb-4">
            {notes.map(note => (
              <Card 
                key={note.id}
                className={cn(
                  "p-3 cursor-pointer transition-all hover:shadow-lg",
                  activeNoteId === note.id 
                    ? "ring-2 ring-primary bg-notebook-accent bg-opacity-10"
                    : "bg-notebook-paper hover:bg-notebook-paper/90"
                )}
                onClick={() => setActiveNoteId(note.id)}
              >
                <div className="flex justify-between items-start">
                  <h3 className="font-medium text-lg line-clamp-1">{note.title}</h3>
                  <Button 
                    variant="ghost" 
                    size="icon" 
                    className="h-7 w-7 text-destructive opacity-0 hover:opacity-100 focus:opacity-100" 
                    onClick={(e) => {
                      e.stopPropagation();
                      deleteNote(note.id);
                    }}
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"></path><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path></svg>
                    <span className="sr-only">Delete</span>
                  </Button>
                </div>
                <p className="text-sm text-muted-foreground line-clamp-2 mt-1">
                  {note.content.substring(0, 150) || "Empty note"}
                </p>
                <div className="flex justify-between items-center mt-2 text-xs text-muted-foreground">
                  <span>
                    Updated {formatDistanceToNow(new Date(note.updatedAt), { addSuffix: true })}
                  </span>
                </div>
              </Card>
            ))}
          </div>
        )}
      </ScrollArea>
    </div>
  );
}
