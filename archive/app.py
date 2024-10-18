import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from CustomComponents import BorderLayout, Color
from config import config

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")


        layout = BorderLayout()

        self.top = Color(config['bg_tertiary'])
        self.left = Color(config['bg_secondary'])
        self.middle = Color(config['bg_primary'])
        self.right = Color(config['bg_secondary'])
        self.bottom = Color(config['bg_tertiary'])

        layout.top_layout.addWidget(self.top)
        layout.middle_layout.addWidget(self.left, 20)
        layout.middle_layout.addWidget(self.middle, 60)
        layout.middle_layout.addWidget(self.right, 20)
        layout.bottom_layout.addWidget(self.bottom)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()