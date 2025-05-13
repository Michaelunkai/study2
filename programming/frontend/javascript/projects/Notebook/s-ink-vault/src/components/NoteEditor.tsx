
import React, { useEffect, useState, useCallback } from 'react';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { useNotebook } from '@/context/NotebookContext';
import { Mic, MicOff, Save } from 'lucide-react';
import { toast } from 'sonner';

export function NoteEditor() {
  const { activeNoteId, getActiveNote, updateNote } = useNotebook();
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [recognition, setRecognition] = useState<SpeechRecognition | null>(null);
  const [interimTranscript, setInterimTranscript] = useState('');
  
  const activeNote = getActiveNote();
  
  // Initialize title and content when active note changes
  useEffect(() => {
    if (activeNote) {
      setTitle(activeNote.title);
      setContent(activeNote.content);
    } else {
      setTitle('');
      setContent('');
    }
  }, [activeNote]);
  
  // Enhanced auto-save functionality with debounce
  useEffect(() => {
    if (activeNoteId && (title !== activeNote?.title || content !== activeNote?.content)) {
      const timer = setTimeout(() => {
        updateNote(activeNoteId, { title, content });
        // Simple visual indicator that auto-save occurred
        const saveIndicator = document.getElementById('auto-save-indicator');
        if (saveIndicator) {
          saveIndicator.classList.add('opacity-100');
          setTimeout(() => saveIndicator.classList.remove('opacity-100'), 1000);
        }
      }, 300); // Decreased from 500ms to 300ms for quicker syncing
      
      return () => clearTimeout(timer);
    }
  }, [title, content, activeNoteId, activeNote, updateNote]);
  
  // Improved speech recognition setup
  const setupSpeechRecognition = useCallback(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      
      if (SpeechRecognition) {
        const recognitionInstance = new SpeechRecognition();
        
        recognitionInstance.continuous = true;
        recognitionInstance.interimResults = true;
        recognitionInstance.lang = navigator.language || 'en-US'; // Use browser language
        recognitionInstance.maxAlternatives = 3; // Get multiple alternatives for better accuracy
        
        recognitionInstance.onresult = (event: SpeechRecognitionEvent) => {
          let finalTranscript = '';
          let currentInterimTranscript = '';
          
          for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            
            if (event.results[i].isFinal) {
              finalTranscript += transcript + ' ';
              
              // Apply smart punctuation to final transcript
              const smartTranscript = applySmartPunctuation(finalTranscript);
              setContent(prev => {
                // Only add space if content doesn't end with one
                const spacer = prev.endsWith(' ') ? '' : ' ';
                return prev + spacer + smartTranscript;
              });
            } else {
              currentInterimTranscript += transcript;
            }
          }
          
          setInterimTranscript(currentInterimTranscript);
        };
        
        recognitionInstance.onerror = (event: SpeechRecognitionErrorEvent) => {
          console.error('Speech recognition error', event.error);
          toast.error('Speech recognition error', {
            description: event.message || event.error,
          });
          setIsRecording(false);
        };
        
        recognitionInstance.onend = () => {
          setIsRecording(false);
          setInterimTranscript('');
        };
        
        setRecognition(recognitionInstance);
      }
    }
  }, []);
  
  // Apply smart punctuation to improve transcription quality
  const applySmartPunctuation = (text: string) => {
    if (!text) return '';
    
    // Capitalize first letter of sentences
    let processed = text.replace(/(^\s*\w|[.!?]\s*\w)/g, match => match.toUpperCase());
    
    // Add periods at the end of sentences if missing
    if (!processed.match(/[.!?]$/)) {
      processed = processed.trim() + '.';
    }
    
    // Fix common speech recognition errors
    processed = processed
      .replace(/\bi\b/g, 'I') // Capitalize "I"
      .replace(/\s{2,}/g, ' ') // Remove extra spaces
      .replace(/\s([,.!?:;])/g, '$1') // Remove spaces before punctuation
      .replace(/(\d+)(st|nd|rd|th)\b/g, '$1$2'); // Fix ordinals
      
    return processed;
  };
  
  // Set up speech recognition
  useEffect(() => {
    setupSpeechRecognition();
    
    return () => {
      if (recognition) {
        try {
          recognition.stop();
        } catch (error) {
          console.error('Error stopping recognition:', error);
        }
      }
    };
  }, [setupSpeechRecognition]);
  
  const toggleSpeechRecognition = () => {
    if (!recognition) {
      setupSpeechRecognition();
      toast.error('Speech recognition not supported by your browser');
      return;
    }
    
    if (isRecording) {
      recognition.stop();
      setIsRecording(false);
      setInterimTranscript('');
      toast.success('Voice recording stopped');
    } else {
      recognition.start();
      setIsRecording(true);
      toast.success('Voice recording started', {
        description: 'Speak clearly into your microphone',
      });
    }
  };
  
  if (!activeNote) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center p-4">
        <h3 className="text-xl font-medium mb-2">No note selected</h3>
        <p className="text-muted-foreground">
          Select a note from the list or create a new one
        </p>
      </div>
    );
  }
  
  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between p-4 border-b border-white/10">
        <Input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Note title"
          className="text-xl font-semibold bg-transparent border-none shadow-none focus-visible:ring-0 p-0 h-auto"
        />
        <div className="flex items-center gap-2">
          <div id="auto-save-indicator" className="text-xs text-muted-foreground opacity-0 transition-opacity duration-300">
            Auto-saved
          </div>
          <Button
            variant={isRecording ? "destructive" : "outline"}
            size="icon"
            onClick={toggleSpeechRecognition}
            title={isRecording ? "Stop recording" : "Start voice recording"}
          >
            {isRecording ? (
              <MicOff className="h-4 w-4" />
            ) : (
              <Mic className="h-4 w-4" />
            )}
          </Button>
          <Button
            onClick={() => {
              updateNote(activeNoteId, { title, content });
              toast.success('Note saved successfully');
            }}
            size="sm"
            className="gap-1"
          >
            <Save className="h-4 w-4" />
            Save
          </Button>
        </div>
      </div>
      
      <div className="flex-1 p-4 overflow-hidden">
        <Card 
          className={`h-full note-content p-4 ${isRecording ? 'ring-2 ring-destructive pulse' : ''}`}
        >
          <Textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Start typing your note content here..."
            className="w-full h-full resize-none bg-transparent border-none shadow-none focus-visible:ring-0 p-0 text-lg"
          />
          
          {isRecording && interimTranscript && (
            <div className="absolute bottom-4 left-4 right-4 bg-background/80 backdrop-blur-sm p-3 rounded-md border border-primary/30">
              <p className="text-sm italic text-primary">{interimTranscript}</p>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
