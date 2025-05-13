
import React from 'react';
import { NotebookSidebar } from './NotebookSidebar';
import { NotebookNotesList } from './NotebookNotesList';
import { NoteEditor } from './NoteEditor';
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar';
import { useIsMobile } from '@/hooks/use-mobile';
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from '@/components/ui/resizable';

export function NotebookLayout() {
  const isMobile = useIsMobile();
  
  return (
    <SidebarProvider>
      <div className="flex h-screen overflow-hidden w-full">
        <NotebookSidebar />
        
        <main className="flex-1 overflow-hidden">
          <div className="flex items-center h-12 px-4 border-b border-white/10">
            <SidebarTrigger />
            <h2 className="ml-4 text-lg font-semibold">Micha Fedro's Notebook</h2>
          </div>
          
          <div className="h-[calc(100%-3rem)]">
            {isMobile ? (
              <div className="h-full">
                <div className="h-1/2 overflow-hidden">
                  <NotebookNotesList />
                </div>
                <div className="h-1/2 overflow-hidden border-t border-white/10">
                  <NoteEditor />
                </div>
              </div>
            ) : (
              <ResizablePanelGroup direction="horizontal">
                <ResizablePanel 
                  defaultSize={25} 
                  minSize={15}
                  maxSize={40}
                  className="border-r border-white/10"
                >
                  <NotebookNotesList />
                </ResizablePanel>
                <ResizableHandle withHandle />
                <ResizablePanel defaultSize={75}>
                  <NoteEditor />
                </ResizablePanel>
              </ResizablePanelGroup>
            )}
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
}
