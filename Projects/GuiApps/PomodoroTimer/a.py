import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QInputDialog, QTextEdit, QProgressBar, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt, QTime, QSettings


class PomodoroTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadSettings()

    def initUI(self):
        self.setWindowTitle('Pomodoro Timer')
        self.setGeometry(100, 100, 400, 300)

        self.setStyleSheet("background-color: black; color: white; font-family: Lobster; font-size: 32px;")  # Increased font size to 32px

        self.work_time = 25 * 60
        self.break_time = 5 * 60

        self.current_time = self.work_time

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)

        tomato_logo = QLabel(self)
        pixmap = QPixmap('C:\\study\\python\\scripts\\PomodoroTimer\\tomato.jpg')  # Path to your tomato logo image
        tomato_logo.setPixmap(pixmap)
        tomato_logo.setAlignment(Qt.AlignCenter)

        self.task_label = QLabel('Current Task:', self)
        self.task_label.setStyleSheet("font-weight: bold;")

        self.task_description = QTextEdit(self)
        self.task_description.setPlaceholderText("Enter task description...")

        self.timer_label = QLabel(self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-weight: bold;")

        self.updateLabel()

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(100)
        self.progress_bar.setTextVisible(False)

        start_button = QPushButton('Start', self)
        start_button.setStyleSheet("font-weight: bold;")
        start_button.clicked.connect(self.startTimer)

        pause_button = QPushButton('Pause', self)
        pause_button.setStyleSheet("font-weight: bold;")
        pause_button.clicked.connect(self.pauseTimer)

        reset_button = QPushButton('Reset', self)
        reset_button.setStyleSheet("font-weight: bold;")
        reset_button.clicked.connect(self.resetTimer)

        work_time_button = QPushButton('Set Work Time', self)
        work_time_button.setStyleSheet("font-weight: bold;")
        work_time_button.clicked.connect(self.setWorkTime)

        break_time_button = QPushButton('Set Break Time', self)
        break_time_button.setStyleSheet("font-weight: bold;")
        break_time_button.clicked.connect(self.setBreakTime)

        layout = QVBoxLayout()
        layout.addWidget(tomato_logo)
        layout.addWidget(self.task_label)
        layout.addWidget(self.task_description)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.progress_bar)

        button_layout = QHBoxLayout()
        button_layout.addWidget(start_button)
        button_layout.addWidget(pause_button)
        button_layout.addWidget(reset_button)
        button_layout.addWidget(work_time_button)
        button_layout.addWidget(break_time_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def updateLabel(self):
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        self.timer_label.setText(f'{minutes:02d}:{seconds:02d}')

    def updateTimer(self):
        self.current_time -= 1
        if self.current_time <= 0:
            self.timer.stop()
            self.current_time = 0
            self.alert()
            self.logTask()
            self.saveSettings()
        self.updateLabel()
        progress_value = int((self.current_time / self.work_time) * 100)
        self.progress_bar.setValue(progress_value)

    def startTimer(self):
        self.timer.start(1000)

    def pauseTimer(self):
        self.timer.stop()

    def resetTimer(self):
        self.timer.stop()
        self.current_time = self.work_time
        self.updateLabel()
        self.progress_bar.setValue(100)

    def setWorkTime(self):
        minutes, ok = QInputDialog.getInt(self, 'Set Work Time', 'Enter work time (minutes):', value=self.work_time // 60)
        if ok:
            self.work_time = minutes * 60
            if self.current_time == self.work_time:
                self.updateLabel()

    def setBreakTime(self):
        minutes, ok = QInputDialog.getInt(self, 'Set Break Time', 'Enter break time (minutes):', value=self.break_time // 60)
        if ok:
            self.break_time = minutes * 60

    def alert(self):
        QMessageBox.information(self, "Session Complete", "Your Pomodoro session is complete!")

    def logTask(self):
        task_description = self.task_description.toPlainText()
        with open(f'task_log_{QTime.currentTime().toString("hh_mm_ss")}.txt', 'a') as f:
            f.write(f'Task: {task_description}\n')
            f.write(f'Time: {QTime.currentTime().toString()}\n\n')

    def saveSettings(self):
        settings = QSettings("PomodoroApp", "Settings")
        settings.setValue("work_time", self.work_time)
        settings.setValue("break_time", self.break_time)

    def loadSettings(self):
        settings = QSettings("PomodoroApp", "Settings")
        self.work_time = settings.value("work_time", 25 * 60, type=int)
        self.break_time = settings.value("break_time", 5 * 60, type=int)
        self.current_time = self.work_time
        self.updateLabel()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer = PomodoroTimer()
    timer.show()
    sys.exit(app.exec_())
