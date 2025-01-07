"use client"

import * as React from "react"
import { ChevronDown, Filter, MoreHorizontal, Plus, X, BarChart2, Clock, Users, Menu, Bell, Settings, HelpCircle, LogOut } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog"
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

const initialTickets = [
  { id: "TICK-1001", title: "Implement new user authentication flow", status: "In Progress", priority: "High", assignee: "Alice Smith", created: "2023-07-01" },
  { id: "TICK-1002", title: "Fix responsiveness issues on dashboard", status: "To Do", priority: "Medium", assignee: "Bob Johnson", created: "2023-07-02" },
  { id: "TICK-1003", title: "Optimize database queries for better performance", status: "In Review", priority: "High", assignee: "Charlie Brown", created: "2023-07-03" },
  { id: "TICK-1004", title: "Update privacy policy page", status: "Done", priority: "Low", assignee: "Diana Prince", created: "2023-07-04" },
  { id: "TICK-1005", title: "Implement dark mode across the application", status: "In Progress", priority: "Medium", assignee: "Eve Taylor", created: "2023-07-05" },
]

export function MichaTickets() {
  const [tickets, setTickets] = React.useState(initialTickets)
  const [searchTerm, setSearchTerm] = React.useState("")
  const [statusFilter, setStatusFilter] = React.useState("All")
  const [sortBy, setSortBy] = React.useState("created")
  const [newTicket, setNewTicket] = React.useState({ title: "", description: "", priority: "Medium", assignee: "" })
  const [editingTicket, setEditingTicket] = React.useState(null)
  const [isEditDialogOpen, setIsEditDialogOpen] = React.useState(false)
  const [notifications, setNotifications] = React.useState([
    { id: 1, message: "New ticket assigned to you", read: false },
    { id: 2, message: "Ticket TICK-1002 status updated", read: false },
  ])

  const filteredTickets = tickets
    .filter((ticket) => ticket.title.toLowerCase().includes(searchTerm.toLowerCase()))
    .filter((ticket) => statusFilter === "All" || ticket.status === statusFilter)
    .sort((a, b) => {
      if (sortBy === "created") {
        return new Date(b.created).getTime() - new Date(a.created).getTime()
      } else if (sortBy === "priority") {
        const priorityOrder = { High: 3, Medium: 2, Low: 1 }
        return priorityOrder[b.priority] - priorityOrder[a.priority]
      }
      return 0
    })

  const handleStatusChange = (ticketId, newStatus) => {
    setTickets((prevTickets) =>
      prevTickets.map((ticket) => (ticket.id === ticketId ? { ...ticket, status: newStatus } : ticket))
    )
  }

  const handlePriorityChange = (ticketId, newPriority) => {
    setTickets((prevTickets) =>
      prevTickets.map((ticket) => (ticket.id === ticketId ? { ...ticket, priority: newPriority } : ticket))
    )
  }

  const handleNewTicketSubmit = () => {
    const newTicketId = `TICK-${Math.floor(1000 + Math.random() * 9000)}`
    const createdTicket = {
      id: newTicketId,
      title: newTicket.title,
      status: "To Do",
      priority: newTicket.priority,
      assignee: newTicket.assignee || "Unassigned",
      created: new Date().toISOString().split('T')[0],
    }
    setTickets((prevTickets) => [createdTicket, ...prevTickets])
    setNewTicket({ title: "", description: "", priority: "Medium", assignee: "" })
    addNotification(`New ticket ${newTicketId} created`)
  }

  const handleEditTicket = (ticket) => {
    setEditingTicket(ticket)
    setIsEditDialogOpen(true)
  }

  const handleEditTicketSubmit = () => {
    setTickets((prevTickets) =>
      prevTickets.map((ticket) => (ticket.id === editingTicket.id ? editingTicket : ticket))
    )
    setIsEditDialogOpen(false)
    addNotification(`Ticket ${editingTicket.id} updated`)
  }

  const handleDeleteTicket = (ticketId) => {
    setTickets((prevTickets) => prevTickets.filter((ticket) => ticket.id !== ticketId))
    addNotification(`Ticket ${ticketId} deleted`)
  }

  const getTicketStats = () => {
    const totalTickets = tickets.length
    const openTickets = tickets.filter((ticket) => ticket.status !== "Done").length
    const completedTickets = totalTickets - openTickets
    return { totalTickets, openTickets, completedTickets }
  }

  const addNotification = (message) => {
    const newNotification = {
      id: Date.now(),
      message,
      read: false,
    }
    setNotifications((prev) => [newNotification, ...prev])
  }

  const markAllNotificationsAsRead = () => {
    setNotifications((prev) => prev.map((notification) => ({ ...notification, read: true })))
  }

  const { totalTickets, openTickets, completedTickets } = getTicketStats()

  return (
    <div className="flex h-screen bg-gradient-to-br from-purple-900 via-indigo-800 to-blue-900">
      <Sheet>
        <SheetTrigger asChild>
          <Button variant="outline" size="icon" className="fixed top-4 left-4 z-50 bg-white/10 border-white/30 text-white hover:bg-white/20">
            <Menu className="h-4 w-4" />
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-64 bg-gray-900 text-white border-r border-white/10">
          <SheetHeader>
            <SheetTitle className="text-white">Menu</SheetTitle>
          </SheetHeader>
          <div className="mt-4 space-y-2">
            <Button variant="ghost" className="w-full justify-start text-white hover:bg-white/10">
              <BarChart2 className="mr-2 h-4 w-4" />
              Dashboard
            </Button>
            <Button variant="ghost" className="w-full justify-start text-white hover:bg-white/10">
              <Users className="mr-2 h-4 w-4" />
              Team
            </Button>
            <Button variant="ghost" className="w-full justify-start text-white hover:bg-white/10">
              <Settings className="mr-2 h-4 w-4" />
              Settings
            </Button>
            <Button variant="ghost" className="w-full justify-start text-white hover:bg-white/10">
              <HelpCircle className="mr-2 h-4 w-4" />
              Help
            </Button>
            <Button variant="ghost" className="w-full justify-start text-white hover:bg-white/10">
              <LogOut className="mr-2 h-4 w-4" />
              Logout
            </Button>
          </div>
        </SheetContent>
      </Sheet>
      <div className="flex-grow p-8 overflow-auto">
        <Card className="w-full max-w-4xl mx-auto backdrop-blur-lg bg-white/10 border-none shadow-2xl">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-3xl font-bold text-white">MichaTickets</CardTitle>
            <div className="flex items-center space-x-2">
              <Dialog>
                <DialogTrigger asChild>
                  <Button size="sm" className="bg-purple-600 hover:bg-purple-700 text-white">
                    <Plus className="mr-2 h-4 w-4" />
                    New Ticket
                  </Button>
                </DialogTrigger>
                <DialogContent className="sm:max-w-[425px] bg-gray-900 text-white">
                  <DialogHeader>
                    <DialogTitle>Create New Ticket</DialogTitle>
                  </DialogHeader>
                  <div className="grid gap-4 py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                      <Label htmlFor="title" className="text-right">
                        Title
                      </Label>
                      <Input
                        id="title"
                        value={newTicket.title}
                        onChange={(e) => setNewTicket({ ...newTicket, title: e.target.value })}
                        className="col-span-3 bg-gray-800 border-gray-700 text-white"
                      />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <Label htmlFor="description" className="text-right">
                        Description
                      </Label>
                      <Textarea
                        id="description"
                        value={newTicket.description}
                        onChange={(e) => setNewTicket({ ...newTicket, description: e.target.value })}
                        className="col-span-3 bg-gray-800 border-gray-700 text-white"
                      />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <Label htmlFor="priority" className="text-right">
                        Priority
                      </Label>
                      <Select
                        value={newTicket.priority}
                        onValueChange={(value) => setNewTicket({ ...newTicket, priority: value })}
                      >
                        <SelectTrigger className="col-span-3 bg-gray-800 border-gray-700 text-white">
                          <SelectValue placeholder="Select priority" />
                        </SelectTrigger>
                        <SelectContent className="bg-gray-800 border-gray-700 text-white">
                          <SelectItem value="Low">Low</SelectItem>
                          <SelectItem value="Medium">Medium</SelectItem>
                          <SelectItem value="High">High</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <Label htmlFor="assignee" className="text-right">
                        Assignee
                      </Label>
                      <Input
                        id="assignee"
                        value={newTicket.assignee}
                        onChange={(e) => setNewTicket({ ...newTicket, assignee: e.target.value })}
                        className="col-span-3 bg-gray-800 border-gray-700 text-white"
                      />
                    </div>
                  </div>
                  <Button onClick={handleNewTicketSubmit} className="bg-purple-600 hover:bg-purple-700 text-white">Create Ticket</Button>
                </DialogContent>
              </Dialog>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" size="icon" className="relative bg-white/10 border-white/30 text-white hover:bg-white/20">
                    <Bell className="h-4 w-4" />
                    {notifications.some((n) => !n.read) && (
                      <span className="absolute top-0 right-0 h-2 w-2 rounded-full bg-red-500" />
                    )}
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-[300px] bg-gray-900 text-white border-gray-800">
                  <DropdownMenuLabel className="flex justify-between items-center">
                    Notifications
                    <Button variant="ghost" size="sm" onClick={markAllNotificationsAsRead}>
                      Mark all as read
                    </Button>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator className="bg-gray-800" />
                  {notifications.map((notification) => (
                    <DropdownMenuItem key={notification.id} className={notification.read ? "text-gray-400" : ""}>
                      {notification.message}
                    </DropdownMenuItem>
                  ))}
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </CardHeader>
          <CardContent>
            <div className="flex space-x-2 pb-4">
              <Input
                className="max-w-sm bg-white/20 border-white/30 text-white placeholder-white/50"
                placeholder="Search tickets..."
                type="search"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" className="ml-auto bg-white/20 border-white/30 text-white hover:bg-white/30">
                    <Filter className="mr-2 h-4 w-4" />
                    Filter
                    <ChevronDown className="ml-2 h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-[200px] bg-gray-900 text-white border-gray-800">
                  <DropdownMenuLabel>Filter by Status</DropdownMenuLabel>
                  <DropdownMenuSeparator className="bg-gray-800" />
                  {["All", "To Do", "In Progress", "In Review", "Done"].map((status) => (
                    <DropdownMenuItem
                      key={status}
                      onClick={() => setStatusFilter(status)}
                      className={statusFilter === status ? "bg-purple-600" : ""}
                    >
                      {status}
                    </DropdownMenuItem>
                  ))}
                </DropdownMenuContent>
              </DropdownMenu>
              <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger className="w-[180px] bg-white/20 border-white/30 text-white">
                  <SelectValue placeholder="Sort by" />
                </SelectTrigger>
                <SelectContent className="bg-gray-900 text-white border-gray-800">
                  <SelectItem value="created">Created Date</SelectItem>
                  <SelectItem value="priority">Priority</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="rounded-md border border-white/20 overflow-hidden">
              <Table>
                <TableHeader className="bg-white/10">
                  <TableRow>
                    <TableHead className="w-[100px] text-white">Ticket ID</TableHead>
                    <TableHead className="text-white">Title</TableHead>
                    <TableHead className="text-white">Status</TableHead>
                    <TableHead className="text-white">Priority</TableHead>
                    <TableHead className="text-white">Assignee</TableHead>
                    <TableHead className="text-right text-white">Created</TableHead>
                    <TableHead className="w-[100px]"></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredTickets.map((ticket) => (
                    <TableRow key={ticket.id} className="group border-b border-white/10 hover:bg-white/5 transition-colors">
                      <TableCell className="font-medium text-white">{ticket.id}</TableCell>
                      <TableCell className="text-white">{ticket.title}</TableCell>
                      <TableCell>
                        <Select value={ticket.status} onValueChange={(value) => handleStatusChange(ticket.id, value)}>
                          <SelectTrigger className="w-[120px] bg-transparent border-none text-white">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent className="bg-gray-900 text-white border-gray-800">
                            <SelectItem value="To Do">To Do</SelectItem>
                            <SelectItem value="In Progress">In Progress</SelectItem>
                            <SelectItem value="In Review">In Review</SelectItem>
                            <SelectItem value="Done">Done</SelectItem>
                          </SelectContent>
                        </Select>
                      </TableCell>
                      <TableCell>
                        <Select value={ticket.priority} onValueChange={(value) => handlePriorityChange(ticket.id, value)}>
                          <SelectTrigger className="w-[100px] bg-transparent border-none text-white">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent className="bg-gray-900 text-white border-gray-800">
                            <SelectItem value="Low">Low</SelectItem>
                            <SelectItem value="Medium">Medium</SelectItem>
                            <SelectItem value="High">High</SelectItem>
                          </SelectContent>
                        </Select>
                      </TableCell>
                      <TableCell className="text-white">{ticket.assignee}</TableCell>
                      <TableCell className="text-right text-white">{ticket.created}</TableCell>
                      <TableCell className="text-right">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-8 w-8 p-0 text-white">
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end" className="bg-gray-900 text-white border-gray-800">
                            <DropdownMenuItem onSelect={() => handleEditTicket(ticket)}>Edit ticket</DropdownMenuItem>
                            <DropdownMenuItem onSelect={() => handleStatusChange(ticket.id, "Done")}>Mark as Done</DropdownMenuItem>
                            <DropdownMenuSeparator className="bg-gray-800" />
                            <AlertDialog>
                              <AlertDialogTrigger asChild>
                                <DropdownMenuItem onSelect={(e) => e.preventDefault()} className="text-red-400">Delete ticket</DropdownMenuItem>
                              </AlertDialogTrigger>
                              <AlertDialogContent className="bg-gray-900 text-white border-gray-800">
                                <AlertDialogHeader>
                                  <AlertDialogTitle>Are you sure you want to delete this ticket?</AlertDialogTitle>
                                  <AlertDialogDescription className="text-gray-400">
                                    This action cannot be undone. This will permanently delete the ticket.
                                  </AlertDialogDescription>
                                </AlertDialogHeader>
                                <AlertDialogFooter>
                                  <AlertDialogCancel className="bg-gray-800 text-white hover:bg-gray-700">Cancel</AlertDialogCancel>
                                  <AlertDialogAction onClick={() => handleDeleteTicket(ticket.id)} className="bg-red-600 hover:bg-red-700">Delete</AlertDialogAction>
                                </AlertDialogFooter>
                              </AlertDialogContent>
                            </AlertDialog>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
            <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card className="bg-white/10 border-none">
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-white">Total Tickets</CardTitle>
                  <BarChart2 className="h-4 w-4 text-white" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-white">{totalTickets}</div>
                </CardContent>
              </Card>
              <Card className="bg-white/10 border-none">
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-white">Open Tickets</CardTitle>
                  <Clock className="h-4 w-4 text-white" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-white">{openTickets}</div>
                </CardContent>
              </Card>
              <Card className="bg-white/10 border-none">
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-white">Completed Tickets</CardTitle>
                  <Users className="h-4 w-4 text-white" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-white">{completedTickets}</div>
                </CardContent>
              </Card>
            </div>
          </CardContent>
        </Card>
      </div>
      <Sheet>
        <SheetTrigger asChild>
          <Button variant="outline" size="icon" className="fixed top-4 right-4 z-50 bg-white/10 border-white/30 text-white hover:bg-white/20">
            <Settings className="h-4 w-4" />
          </Button>
        </SheetTrigger>
        <SheetContent side="right" className="w-[300px] sm:w-[400px] bg-gray-900 text-white border-l border-white/10">
          <SheetHeader>
            <SheetTitle className="text-white">Settings</SheetTitle>
          </SheetHeader>
          <div className="py-4">
            <Tabs defaultValue="account" className="w-full">
              <TabsList className="grid w-full grid-cols-2 bg-gray-800">
                <TabsTrigger value="account" className="text-white data-[state=active]:bg-gray-700">Account</TabsTrigger>
                <TabsTrigger value="notifications" className="text-white data-[state=active]:bg-gray-700">Notifications</TabsTrigger>
              </TabsList>
              <TabsContent value="account">
                <Card className="bg-gray-800 border-gray-700">
                  <CardHeader>
                    <CardTitle className="text-white">Account Settings</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <div className="space-y-1">
                      <Label htmlFor="name" className="text-white">Name</Label>
                      <Input id="name" defaultValue="John Doe" className="bg-gray-700 border-gray-600 text-white" />
                    </div>
                    <div className="space-y-1">
                      <Label htmlFor="email" className="text-white">Email</Label>
                      <Input id="email" defaultValue="john@example.com" className="bg-gray-700 border-gray-600 text-white" />
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
              <TabsContent value="notifications">
                <Card className="bg-gray-800 border-gray-700">
                  <CardHeader>
                    <CardTitle className="text-white">Notification Settings</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <input type="checkbox" id="email-notifications" className="bg-gray-700 border-gray-600" />
                      <Label htmlFor="email-notifications" className="text-white">Email Notifications</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <input type="checkbox" id="push-notifications" className="bg-gray-700 border-gray-600" />
                      <Label htmlFor="push-notifications" className="text-white">Push Notifications</Label>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </SheetContent>
      </Sheet>
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent className="sm:max-w-[425px] bg-gray-900 text-white">
          <DialogHeader>
            <DialogTitle>Edit Ticket</DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="edit-title" className="text-right">
                Title
              </Label>
              <Input
                id="edit-title"
                value={editingTicket?.title || ""}
                onChange={(e) => setEditingTicket({ ...editingTicket, title: e.target.value })}
                className="col-span-3 bg-gray-800 border-gray-700 text-white"
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="edit-status" className="text-right">
                Status
              </Label>
              <Select
                value={editingTicket?.status || ""}
                onValueChange={(value) => setEditingTicket({ ...editingTicket, status: value })}
              >
                <SelectTrigger className="col-span-3 bg-gray-800 border-gray-700 text-white">
                  <SelectValue placeholder="Select status" />
                </SelectTrigger>
                <SelectContent className="bg-gray-800 border-gray-700 text-white">
                  <SelectItem value="To Do">To Do</SelectItem>
                  <SelectItem value="In Progress">In Progress</SelectItem>
                  <SelectItem value="In Review">In Review</SelectItem>
                  <SelectItem value="Done">Done</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="edit-priority" className="text-right">
                Priority
              </Label>
              <Select
                value={editingTicket?.priority || ""}
                onValueChange={(value) => setEditingTicket({ ...editingTicket, priority: value })}
              >
                <SelectTrigger className="col-span-3 bg-gray-800 border-gray-700 text-white">
                  <SelectValue placeholder="Select priority" />
                </SelectTrigger>
                <SelectContent className="bg-gray-800 border-gray-700 text-white">
                  <SelectItem value="Low">Low</SelectItem>
                  <SelectItem value="Medium">Medium</SelectItem>
                  <SelectItem value="High">High</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="edit-assignee" className="text-right">
                Assignee
              </Label>
              <Input
                id="edit-assignee"
                value={editingTicket?.assignee || ""}
                onChange={(e) => setEditingTicket({ ...editingTicket, assignee: e.target.value })}
                className="col-span-3 bg-gray-800 border-gray-700 text-white"
              />
            </div>
          </div>
          <Button onClick={handleEditTicketSubmit} className="bg-purple-600 hover:bg-purple-700 text-white">Save Changes</Button>
        </DialogContent>
      </Dialog>
    </div>
  )
}