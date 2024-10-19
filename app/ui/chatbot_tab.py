import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy 
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor

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

        prompt_box = QLineEdit()
        prompt_button = QPushButton()

        prompt_layout.addWidget(prompt_box)
        prompt_layout.addWidget(prompt_button)

        prompt_widget = QWidget()
        prompt_widget.setLayout(prompt_layout)
        
        chat_widget = QWidget()

        layout.addWidget(prompt_widget)
        layout.addWidget(chat_widget)

        self.setLayout(layout)