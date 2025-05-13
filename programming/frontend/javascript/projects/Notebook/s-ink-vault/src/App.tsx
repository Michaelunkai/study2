
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { NotebookProvider } from "@/context/NotebookContext";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import { Suspense, lazy } from "react";

// Create a new query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      refetchOnWindowFocus: true,
    },
  },
});

const App = () => (
  <QueryClientProvider client={queryClient}>
    <NotebookProvider>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Suspense fallback={
            <div className="flex h-screen w-full items-center justify-center bg-notebook-dark">
              <div className="text-center">
                <h2 className="text-2xl font-bold text-white mb-2">Loading Micha Fedro's Notebook</h2>
                <p className="text-blue-300">Syncing your notes...</p>
              </div>
            </div>
          }>
            <Routes>
              <Route path="/" element={<Index />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </Suspense>
        </BrowserRouter>
      </TooltipProvider>
    </NotebookProvider>
  </QueryClientProvider>
);

export default App;
