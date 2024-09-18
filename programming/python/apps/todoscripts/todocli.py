# Step 2: Define Data Structures
tasks = []

# Step 3.1: Add Task
def add_task():
    task_name = input("Enter the task: ")
    task = {"name": task_name, "completed": False}
    tasks.append(task)
    print(f"Task '{task_name}' added.")

# Step 3.2: List Tasks
def list_tasks():
    if not tasks:
        print("No tasks found.")
    else:
        for idx, task in enumerate(tasks):
            status = "Completed" if task["completed"] else "Not Completed"
            print(f"{idx + 1}. {task['name']} - {status}")

# Step 3.3: Mark Task as Completed
def mark_completed():
    list_tasks()
    task_index = int(input("Enter the task number to mark as completed: ")) - 1
    if 0 <= task_index < len(tasks):
        tasks[task_index]["completed"] = True
        print(f"Task '{tasks[task_index]['name']}' marked as completed.")
    else:
        print("Invalid task number.")

# Step 4: Create a Menu
while True:
    print("\nTo-Do App Menu:")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Mark Task as Completed")
    print("4. Quit")
    
    choice = input("Enter your choice (1/2/3/4): ")
    
    if choice == '1':
        add_task()
    elif choice == '2':
        list_tasks()
    elif choice == '3':
        mark_completed()
    elif choice == '4':
        break
    else:
        print("Invalid choice. Please try again.")