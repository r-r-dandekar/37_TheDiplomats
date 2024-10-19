import sys
import os
import subprocess
from PyQt6.QtCore import QProcess, Qt, QDir
from PyQt6.QtGui import QTextOption
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QFileDialog,
    QTreeView, QApplication, QVBoxLayout,
    QTextEdit, QSizePolicy, QLabel
)
from PyQt6.QtGui import QFileSystemModel
from ..utils.config import AppConfig
from .widgets.menubar import MenuBar
from .widgets.toolbar import ToolBar
from .widgets.accordion import *
from ..utils.config import config
from ..logs import showlog
from PyQt6.QtGui import QTextOption, QIcon  # Added QIcon here



class MainWindow(QMainWindow):
    """
    MainWindow

    Args:
        QMainWindow  Inheritance
    """    # ... [existing code] ...

    def cut_text(self) -> None:
        """
        Cuts the selected text from the terminal.
        """
        cursor = self.terminal.textCursor()
        if cursor.hasSelection():
            cursor.removeSelectedText()
            cursor.clearSelection()
            self.terminal.setTextCursor(cursor)

    def create_new_folder(self) -> None:
        """
        Event handler for the "Create New Folder" button. 
        Creates a new folder in the currently selected directory in the tree view.
        """
        # Get the currently selected directory from the tree view
        current_index = self.treeview.currentIndex()
        if current_index.isValid():
            # Get the path of the selected directory
            folder_path = self.model.filePath(current_index)

            # Open a dialog to get the new folder name
            new_folder_name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:")
        
            if ok and new_folder_name:
                new_folder_path = os.path.join(folder_path, new_folder_name)
                try:
                    os.makedirs(new_folder_path)  # Create the new folder
                    print(f"Created New Folder: {new_folder_path}")
                    # Update the tree view to reflect the new folder
                    self.treeview.setRootIndex(self.model.index(folder_path))
                except Exception as e:
                    print(f"Error creating folder: {e}")
        else:
            print("No valid directory selected.")


    def copy_text(self) -> None:
        """
        Copies the selected text from the terminal to the clipboard.
        """
        cursor = self.terminal.textCursor()
        if cursor.hasSelection():
            clipboard = QApplication.clipboard()
            clipboard.setText(cursor.selectedText())

    def paste_text(self) -> None:
        """
        Pastes text from the clipboard into the terminal.
        """
        clipboard = QApplication.clipboard()
        self.terminal.insertPlainText(clipboard.text())


    

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

        # Create a vertical layout for the left panel
        self.left_layout = QVBoxLayout()  # New vertical layout for the left column

        # Create treeview container
        self.treeview_container = self.create_treeview_container()

        # Add the tree view container to the left layout
        self.left_layout.addWidget(self.treeview_container)  # Add tree view container

        # Create a container for the right panel (70% blank space above the terminal)
        self.right_container = QWidget(self)
        self.right_layout = QVBoxLayout(self.right_container)  # Vertical layout for the right side

        # Create the "Errors" navbar
        self.errors_navbar = QLabel("Errors", self)
        self.errors_navbar.setStyleSheet("background-color: darkred; color: white; font-weight: bold; font-size: 16px; padding: 5px;")  # Adjust font-size here
        self.errors_navbar.setFixedHeight(50)  # Set fixed height for the navbar to match the toolbar height
        self.right_layout.addWidget(self.errors_navbar)  # Add the errors navbar to the layout

        self.log_critical = AccordionSection("Critical", "Hello this is a test", 'red')    
        self.log_non_critical = AccordionSection("Non-Critical", "You can collapse this", 'orange')        
        self.log_info = AccordionSection("Information", "Just close this if you don't even want to see it...", 'green')        

        self.log_critical.show_list(["hi", 'BUE', "xrthi"])

        # Add a blank space (QTextEdit for demonstration, could be any widget)
        # self.blank_space = QTextEdit(self)
        # self.blank_space.setReadOnly(True)
        # self.blank_space.setPlaceholderText("Blank Space Above Terminal")
        # self.blank_space.setStyleSheet("background-color: lightgray;")  # Visual distinction
        # self.blank_space.setFixedHeight(400)
        self.right_layout.setContentsMargins(5,5,5,5)
        self.right_layout.setSpacing(3)
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.right_layout.addWidget(self.log_critical, stretch=4)  # Adjusted stretch for blank space
        self.right_layout.addWidget(self.log_non_critical, stretch=4)  # Adjusted stretch for blank space
        self.right_layout.addWidget(self.log_info, stretch=4)  # Adjusted stretch for blank space
        self.terminal = self.create_terminal()  # Create the terminal
        self.right_layout.addWidget(self.terminal, stretch=6)  # Adjusted stretch for terminal

        # Add the left layout and right container to the main layout
        layout.addLayout(self.left_layout)  # Add the left layout to the main layout
        layout.addWidget(self.right_container)  # Add right container to the main layout

        # Set margins and spacing to zero to eliminate gaps
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins around the main layout
        layout.setSpacing(0)  # Remove spacing between left and right columns

        # Create and add the menu bar
        self.setMenuBar(MenuBar(self))  # Pass the main window to MenuBar

    def create_treeview_container(self) -> QWidget:
        """
        Creates a container widget for the tree view and navigation bar.
        """
        container = QWidget(self)
        container.setMaximumWidth(250)
        v_layout = QVBoxLayout(container)  # Vertical layout for tree view and navbar

       # Create and add the navigation bar
        self.navbar = ToolBar(self, orientation=Qt.Orientation.Horizontal,
                      style=Qt.ToolButtonStyle.ToolButtonTextUnderIcon, icon_size=(18, 18))

        # Adding "Open Folder" button with an icon
        open_folder_icon = QIcon("resources/assets/icons/windows/folder.ico")
        self.navbar.add_button("Open Folder", open_folder_icon, self.open_folder)

        # Adding "Create New Folder" button with an icon
        new_folder_icon = QIcon("resources/assets/icons/windows/create-folder.ico")
        self.navbar.add_button("Create New Folder", new_folder_icon, self.create_new_folder)

        # Set the border for the toolbar
        self.navbar.setStyleSheet("QToolBar { border: 1px solid #cfcaca; padding: 5px; }")  # Adjust thickness and padding
        
        # Set the width of the toolbar to match the tree view
        self.navbar.setFixedWidth(250)  # Match the tree view width

        v_layout.addWidget(self.navbar)  # Add the navigation bar to the vertical layout

        # Create and add the tree view
        self.treeview = self.create_treeview()
        v_layout.addWidget(self.treeview)  # Add the tree view to the vertical layout

        container.setLayout(v_layout)
        return container

    def create_terminal(self) -> QTextEdit:
        """
        Creates a terminal widget using QTextEdit for displaying command outputs.
        """
        terminal = QTextEdit(self)
        terminal.setStyleSheet("background-color: black; color: white; font-family: Courier;")
        terminal.setReadOnly(False)  # Allows input for commands
        terminal.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        terminal.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        return terminal

    def create_treeview(self) -> QTreeView:
        """
        Creates and adds the tree view widget to the main window.
        """
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())  # Set root path to the root of the file system

        treeview = QTreeView(self)
        treeview.setModel(self.model)
        treeview.setRootIndex(self.model.index(QDir.rootPath()))  # Display the file system

        treeview.setFixedWidth(250)  # Set fixed width to 250 pixels
        treeview.setMinimumHeight(600)  # Ensure minimum height
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


# Standard PyQt app initialization
if __name__ == "__main__":
    app = QApplication(sys.argv)
    palette = app.palette()
    window = MainWindow()
    if palette.window().color().lightness() < 128:
        config['theme']='dark'
    window.show()
    sys.exit(app.exec())