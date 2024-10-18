    # app/ui/widgets/menubar.py
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction


class MenuBar(QMenuBar):
        """
        Initialize the menu bar.

        Args:
            parent: The parent widget.
        """

        def __init__(self, parent=None) -> None:
            super().__init__(parent)

            # Create File Menu
            file_menu = self.addMenu("File")

            # Create actions for the File Menu
            open_action = QAction("Open", self)
            open_action.triggered.connect(parent.open_folder)  # Connect to the open_folder method
            file_menu.addAction(open_action)

            

            # You can also add additional menus if needed
