using System.Windows.Forms;

namespace ToDoListApp
{
    partial class Form1
    {
        private System.ComponentModel.IContainer components = null;
        private TextBox txtTaskDescription;
        private Button btnAddTask;
        private ListBox lstTasks;
        private Button btnMarkCompleted;
        private Button btnRemoveTask;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.txtTaskDescription = new TextBox();
            this.btnAddTask = new Button();
            this.lstTasks = new ListBox();
            this.btnMarkCompleted = new Button();
            this.btnRemoveTask = new Button();
            this.SuspendLayout();
            // 
            // txtTaskDescription
            // 
            this.txtTaskDescription.Location = new System.Drawing.Point(13, 13);
            this.txtTaskDescription.Name = "txtTaskDescription";
            this.txtTaskDescription.Size = new System.Drawing.Size(200, 20);
            this.txtTaskDescription.TabIndex = 0;
            // 
            // btnAddTask
            // 
            this.btnAddTask.Location = new System.Drawing.Point(220, 10);
            this.btnAddTask.Name = "btnAddTask";
            this.btnAddTask.Size = new System.Drawing.Size(75, 23);
            this.btnAddTask.TabIndex = 1;
            this.btnAddTask.Text = "Add Task";
            this.btnAddTask.UseVisualStyleBackColor = true;
            this.btnAddTask.Click += new System.EventHandler(this.btnAddTask_Click);
            // 
            // lstTasks
            // 
            this.lstTasks.FormattingEnabled = true;
            this.lstTasks.Location = new System.Drawing.Point(13, 40);
            this.lstTasks.Name = "lstTasks";
            this.lstTasks.Size = new System.Drawing.Size(282, 147);
            this.lstTasks.TabIndex = 2;
            // 
            // btnMarkCompleted
            // 
            this.btnMarkCompleted.Location = new System.Drawing.Point(13, 194);
            this.btnMarkCompleted.Name = "btnMarkCompleted";
            this.btnMarkCompleted.Size = new System.Drawing.Size(105, 23);
            this.btnMarkCompleted.TabIndex = 3;
            this.btnMarkCompleted.Text = "Mark Completed";
            this.btnMarkCompleted.UseVisualStyleBackColor = true;
            this.btnMarkCompleted.Click += new System.EventHandler(this.btnMarkCompleted_Click);
            // 
            // btnRemoveTask
            // 
            this.btnRemoveTask.Location = new System.Drawing.Point(124, 194);
            this.btnRemoveTask.Name = "btnRemoveTask";
            this.btnRemoveTask.Size = new System.Drawing.Size(105, 23);
            this.btnRemoveTask.TabIndex = 4;
            this.btnRemoveTask.Text = "Remove Task";
            this.btnRemoveTask.UseVisualStyleBackColor = true;
            this.btnRemoveTask.Click += new System.EventHandler(this.btnRemoveTask_Click);
            // 
            // Form1
            // 
            this.ClientSize = new System.Drawing.Size(307, 229);
            this.Controls.Add(this.btnRemoveTask);
            this.Controls.Add(this.btnMarkCompleted);
            this.Controls.Add(this.lstTasks);
            this.Controls.Add(this.btnAddTask);
            this.Controls.Add(this.txtTaskDescription);
            this.Name = "Form1";
            this.Text = "To-Do List App";
            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}
