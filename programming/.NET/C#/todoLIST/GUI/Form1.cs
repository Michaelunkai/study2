using System;
using System.Windows.Forms;

namespace ToDoListApp
{
    public partial class Form1 : Form
    {
        private ToDoList toDoList;

        public Form1()
        {
            InitializeComponent();
            toDoList = new ToDoList();
        }

        private void btnAddTask_Click(object sender, EventArgs e)
        {
            string description = txtTaskDescription.Text;
            if (!string.IsNullOrWhiteSpace(description))
            {
                toDoList.AddTask(description);
                txtTaskDescription.Clear();
                RefreshTaskList();
            }
            else
            {
                MessageBox.Show("Please enter a task description.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void btnRemoveTask_Click(object sender, EventArgs e)
        {
            if (lstTasks.SelectedItem != null)
            {
                var selectedTask = (Task)lstTasks.SelectedItem;
                toDoList.RemoveTask(selectedTask.Id);
                RefreshTaskList();
            }
            else
            {
                MessageBox.Show("Please select a task to remove.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void btnMarkCompleted_Click(object sender, EventArgs e)
        {
            if (lstTasks.SelectedItem != null)
            {
                var selectedTask = (Task)lstTasks.SelectedItem;
                toDoList.MarkTaskAsCompleted(selectedTask.Id);
                RefreshTaskList();
            }
            else
            {
                MessageBox.Show("Please select a task to mark as completed.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void RefreshTaskList()
        {
            lstTasks.DataSource = null;
            lstTasks.DataSource = toDoList.GetTasks();
        }
    }
}
