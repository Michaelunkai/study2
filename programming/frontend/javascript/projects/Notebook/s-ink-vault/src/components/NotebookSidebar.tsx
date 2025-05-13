
import React, { useState } from 'react';
import { 
  Sidebar, 
  SidebarContent,
  SidebarHeader,
  SidebarFooter,
} from '@/components/ui/sidebar';
import { Button } from '@/components/ui/button';
import { PlusCircle, Folder, Save } from 'lucide-react';
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import { useNotebook, Tab } from '@/context/NotebookContext';

export function NotebookSidebar() {
  const { 
    tabs, 
    activeTabId, 
    setActiveTabId, 
    createTab, 
    deleteTab,
    updateTabName,
    createNote,
    getNotesByTabId
  } = useNotebook();
  
  const [newTabName, setNewTabName] = useState('');
  const [editingTab, setEditingTab] = useState<Tab | null>(null);
  
  const handleCreateTab = () => {
    if (newTabName.trim()) {
      createTab(newTabName.trim());
      setNewTabName('');
    }
  };

  const handleUpdateTabName = () => {
    if (editingTab && newTabName.trim()) {
      updateTabName(editingTab.id, newTabName.trim());
      setEditingTab(null);
      setNewTabName('');
    }
  };

  const startEditingTab = (tab: Tab) => {
    setEditingTab(tab);
    setNewTabName(tab.name);
  };
  
  const handleCreateNote = () => {
    if (activeTabId) {
      createNote(activeTabId);
    }
  };

  return (
    <Sidebar className="border-r border-white/10">
      <SidebarHeader className="p-4 flex flex-col">
        <h1 className="font-bold text-xl text-center text-gradient bg-clip-text bg-gradient-to-r from-blue-400 to-primary">
          Micha Fedro's Notebook
        </h1>
      </SidebarHeader>
      
      <SidebarContent>
        <div className="px-3 py-2">
          <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight">Tabs</h2>
          <div className="space-y-1">
            <Button
              variant="outline" 
              className="w-full justify-start gap-2" 
              onClick={handleCreateNote}
            >
              <PlusCircle className="h-4 w-4" />
              New Note
            </Button>
          </div>
          
          <ScrollArea className="h-[calc(100vh-250px)] py-2 pr-2">
            <div className="space-y-1">
              {tabs.map(tab => (
                <div key={tab.id} className="flex items-center group">
                  <Button
                    variant={activeTabId === tab.id ? "secondary" : "ghost"}
                    className={cn(
                      "w-full justify-start text-left",
                      activeTabId === tab.id && "bg-notebook-accent bg-opacity-20"
                    )}
                    onClick={() => setActiveTabId(tab.id)}
                  >
                    <Folder className="mr-2 h-4 w-4" />
                    <span className="flex-grow truncate">{tab.name}</span>
                    <span className="ml-auto opacity-60 text-xs">
                      {getNotesByTabId(tab.id).length}
                    </span>
                  </Button>

                  <div className="opacity-0 group-hover:opacity-100 flex">
                    <Button 
                      variant="ghost" 
                      size="icon" 
                      className="h-8 w-8" 
                      onClick={() => startEditingTab(tab)}
                    >
                      <span className="sr-only">Edit</span>
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"></path></svg>
                    </Button>
                    
                    <Button 
                      variant="ghost" 
                      size="icon" 
                      className="h-8 w-8 text-destructive" 
                      onClick={() => deleteTab(tab.id)}
                    >
                      <span className="sr-only">Delete</span>
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"></path><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path></svg>
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </ScrollArea>
        </div>
      </SidebarContent>
      
      <SidebarFooter className="border-t border-white/10 p-4">
        <Dialog>
          <DialogTrigger asChild>
            <Button className="w-full gap-2">
              <PlusCircle className="h-4 w-4" />
              New Tab
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>{editingTab ? 'Edit Tab' : 'Create New Tab'}</DialogTitle>
              <DialogDescription>
                {editingTab 
                  ? 'Enter a new name for this tab.' 
                  : 'Add a new tab to organize your notes.'}
              </DialogDescription>
            </DialogHeader>
            <div className="py-4">
              <Label htmlFor="tab-name">Tab Name</Label>
              <Input 
                id="tab-name" 
                value={newTabName} 
                onChange={(e) => setNewTabName(e.target.value)}
                placeholder="Enter tab name"
                className="mt-2"
                autoFocus
              />
            </div>
            <DialogFooter>
              <Button onClick={editingTab ? handleUpdateTabName : handleCreateTab}>
                <Save className="h-4 w-4 mr-2" />
                {editingTab ? 'Update Tab' : 'Create Tab'}
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </SidebarFooter>
    </Sidebar>
  );
}
