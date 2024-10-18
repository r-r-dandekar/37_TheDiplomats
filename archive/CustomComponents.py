from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt6.QtGui import QPalette, QColor
from config import config

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class BorderLayout(QVBoxLayout):

    def __init__(self):
        super(QVBoxLayout, self).__init__()
        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(0,0,0,0)
        self.top_layout.setSpacing(0)
        self.middle_layout = QHBoxLayout()
        self.middle_layout.setContentsMargins(0,0,0,0)
        self.middle_layout.setSpacing(0)
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0,0,0,0)
        self.bottom_layout.setSpacing(0)

        self.top_widget = Color(config['bg_primary'])
        self.top_widget.setLayout(self.top_layout)
        self.middle_widget = Color(config['bg_primary'])
        self.middle_widget.setLayout(self.middle_layout)
        self.bottom_widget = Color(config['bg_primary'])
        self.bottom_widget.setLayout(self.bottom_layout)

        self.addWidget(self.top_widget)
        self.addWidget(self.middle_widget)
        self.addWidget(self.bottom_widget)
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)
        
        self.top_widget.setMinimumHeight(20)
        self.top_widget.setMaximumHeight(20)
        self.bottom_widget.setMinimumHeight(30)
        self.bottom_widget.setMaximumHeight(100)