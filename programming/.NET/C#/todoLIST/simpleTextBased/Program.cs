
using System;

namespace ToDoListApp
{
    class Program
    {
        static void Main(string[] args)
        {
            ToDoList toDoList = new ToDoList();
            string command = string.Empty;

            Console.WriteLine("Welcome to the To-Do List App!");

            while (command != "exit")
            {
                Console.WriteLine("\nEnter a command (add, remove, complete, list, exit):");
                command = Console.ReadLine().ToLower();

                switch (command)
                {
                    case "add":
                        Console.WriteLine("Enter the task description:");
                        string description = Console.ReadLine();
                        toDoList.AddTask(description);
                        break;
                    case "remove":
                        Console.WriteLine("Enter the task ID to remove:");
                        if (int.TryParse(Console.ReadLine(), out int removeId))
                        {
                            toDoList.RemoveTask(removeId);
                        }
                        else
                        {
                            Console.WriteLine("Invalid ID.");
                        }
                        break;
                    case "complete":
                        Console.WriteLine("Enter the task ID to mark as completed:");
                        if (int.TryParse(Console.ReadLine(), out int completeId))
                        {
                            toDoList.MarkTaskAsCompleted(completeId);
                        }
                        else
                        {
                            Console.WriteLine("Invalid ID.");
                        }
                        break;
                    case "list":
                        toDoList.DisplayTasks();
                        break;
                    case "exit":
                        Console.WriteLine("Exiting the app. Goodbye!");
                        break;
                    default:
                        Console.WriteLine("Invalid command.");
                        break;
                }
            }
        }
    }
}
