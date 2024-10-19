import sys
from PyQt6.QtWidgets import QApplication, QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy 
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor
from ...utils.config import config

HEIGHT = 35
color_light = '#cccccc'
color_dark = '#b3b3b3'

class AccordionSection(QWidget):

    def __init__(self, title, content, color):
        super().__init__()

        self.color = color

        self.setFixedHeight(HEIGHT)
        
        # Create the layout for the section
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.main_layout.setContentsMargins(15,5,0,5)
        self.main_layout.setSpacing(0)

        # Create the toggle button for the accordion (will contain circle, title, and arrow)
        self.toggle_button = QPushButton()
        self.toggle_button.setCheckable(True)
        self.toggle_button.setFlat(True)
        self.toggle_button.clicked.connect(self.toggle_content)
        self.toggle_button.setStyleSheet("text-align: left; padding: 0px;")  # Add padding for appearance
        self.toggle_button.setFixedHeight(HEIGHT)

        # Create a horizontal layout for the button content
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10,0,5,2)
        button_layout.setSpacing(0)

        # Small circle on the left
        self.circle_label = QLabel()
        self.circle_label.setFixedSize(15, 15)
        self.circle_label.setStyleSheet(f"background-color: {color}; border-radius: 7px;")  # Circle styling

        # Title label
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: black;")

        # Arrow icon on the right
        self.arrow_label = QLabel()
        self.arrow_down = QPixmap("app/ui/images/arrow_down.png").scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio)
        self.arrow_right = QPixmap("app/ui/images/arrow_right.png").scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio)
        self.arrow_label.setPixmap(self.arrow_right)

        # Add circle, title, and arrow to the button layout
        button_layout.addWidget(self.circle_label)
        button_layout.addWidget(self.title_label)
        button_layout.addStretch()  # Push arrow to the right
        button_layout.addWidget(self.arrow_label)

        # Set the button layout and add it to the toggle button
        self.toggle_button.setLayout(button_layout)

        # Create the content of the accordion
        self.content_area = QWidget()
        self.content_area_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_area_layout)
        self.main_layout.setContentsMargins(5,5,5,5)
        self.main_layout.setSpacing(0)
        # self.content_area_layout.addWidget(QLabel(content))
        self.content_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.content_area.setStyleSheet(f"background-color: {color_light}; border: 1px solid {color_light};")

        self.scroll_area = QScrollArea()
        self.scroll_area.setVisible(False)  # Initially collapsed
        self.scroll_area.setWidget(self.content_area)
        self.scroll_area.setWidgetResizable(True)  

        # Add the button and content area to the main layout
        self.main_layout.addWidget(self.toggle_button)
        self.main_layout.addWidget(self.scroll_area)

        # Set the layout for the section
        self.setLayout(self.main_layout)
        self.setStyleSheet(f"background-color: {color_dark}; padding: 5px; border: 1px solid {color_dark}; margin: 0px;")

    def toggle_content(self):
        # Toggle the visibility of the content area
        visible = not self.content_area.isVisible()
        if not visible:
            self.setMaximumHeight(HEIGHT)
        else:
            self.setMaximumHeight(1000)
        self.scroll_area.setVisible(visible)
        # Change the arrow icon based on the expanded/collapsed state
        self.arrow_label.setPixmap(self.arrow_down if visible else self.arrow_right)

    def show_list(self, list):
        for str in list:
            label = QLabel(str)
            label.setStyleSheet(f"color: {self.color};")
            self.content_area_layout.addWidget(label)


class Accordion(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout for the entire accordion
        self.layout = QVBoxLayout()

        # Ensure the sections are aligned to the top
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add accordion sections
        self.add_accordion_section("Section 1", "This is the content of Section 1")
        self.add_accordion_section("Section 2", "This is the content of Section 2")
        self.add_accordion_section("Section 3", "This is the content of Section 3")

        # Set the layout for the main widget
        self.setLayout(self.layout)

    def add_accordion_section(self, title, content):
        # Create a new AccordionSection and add it to the main layout
        section = AccordionSection(title, content)
        self.layout.addWidget(section)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Accordion()
    window.setWindowTitle("Accordion with Circle and Arrow Inside Button")
    window.setGeometry(300, 200, 400, 300)
    window.show()

    sys.exit(app.exec())
