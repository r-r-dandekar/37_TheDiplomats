import sys
import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QTextEdit, QFileDialog, QTreeView
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import Qt, QDir
from ..utils.config import AppConfig
from .widgets.menubar import MenuBar
from .widgets.toolbar import ToolBar
from .widgets.statusbar import StatusBar


class MainWindow(QMainWindow):
    """
    MainWindow

    Args:
        QMainWindow (QMainWindow): Inheritance
    """

    def __init__(self) -> None:
        """
        Initialize the Main-Window.
        """
        super().__init__()
        # Window-Settings
        self.setWindowTitle(AppConfig.APP_NAME)
        self.setGeometry(100, 100, 800, 600)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        central_widget.setLayout(layout)

        # Create Widgets
        self.treeview = self.create_treeview()
        self.editbox = self.create_edit()

        self.create_toolbars()

        # Add Widgets to Window
        self.setMenuBar(MenuBar(self))
        self.setStatusBar(StatusBar(self))

        layout.addWidget(self.treeview)
        layout.addWidget(self.editbox, stretch=1)
        layout.addWidget(self.editbox)

    def create_toolbars(self) -> None:
        """
        Creates and adds the top and right toolbars to the main window.
        """
        # Top Toolbar [PyQt6.QtWidgets.QToolBar]
        self.topbar = ToolBar(self, orientation=Qt.Orientation.Horizontal,
                              style=Qt.ToolButtonStyle.ToolButtonTextUnderIcon, icon_size=(24, 24))

        # Top Toolbar Buttons
        self.topbar.add_button(
            "Open", "resources/assets/icons/windows/imageres-10.ico", self.open_folder)
        self.topbar.add_button(
            "Save", "resources/assets/icons/windows/shell32-259.ico", self.save_file)
        self.topbar.add_separator()
        self.topbar.add_button(
            "Exit", "resources/assets/icons/windows/shell32-220.ico", self.exit_app)

        # Right Toolbar [PyQt6.QtWidgets.QToolBar]
        self.rightbar = ToolBar(self, orientation=Qt.Orientation.Vertical,
                                style=Qt.ToolButtonStyle.ToolButtonIconOnly,
                                icon_size=(24, 24))

        # Right Toolbar Buttons
        self.rightbar.add_separator()
        self.rightbar.add_button(
            "Privacy", "resources/assets/icons/windows/shell32-167.ico", self.privacy_window)
        self.rightbar.add_button(
            "Settings", "resources/assets/icons/windows/shell32-315.ico", self.settings_window)

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.topbar)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.rightbar)

    def create_treeview(self) -> QTreeView:
        """
        Creates and adds the tree view widget to the main window.
        """
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())  # Set root path to the root of the file system

        treeview = QTreeView(self)
        treeview.setModel(self.model)
        treeview.setRootIndex(self.model.index(QDir.rootPath()))  # Display the file system

        treeview.setColumnWidth(0, 250)
        return treeview

    def create_edit(self) -> QTextEdit:
        """
        Creates and adds the QTextEdit widget to the main window.
        """
        return QTextEdit(self)

    def open_folder(self) -> None:
        """
        Event handler for the "Open" button. Opens a folder selection dialog and updates the tree view.
        """
        # Open the folder selection dialog
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")

        # Check if a folder is selected
        if folder_path:
            print(f"Selected Folder: {folder_path}")
            # Update the tree view to display the contents of the selected folder
            self.treeview.setRootIndex(self.model.index(folder_path))
        else:
            print("No folder selected.")

    def save_file(self) -> None:
        """
        Event handler for the "Save" button. Displays the "Save File" dialog.
        """
        print("Save")

    def exit_app(self) -> None:
        """
        Event handler for the "Exit" button. Closes the application.
        """
        self.close()

    def settings_window(self) -> None:
        """
        Event handler for the "Settings" button. Displays the "Settings" window.
        """
        print("settings_window")

    def privacy_window(self) -> None:
        """
        Event handler for the "Privacy" button. Displays the "Privacy" window.
        """
        print("privacy_window")


# Standard PyQt app initialization
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
