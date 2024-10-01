import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
import requests
from bs4 import BeautifulSoup

class APIKeyTutorialApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('How to Get API Key Tutorial Tool')
        self.setGeometry(100, 100, 1200, 900)
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #FFFFFF;
                font-size: 24px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px;
                border: none;
                border-radius: 10px;
                font-size: 28px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 15px;
                border: 2px solid #4CAF50;
                border-radius: 10px;
                font-size: 24px;
                color: #FFFFFF;
                background-color: #1E1E1E;
            }
            QTextEdit {
                border: 2px solid #4CAF50;
                border-radius: 10px;
                font-size: 22px;
                color: #FFFFFF;
                background-color: #1E1E1E;
            }
        """)

        main_layout = QVBoxLayout()

        label = QLabel("Enter the name of the service you want to get an API key for:")
        label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label)

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setFixedHeight(70)
        input_layout.addWidget(self.input_field)

        self.guide_button = QPushButton("Guide Me")
        self.guide_button.setFixedSize(200, 70)
        self.guide_button.clicked.connect(self.generate_tutorial)
        input_layout.addWidget(self.guide_button)

        main_layout.addLayout(input_layout)

        self.tutorial_area = QTextEdit()
        self.tutorial_area.setReadOnly(True)
        self.tutorial_area.setFont(QFont("Arial", 22, QFont.Bold))
        main_layout.addWidget(self.tutorial_area)

        self.setLayout(main_layout)

    def generate_tutorial(self):
        service = self.input_field.text().strip().lower()
        tutorial = self.get_api_key_tutorial(service)
        self.tutorial_area.setPlainText(tutorial)

    def get_api_key_tutorial(self, service):
        # Always generate a custom tutorial
        return self.generate_custom_tutorial(service)

    def generate_custom_tutorial(self, service):
        try:
            url = f"https://www.google.com/search?q=how+to+get+api+key+for+{service}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            paragraphs = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
            info = [p.text.strip() for p in paragraphs if p.text.strip()]
            
            steps = self.create_comprehensive_steps(service, info)
            formatted_steps = "\n".join(f"{i+1}. {step}" for i, step in enumerate(steps))
            
            return f"Step-by-step guide to get an API key for {service.capitalize()}:\n\n{formatted_steps}\n\nRemember to keep your API key secure and never share it publicly!\n\nNote: This guide is generated based on available information. For the most accurate and up-to-date instructions, always refer to the official {service.capitalize()} documentation."
        except Exception as e:
            return f"An error occurred while fetching information for {service}. Please try again later or check the official documentation."

    def create_comprehensive_steps(self, service, info):
        common_steps = [
            f"Go to the official {service.capitalize()} website",
            f"Sign in to your {service.capitalize()} account or create one if you don't have it",
            f"Look for a 'Developer' or 'API' section in the website",
            f"Find and click on an option like 'Get API Key' or 'Create New API Key'",
            "You may need to agree to terms of service or select specific API features",
            "Generate the API key",
            "Copy your new API key and store it securely",
            f"Implement the API key in your {service.capitalize()} API requests"
        ]
        
        specific_steps = []
        for text in info:
            sentences = text.split('. ')
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in ['api', 'key', 'token', 'credential']):
                    specific_steps.append(sentence.strip())
        
        # Combine common steps with any specific steps found
        combined_steps = common_steps[:3] + specific_steps + common_steps[3:]
        
        # Ensure steps are unique and start with an action verb
        unique_steps = []
        for step in combined_steps:
            cleaned_step = step.lstrip('0123456789.) ').capitalize()
            if not any(cleaned_step in s for s in unique_steps):
                if not cleaned_step.startswith(('Go', 'Sign', 'Look', 'Find', 'Generate', 'Copy', 'Implement')):
                    cleaned_step = f"Follow this step: {cleaned_step}"
                unique_steps.append(cleaned_step)
        
        return unique_steps[:12]  # Limit to 12 steps for readability

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = APIKeyTutorialApp()
    ex.show()
    sys.exit(app.exec_())
