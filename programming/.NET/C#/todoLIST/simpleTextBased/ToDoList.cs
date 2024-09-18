
using System;
using System.Collections.Generic;

namespace ToDoListApp
{
    public class ToDoList
    {
        private List<Task> tasks;
        private int nextId;

        public ToDoList()
        {
            tasks = new List<Task>();
            nextId = 1;
        }

        public void AddTask(string description)
        {
            tasks.Add(new Task { Id = nextId++, Description = description, IsCompleted = false });
        }

        public void RemoveTask(int id)
        {
            tasks.RemoveAll(t => t.Id == id);
        }

        public void MarkTaskAsCompleted(int id)
        {
            var task = tasks.Find(t => t.Id == id);
            if (task != null)
            {
                task.IsCompleted = true;
            }
        }

        public void DisplayTasks()
        {
            Console.WriteLine("To-Do List:");
            foreach (var task in tasks)
            {
                Console.WriteLine(task);
            }
        }
    }
}
