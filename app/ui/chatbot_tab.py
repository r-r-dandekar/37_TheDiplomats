import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy 
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor
from ..chatbot import ask

color_light = '#cccccc'
color_dark = '#b3b3b3'

class ChatbotTab(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        prompt_layout = QHBoxLayout()
        prompt_layout.setContentsMargins(0,0,0,0)
        prompt_layout.setSpacing(0)

        self.prompt_box = QLineEdit()
        prompt_button = QPushButton("Submit")
        prompt_button.clicked.connect(self.submit_prompt)

        prompt_layout.addWidget(self.prompt_box)
        prompt_layout.addWidget(prompt_button)

        prompt_widget = QWidget()
        prompt_widget.setLayout(prompt_layout)
        
        self.chat_widget_layout = QVBoxLayout()
        self.chat_widget = QWidget()
        self.chat_widget.setLayout(self.chat_widget_layout)

        self.chat_scroller = QScrollArea()
        self.chat_scroller.setWidget(self.chat_widget)
        self.chat_scroller.setWidgetResizable(True)  
        self.chat_scroller.setStyleSheet(f"background-color: gray") 

        layout.addWidget(self.chat_scroller)
        layout.addWidget(prompt_widget)

        self.setLayout(layout)

    def submit_prompt(self):
        prompt = self.prompt_box.text()
        self.prompt_box.clear()
        prompt_label = QLabel(prompt)
        prompt_label.setStyleSheet(f"color: black; background-color: gray")
        self.chat_widget_layout.addWidget(prompt_label, alignment=Qt.AlignmentFlag.AlignRight)
        response = ask(prompt)
        response_label = QLabel(response)
        response_label.setStyleSheet(f"color: black; background-color: white")
        self.chat_widget_layout.addWidget(response_label, alignment=Qt.AlignmentFlag.AlignLeft)
        