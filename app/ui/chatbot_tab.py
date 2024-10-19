import threading
import sys
from PyQt6.QtWidgets import (
    QApplication, QTextEdit, QScrollArea, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ..chatbot import ask

color_light = '#cccccc'
color_dark = '#b3b3b3'

class ChatbotTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        self.searching = False

        prompt_layout = QHBoxLayout()
        prompt_layout.setContentsMargins(2, 2, 2, 2)
        prompt_layout.setSpacing(0)

        # Using QTextEdit for multi-line input
        self.prompt_box = QTextEdit()
        self.prompt_box.setFixedHeight(50)  # Set fixed height
        self.prompt_box.setFixedWidth(900)   # Set fixed width
        self.prompt_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Set the background color of the prompt box
        self.prompt_box.setStyleSheet("QTextEdit {background-color: #444444; color: white;}")

        # Set font size for the prompt box
        font = QFont()
        font.setPointSize(12)  # Set initial font size
        self.prompt_box.setFont(font)

        # Submit button
        prompt_button = QPushButton("Submit")
        prompt_button.setFixedHeight(50)  # Fixed height for the button
        prompt_button.setFixedWidth(80)    # Fixed width for the button
        prompt_button.clicked.connect(self.submit_prompt)

        prompt_layout.addWidget(self.prompt_box)
        prompt_layout.addWidget(prompt_button)

        prompt_widget = QWidget()
        prompt_widget.setLayout(prompt_layout)

        self.chat_widget_layout = QVBoxLayout()
        self.chat_widget = QWidget()
        self.chat_widget.setLayout(self.chat_widget_layout)
        self.chat_widget_layout.setContentsMargins(10, 10, 10, 10)

        self.chat_scroller = QScrollArea()
        self.chat_scroller.setWidget(self.chat_widget)
        self.chat_scroller.setWidgetResizable(True)
        self.chat_scroller.setStyleSheet("background-color: #212121")

        layout.addWidget(self.chat_scroller)
        layout.addWidget(prompt_widget)

        self.setLayout(layout)

    def submit_prompt(self):
        prompt = self.prompt_box.toPlainText()  # Get text from QTextEdit
        self.prompt_box.clear()
        
        # Set larger font size for the prompt label
        prompt_label = QLabel(prompt)
        prompt_label.setWordWrap(True)  # Enable word wrap
        prompt_label.setStyleSheet("QLabel {color: white; border-radius: 15px; background-color: #555555; padding: 10px;}")  # Rounded corners and color
        prompt_label.setMinimumHeight(40)  # Optional: Set a minimum height to control appearance
        font = QFont("Arial", 14)  # Set a nicer font
        prompt_label.setFont(font)  # Apply the font to the label

        # Add prompt label to chat widget layout
        self.chat_widget_layout.addWidget(prompt_label, alignment=Qt.AlignmentFlag.AlignRight)

        # Create a response label
        response_label = QLabel("Searching the web for answers...")
        response_label.setWordWrap(True)  # Enable word wrap for the response label
        response_label.setStyleSheet("QLabel {color: white; border-radius: 15px; background-color: #444444; margin: 10px; padding: 10px;}")  # Rounded corners and color
        response_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Allow the label to expand horizontally
        response_label.setFont(QFont("Arial", 14))  # Set a nicer font

        # Add the response label to the chat widget layout
        self.chat_widget_layout.addWidget(response_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Start a thread to fetch the response
        thread = threading.Thread(target=self.concurrent_ask, args=(prompt, response_label))
        thread.start()  # Start the thread to fetch response


    def concurrent_ask(self, prompt, response_label):
        self.searching = True
        response = ask(prompt)
        response_label.setText(response)
        self.searching = False
    
    def keyPressEvent(self, event):
        # Check for Enter or Return key press
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.submit_prompt()  # Call submit prompt
        else:
            super().keyPressEvent(event)  # Call the base class method

# Add the following lines if you're running this as a standalone application.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatbotTab()
    window.show()
    sys.exit(app.exec())
