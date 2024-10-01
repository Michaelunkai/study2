'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { SaveIcon, TagIcon, XIcon } from 'lucide-react'
import { format } from 'date-fns'

type Thought = {
  id: string;
  content: string;
  tags: string[];
  createdAt: Date;
}

export function EnhancedNotebook() {
  const [thoughts, setThoughts] = useState<Thought[]>([])
  const [currentThought, setCurrentThought] = useState('')
  const [currentTags, setCurrentTags] = useState<string[]>([])
  const [tagInput, setTagInput] = useState('')
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedTag, setSelectedTag] = useState<string | null>(null)

  useEffect(() => {
    const savedThoughts = localStorage.getItem('thoughts')
    if (savedThoughts) {
      setThoughts(JSON.parse(savedThoughts))
    }
  }, [])

  const saveThought = () => {
    if (currentThought.trim()) {
      const newThought: Thought = {
        id: Date.now().toString(),
        content: currentThought,
        tags: currentTags,
        createdAt: new Date(),
      }
      const updatedThoughts = [...thoughts, newThought]
      setThoughts(updatedThoughts)
      localStorage.setItem('thoughts', JSON.stringify(updatedThoughts))
      setCurrentThought('')
      setCurrentTags([])
    }
  }

  const addTag = () => {
    if (tagInput.trim() && !currentTags.includes(tagInput.trim())) {
      setCurrentTags([...currentTags, tagInput.trim()])
      setTagInput('')
    }
  }

  const removeTag = (tagToRemove: string) => {
    setCurrentTags(currentTags.filter(tag => tag !== tagToRemove))
  }

  const filteredThoughts = thoughts.filter(thought => 
    (selectedTag ? thought.tags.includes(selectedTag) : true) &&
    (searchTerm ? thought.content.toLowerCase().includes(searchTerm.toLowerCase()) : true)
  )

  return (
    <div className="flex h-screen bg-gray-100">
      <aside className="w-64 bg-white p-6 shadow-md overflow-hidden flex flex-col">
        <h2 className="text-xl font-semibold mb-4">Saved Thoughts</h2>
        <Input
          type="text"
          placeholder="Search thoughts..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="mb-4"
        />
        <ScrollArea className="flex-grow">
          {filteredThoughts.map(thought => (
            <div key={thought.id} className="mb-4 p-3 bg-gray-50 rounded-lg">
              <p className="text-sm font-medium text-gray-800 mb-1">
                {thought.content.substring(0, 50)}...
              </p>
              <p className="text-xs text-gray-500 mb-1">
                {format(new Date(thought.createdAt), 'MMM d, yyyy HH:mm')}
              </p>
              <div className="flex flex-wrap gap-1">
                {thought.tags.map(tag => (
                  <Badge 
                    key={tag} 
                    variant="secondary" 
                    className="cursor-pointer"
                    onClick={() => setSelectedTag(tag)}
                  >
                    {tag}
                  </Badge>
                ))}
              </div>
            </div>
          ))}
        </ScrollArea>
        {selectedTag && (
          <Button 
            variant="outline" 
            className="mt-4" 
            onClick={() => setSelectedTag(null)}
          >
            Clear Filter
          </Button>
        )}
      </aside>
      <main className="flex-grow p-8">
        <Card className="w-full max-w-4xl mx-auto">
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-center text-gray-800">My Professional Notebook</CardTitle>
          </CardHeader>
          <CardContent>
            <Textarea 
              placeholder="Write your thoughts here..."
              value={currentThought}
              onChange={(e) => setCurrentThought(e.target.value)}
              className="mb-4 h-64 resize-none"
            />
            <div className="flex items-center mb-4">
              <Input
                type="text"
                placeholder="Add tags..."
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addTag()}
                className="mr-2"
              />
              <Button onClick={addTag} size="sm">
                <TagIcon className="h-4 w-4 mr-2" /> Add Tag
              </Button>
            </div>
            <div className="flex flex-wrap gap-2 mb-4">
              {currentTags.map(tag => (
                <Badge key={tag} variant="secondary" className="text-sm">
                  {tag}
                  <XIcon 
                    className="h-3 w-3 ml-1 cursor-pointer" 
                    onClick={() => removeTag(tag)}
                  />
                </Badge>
              ))}
            </div>
            <Button onClick={saveThought} className="w-full">
              <SaveIcon className="mr-2 h-4 w-4" /> Save Thought
            </Button>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}