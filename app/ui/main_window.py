import sys
import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QTreeView, QApplication
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

        # Main layout
        layout = QHBoxLayout(central_widget)
        central_widget.setLayout(layout)

        # Create Widgets
        self.treeview_container = self.create_treeview_container()  # Create a container for tree view and nav bar
        self.vbox_container = self.create_vbox_container()  # Create a vertical box layout container

        # Create and add the menu bar
        self.setMenuBar(MenuBar(self))  # Pass the main window to MenuBar

        # Add Widgets to Layout
        layout.addWidget(self.treeview_container)
        layout.addLayout(self.vbox_container, stretch=1)

    def create_treeview_container(self) -> QWidget:
        """
        Creates a container widget for the tree view and navigation bar.
        """
        container = QWidget(self)
        v_layout = QVBoxLayout(container)  # Vertical layout for tree view and navbar

        # Create and add the navigation bar
        self.navbar = ToolBar(self, orientation=Qt.Orientation.Horizontal,
                          style=Qt.ToolButtonStyle.ToolButtonTextUnderIcon, icon_size=(18, 18))
        self.navbar.add_button("Open Folder", "resources/assets/icons/windows/imageres-10.ico", self.open_folder)
    
        # Set the border for the toolbar
        self.navbar.setStyleSheet("QToolBar { border: 1px solid #cfcaca; padding: 5px; }")  # Adjust thickness and padding

        v_layout.addWidget(self.navbar)  # Add the navigation bar to the vertical layout

        # Create and add the tree view
        self.treeview = self.create_treeview()
        v_layout.addWidget(self.treeview)  # Add the tree view to the vertical layout

        container.setLayout(v_layout)
        return container

    def create_vbox_container(self) -> QVBoxLayout:
        """
        Creates a vertical box layout to be added to the main window.
        """
        vbox = QVBoxLayout()

        # Add your widgets to the vbox layout here if needed.
        # Example placeholder widgets could be added here:
        # label = QLabel("Placeholder Widget", self)
        # vbox.addWidget(label)

        return vbox

    def create_toolbars(self) -> None:
        """
        Creates and adds the toolbars to the main window.
        """
        # Right Toolbar
        self.rightbar = ToolBar(self, orientation=Qt.Orientation.Vertical,
                                style=Qt.ToolButtonStyle.ToolButtonIconOnly,
                                icon_size=(24, 24))

        # Right Toolbar Buttons
        self.rightbar.add_separator()
        self.rightbar.add_button(
            "Privacy", "resources/assets/icons/windows/shell32-167.ico", self.privacy_window)
        self.rightbar.add_button(
            "Settings", "resources/assets/icons/windows/shell32-315.ico", self.settings_window)

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

        treeview.setFixedWidth(250)        # Set fixed width to 250 pixels
        treeview.setMinimumHeight(600)  
        treeview.setColumnWidth(0, 250)
        return treeview

    def open_folder(self) -> None:
        """
        Event handler for the "Open Folder" button. Opens a folder selection dialog and updates the tree view.
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
