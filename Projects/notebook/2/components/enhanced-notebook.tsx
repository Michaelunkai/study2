'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { SaveIcon, TagIcon, XIcon, StarIcon, HashIcon, TrashIcon, PlusCircleIcon } from 'lucide-react'
import { format } from 'date-fns'

type Thought = {
  id: string;
  content: string;
  tags: string[];
  category: string;
  isFavorite: boolean;
  createdAt: Date;
}

export function EnhancedNotebook() {
  const [thoughts, setThoughts] = useState<Thought[]>([])
  const [currentThought, setCurrentThought] = useState('')
  const [currentTags, setCurrentTags] = useState<string[]>([])
  const [currentCategory, setCurrentCategory] = useState('Other')
  const [tagInput, setTagInput] = useState('')
  const [searchTerm, setSearchTerm] = useState('')
  const [searchTags, setSearchTags] = useState<string[]>([])
  const [selectedTag, setSelectedTag] = useState<string | null>(null)
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [showFavorites, setShowFavorites] = useState(false)
  const [categories, setCategories] = useState<string[]>(['Work', 'Personal', 'Ideas', 'To-Do', 'Other'])
  const [newCategory, setNewCategory] = useState('')
  const [isManageCategoriesOpen, setIsManageCategoriesOpen] = useState(false)

  useEffect(() => {
    const savedThoughts = localStorage.getItem('thoughts')
    if (savedThoughts) {
      setThoughts(JSON.parse(savedThoughts))
    }
    const savedCategories = localStorage.getItem('categories')
    if (savedCategories) {
      setCategories(JSON.parse(savedCategories))
    }
  }, [])

  useEffect(() => {
    localStorage.setItem('thoughts', JSON.stringify(thoughts))
  }, [thoughts])

  useEffect(() => {
    localStorage.setItem('categories', JSON.stringify(categories))
  }, [categories])

  const saveThought = () => {
    if (currentThought.trim()) {
      const newThought: Thought = {
        id: Date.now().toString(),
        content: currentThought,
        tags: currentTags,
        category: currentCategory,
        isFavorite: false,
        createdAt: new Date(),
      }
      setThoughts([...thoughts, newThought])
      setCurrentThought('')
      setCurrentTags([])
      setCurrentCategory('Other')
    }
  }

  const deleteThought = (id: string) => {
    setThoughts(thoughts.filter(thought => thought.id !== id))
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

  const toggleFavorite = (id: string) => {
    setThoughts(thoughts.map(thought =>
      thought.id === id ? { ...thought, isFavorite: !thought.isFavorite } : thought
    ))
  }

  const addCategory = () => {
    if (newCategory.trim() && !categories.includes(newCategory.trim())) {
      setCategories([...categories, newCategory.trim()])
      setNewCategory('')
    }
  }

  const removeCategory = (categoryToRemove: string) => {
    if (categoryToRemove !== 'Other') {
      setCategories(categories.filter(category => category !== categoryToRemove))
      setThoughts(thoughts.map(thought => 
        thought.category === categoryToRemove ? { ...thought, category: 'Other' } : thought
      ))
    }
  }

  const addSearchTag = () => {
    if (tagInput.trim() && !searchTags.includes(tagInput.trim())) {
      setSearchTags([...searchTags, tagInput.trim()])
      setTagInput('')
    }
  }

  const removeSearchTag = (tagToRemove: string) => {
    setSearchTags(searchTags.filter(tag => tag !== tagToRemove))
  }

  const filteredThoughts = thoughts.filter(thought => 
    (selectedCategory ? thought.category === selectedCategory : true) &&
    (showFavorites ? thought.isFavorite : true) &&
    (searchTerm ? thought.content.toLowerCase().includes(searchTerm.toLowerCase()) : true) &&
    (searchTags.length > 0 ? searchTags.every(tag => thought.tags.includes(tag)) : true)
  )

  const wordCount = currentThought.trim().split(/\s+/).length

  return (
    <div className="flex h-screen bg-gradient-to-b from-purple-600 via-indigo-700 to-blue-500 text-gray-100">
      <aside className="w-96 bg-gray-900 bg-opacity-50 p-6 shadow-lg overflow-hidden flex flex-col">
        <h2 className="text-2xl font-semibold mb-4 text-purple-300">Thought Collection</h2>
        <Input
          type="text"
          placeholder="Search thoughts..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="mb-4 bg-gray-800 border-gray-700 text-gray-100"
        />
        <div className="flex items-center mb-4">
          <Input
            type="text"
            placeholder="Search by tag..."
            value={tagInput}
            onChange={(e) => setTagInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && addSearchTag()}
            className="mr-2 bg-gray-800 border-gray-700 text-gray-100"
          />
          <Button onClick={addSearchTag} size="sm" variant="secondary">
            <TagIcon className="h-4 w-4" />
          </Button>
        </div>
        <div className="flex flex-wrap gap-2 mb-4">
          {searchTags.map(tag => (
            <Badge key={tag} variant="secondary" className="text-sm">
              {tag}
              <XIcon 
                className="h-3 w-3 ml-1 cursor-pointer" 
                onClick={() => removeSearchTag(tag)}
              />
            </Badge>
          ))}
        </div>
        <Select onValueChange={(value) => setSelectedCategory(value)}>
          <SelectTrigger className="mb-2 bg-gray-800 border-gray-700 text-gray-100">
            <SelectValue placeholder="Filter by category" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Categories</SelectItem>
            {categories.map(category => (
              <SelectItem key={category} value={category}>{category}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Dialog open={isManageCategoriesOpen} onOpenChange={setIsManageCategoriesOpen}>
          <DialogTrigger asChild>
            <Button className="mb-4 bg-purple-600 hover:bg-purple-700">
              <PlusCircleIcon className="mr-2 h-4 w-4" /> Add/Remove Category
            </Button>
          </DialogTrigger>
          <DialogContent className="bg-gray-800 text-gray-100">
            <DialogHeader>
              <DialogTitle>Manage Categories</DialogTitle>
            </DialogHeader>
            <div className="flex items-center mb-4">
              <Input
                type="text"
                placeholder="New category name..."
                value={newCategory}
                onChange={(e) => setNewCategory(e.target.value)}
                className="mr-2 bg-gray-700 border-gray-600 text-gray-100"
              />
              <Button onClick={addCategory} size="sm" variant="secondary">
                Add
              </Button>
            </div>
            <ScrollArea className="h-[200px]">
              {categories.map(category => (
                <div key={category} className="flex justify-between items-center mb-2">
                  <span>{category}</span>
                  {category !== 'Other' && (
                    <Button 
                      onClick={() => removeCategory(category)} 
                      size="sm" 
                      variant="destructive"
                    >
                      Remove
                    </Button>
                  )}
                </div>
              ))}
            </ScrollArea>
          </DialogContent>
        </Dialog>
        <Button 
          variant={showFavorites ? "secondary" : "outline"} 
          className="mb-4"
          onClick={() => setShowFavorites(!showFavorites)}
        >
          <StarIcon className="mr-2 h-4 w-4" /> {showFavorites ? 'Show All' : 'Show Favorites'}
        </Button>
        <ScrollArea className="flex-grow">
          {filteredThoughts.map(thought => (
            <Card key={thought.id} className="mb-4 bg-gray-800 border-gray-700">
              <CardContent className="p-4">
                <div className="flex justify-between items-start mb-2">
                  <Badge variant={thought.isFavorite ? "secondary" : "outline"} className="text-xs">
                    {thought.category}
                  </Badge>
                  <div className="flex space-x-2">
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      onClick={() => toggleFavorite(thought.id)}
                      className={thought.isFavorite ? "text-yellow-400" : "text-gray-400"}
                    >
                      <StarIcon className="h-4 w-4" />
                    </Button>
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      onClick={() => deleteThought(thought.id)}
                      className="text-red-400"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
                <p className="text-sm font-medium text-gray-100 mb-2">
                  {thought.content.substring(0, 100)}...
                </p>
                <p className="text-xs text-gray-400 mb-2">
                  {format(new Date(thought.createdAt), 'MMM d, yyyy HH:mm')}
                </p>
                <div className="flex flex-wrap gap-1">
                  {thought.tags.map(tag => (
                    <Badge 
                      key={tag} 
                      variant="secondary" 
                      className="text-xs cursor-pointer"
                      onClick={() => setSelectedTag(tag)}
                    >
                      {tag}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </ScrollArea>
        {(selectedCategory || showFavorites || searchTags.length > 0) && (
          <Button 
            variant="outline" 
            className="mt-4" 
            onClick={() => {
              setSelectedCategory(null)
              setShowFavorites(false)
              setSearchTags([])
            }}
          >
            Clear Filters
          </Button>
        )}
      </aside>
      <main className="flex-grow p-8">
        <Card className="w-full max-w-4xl mx-auto bg-gray-900 bg-opacity-50 border-gray-700">
          <CardHeader>
            <CardTitle className="text-3xl font-bold text-center text-purple-300">Notebook</CardTitle>
          </CardHeader>
          <CardContent>
            <Textarea 
              placeholder="Capture your thoughts here..."
              value={currentThought}
              onChange={(e) => setCurrentThought(e.target.value)}
              className="mb-4 h-64 resize-none bg-gray-800 border-gray-700 text-gray-100 font-lobster text-lg"
              style={{ fontFamily: 'Lobster, cursive' }}
            />
            <div className="flex justify-between items-center mb-4">
              <div className="text-sm text-gray-400">
                Word Count: {wordCount}
              </div>
              <Select value={currentCategory} onValueChange={setCurrentCategory}>
                <SelectTrigger className="w-[180px] bg-gray-800 border-gray-700 text-gray-100">
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  {categories.map(category => (
                    <SelectItem key={category} value={category}>{category}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="flex items-center mb-4">
              <Input
                type="text"
                placeholder="Add tags..."
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addTag()}
                className="mr-2 bg-gray-800 border-gray-700 text-gray-100"
              />
              <Button onClick={addTag} size="sm" variant="secondary">
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
            <Button onClick={saveThought} className="w-full bg-purple-600 hover:bg-purple-700">
              <SaveIcon className="mr-2 h-4 w-4" /> Capture Thought
            </Button>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}