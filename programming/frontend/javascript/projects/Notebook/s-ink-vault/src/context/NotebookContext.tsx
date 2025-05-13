
import React, { createContext, useState, useContext, useEffect } from 'react';
import { toast } from 'sonner';

// Define types for our data structures
export type Note = {
  id: string;
  title: string;
  content: string;
  tabId: string;
  createdAt: string;
  updatedAt: string;
};

export type Tab = {
  id: string;
  name: string;
  createdAt: string;
};

interface NotebookContextType {
  notes: Note[];
  tabs: Tab[];
  activeTabId: string;
  activeNoteId: string | null;
  setActiveTabId: (id: string) => void;
  setActiveNoteId: (id: string | null) => void;
  createTab: (name: string) => void;
  updateTabName: (id: string, name: string) => void;
  deleteTab: (id: string) => void;
  createNote: (tabId: string, title?: string) => string;
  updateNote: (id: string, data: Partial<Note>) => void;
  deleteNote: (id: string) => void;
  getNotesByTabId: (tabId: string) => Note[];
  getActiveNote: () => Note | null;
}

const NotebookContext = createContext<NotebookContextType | undefined>(undefined);

// Key constants for localStorage
const STORAGE_KEYS = {
  TABS: 'notebook-tabs',
  NOTES: 'notebook-notes',
  ACTIVE_TAB: 'notebook-active-tab-id',
  ACTIVE_NOTE: 'notebook-active-note-id',
  LAST_SYNC: 'notebook-last-sync'
};

export function NotebookProvider({ children }: { children: React.ReactNode }) {
  const [notes, setNotes] = useState<Note[]>([]);
  const [tabs, setTabs] = useState<Tab[]>([]);
  const [activeTabId, setActiveTabId] = useState<string>('');
  const [activeNoteId, setActiveNoteId] = useState<string | null>(null);
  const [lastSyncTime, setLastSyncTime] = useState<number>(0);
  const [isInitialLoad, setIsInitialLoad] = useState(true);
  
  // Initialize with a default tab if none exists and load data
  useEffect(() => {
    const loadData = () => {
      try {
        // Load tabs from localStorage
        const savedTabs = localStorage.getItem(STORAGE_KEYS.TABS);
        const parsedTabs = savedTabs ? JSON.parse(savedTabs) as Tab[] : [];
        
        // Load notes from localStorage
        const savedNotes = localStorage.getItem(STORAGE_KEYS.NOTES);
        const parsedNotes = savedNotes ? JSON.parse(savedNotes) as Note[] : [];
        
        // If no tabs, create a default one
        if (parsedTabs.length === 0) {
          const defaultTab: Tab = {
            id: 'tab-' + Date.now(),
            name: 'General',
            createdAt: new Date().toISOString(),
          };
          parsedTabs.push(defaultTab);
        }
        
        // Get active tab from localStorage or use the first tab
        const savedActiveTabId = localStorage.getItem(STORAGE_KEYS.ACTIVE_TAB);
        const initialActiveTabId = savedActiveTabId || parsedTabs[0].id;
        
        // Get active note from localStorage
        const savedActiveNoteId = localStorage.getItem(STORAGE_KEYS.ACTIVE_NOTE);
        
        // Get last sync time
        const savedLastSyncTime = localStorage.getItem(STORAGE_KEYS.LAST_SYNC);
        const parsedLastSyncTime = savedLastSyncTime ? parseInt(savedLastSyncTime) : 0;
        
        // Set state
        setTabs(parsedTabs);
        setNotes(parsedNotes);
        setActiveTabId(initialActiveTabId);
        setActiveNoteId(savedActiveNoteId);
        setLastSyncTime(parsedLastSyncTime);
        
        const noteCount = parsedNotes.length;
        const tabCount = parsedTabs.length;
        
        toast.success('Notes loaded successfully', {
          description: `${noteCount} notes in ${tabCount} tabs`,
          duration: 2000,
        });
        
        setIsInitialLoad(false);
      } catch (error) {
        console.error('Error loading notebook data:', error);
        toast.error('Failed to load your notes');
        setIsInitialLoad(false);
      }
    };
    
    loadData();
    
    // Set up more frequent check for updates from other browser instances
    const syncInterval = setInterval(checkForExternalChanges, 3000); // Changed from 5000ms to 3000ms
    
    // Set up storage event listener to detect changes from other tabs/windows
    window.addEventListener('storage', handleStorageChange);
    
    return () => {
      clearInterval(syncInterval);
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);
  
  // Check for external changes (from other browsers/tabs)
  const checkForExternalChanges = () => {
    try {
      // Check last sync time
      const externalLastSyncTime = localStorage.getItem(STORAGE_KEYS.LAST_SYNC);
      const parsedExternalLastSyncTime = externalLastSyncTime ? parseInt(externalLastSyncTime) : 0;
      
      // If external changes are newer than our last sync, reload data
      if (parsedExternalLastSyncTime > lastSyncTime) {
        const savedTabs = localStorage.getItem(STORAGE_KEYS.TABS);
        const savedNotes = localStorage.getItem(STORAGE_KEYS.NOTES);
        
        if (savedTabs) {
          setTabs(JSON.parse(savedTabs));
        }
        
        if (savedNotes) {
          setNotes(JSON.parse(savedNotes));
        }
        
        setLastSyncTime(parsedExternalLastSyncTime);
        
        // If we're using a note that's been updated externally, we need to refresh our view of it
        if (activeNoteId) {
          const parsedNotes = savedNotes ? JSON.parse(savedNotes) as Note[] : [];
          const activeNote = parsedNotes.find(note => note.id === activeNoteId);
          
          // If the active note has been updated externally, inform the user
          if (activeNote && getActiveNote() && 
              activeNote.updatedAt > getActiveNote()!.updatedAt) {
            toast.info('Note updated externally', {
              description: 'This note was updated from another device',
              duration: 3000,
            });
          }
        }
        
        toast.info('Notes synchronized', {
          description: 'Latest changes from other devices loaded',
          duration: 2000,
        });
      }
    } catch (error) {
      console.error('Error checking for external changes:', error);
    }
  };
  
  // Handle storage events (triggered when another tab/window changes localStorage)
  const handleStorageChange = (event: StorageEvent) => {
    if (event.key === STORAGE_KEYS.TABS) {
      const newTabs = event.newValue ? JSON.parse(event.newValue) as Tab[] : [];
      setTabs(newTabs);
    } else if (event.key === STORAGE_KEYS.NOTES) {
      const newNotes = event.newValue ? JSON.parse(event.newValue) as Note[] : [];
      setNotes(newNotes);
    } else if (event.key === STORAGE_KEYS.LAST_SYNC) {
      const newLastSyncTime = event.newValue ? parseInt(event.newValue) : 0;
      setLastSyncTime(newLastSyncTime);
    }
  };
  
  // Save to localStorage whenever data changes
  useEffect(() => {
    // Skip during initial load to prevent duplicate saves
    if (isInitialLoad) return;
    
    if (tabs.length > 0) {
      localStorage.setItem(STORAGE_KEYS.TABS, JSON.stringify(tabs));
    }
    if (notes.length > 0 || tabs.length > 0) {
      localStorage.setItem(STORAGE_KEYS.NOTES, JSON.stringify(notes));
    }
    if (activeTabId) {
      localStorage.setItem(STORAGE_KEYS.ACTIVE_TAB, activeTabId);
    }
    if (activeNoteId) {
      localStorage.setItem(STORAGE_KEYS.ACTIVE_NOTE, activeNoteId);
    } else {
      localStorage.removeItem(STORAGE_KEYS.ACTIVE_NOTE);
    }
    
    // Update last sync time
    const currentTime = Date.now();
    localStorage.setItem(STORAGE_KEYS.LAST_SYNC, currentTime.toString());
    setLastSyncTime(currentTime);
  }, [tabs, notes, activeTabId, activeNoteId, isInitialLoad]);
  
  // Tab operations
  const createTab = (name: string) => {
    const newTab: Tab = {
      id: 'tab-' + Date.now(),
      name,
      createdAt: new Date().toISOString(),
    };
    setTabs([...tabs, newTab]);
    setActiveTabId(newTab.id);
    toast.success(`Tab "${name}" created`);
  };
  
  const updateTabName = (id: string, name: string) => {
    setTabs(tabs.map(tab => tab.id === id ? { ...tab, name } : tab));
    toast.success(`Tab renamed to "${name}"`);
  };
  
  const deleteTab = (id: string) => {
    // If we're deleting the active tab, set a different active tab
    if (activeTabId === id) {
      const otherTab = tabs.find(t => t.id !== id);
      if (otherTab) {
        setActiveTabId(otherTab.id);
      }
    }
    
    // Delete the tab and associated notes
    setTabs(tabs.filter(tab => tab.id !== id));
    setNotes(notes.filter(note => note.tabId !== id));
    
    toast.success('Tab deleted');
  };
  
  // Note operations
  const createNote = (tabId: string, title = 'New Note') => {
    const id = 'note-' + Date.now();
    const newNote: Note = {
      id,
      title,
      content: '',
      tabId,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    setNotes([...notes, newNote]);
    setActiveNoteId(id);
    toast.success('New note created');
    return id;
  };
  
  const updateNote = (id: string, data: Partial<Note>) => {
    setNotes(notes.map(note => {
      if (note.id === id) {
        return {
          ...note,
          ...data,
          updatedAt: new Date().toISOString(),
        };
      }
      return note;
    }));
  };
  
  const deleteNote = (id: string) => {
    // If we're deleting the active note, clear the active note
    if (activeNoteId === id) {
      setActiveNoteId(null);
    }
    
    // Delete the note
    setNotes(notes.filter(note => note.id !== id));
    toast.success('Note deleted');
  };
  
  // Helper functions
  const getNotesByTabId = (tabId: string) => {
    return notes.filter(note => note.tabId === tabId);
  };
  
  const getActiveNote = () => {
    return activeNoteId ? notes.find(note => note.id === activeNoteId) || null : null;
  };
  
  const value = {
    notes,
    tabs,
    activeTabId,
    activeNoteId,
    setActiveTabId,
    setActiveNoteId,
    createTab,
    updateTabName,
    deleteTab,
    createNote,
    updateNote,
    deleteNote,
    getNotesByTabId,
    getActiveNote,
  };
  
  return (
    <NotebookContext.Provider value={value}>
      {children}
    </NotebookContext.Provider>
  );
}

export function useNotebook() {
  const context = useContext(NotebookContext);
  if (context === undefined) {
    throw new Error('useNotebook must be used within a NotebookProvider');
  }
  return context;
}
