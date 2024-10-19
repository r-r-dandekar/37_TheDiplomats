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

        # Create Edit Menu
        edit_menu = self.addMenu("Edit")

        # Create actions for the Edit Menu
        cut_action = QAction("Cut", self)
        cut_action.triggered.connect(parent.cut_text)  # Connect to the cut_text method
        edit_menu.addAction(cut_action)

        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(parent.copy_text)  # Connect to the copy_text method
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.triggered.connect(parent.paste_text)  # Connect to the paste_text method
        edit_menu.addAction(paste_action)

        # You can also add additional menus if needed
