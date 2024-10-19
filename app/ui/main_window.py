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
        self.setGeometry(100, 0, 800, 600)

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

        # Add a blank space (QTextEdit for demonstration, could be any widget)
        self.blank_space = QTextEdit(self)
        self.blank_space.setReadOnly(True)
        self.blank_space.setPlaceholderText("Blank Space Above Terminal")
        self.blank_space.setStyleSheet("background-color: lightgray;")  # Visual distinction
        self.blank_space.setFixedHeight(400)
        self.right_layout.addWidget(self.blank_space, stretch=4)  # Adjusted stretch for blank space
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

        # Initialize and start the command prompt
        self.process = QProcess()
        self.process.start("cmd.exe")
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.readyReadStandardError.connect(self.handle_error)

        # Run a command in the terminal at startup
        self.run_command_in_terminal("echo Welcome to the integrated terminal!\n")

    def closeEvent(self, event) -> None:
        """
        Overrides the close event to terminate the QProcess if it's running.
        """
        if self.process.state() == QProcess.ProcessState.Running:
            self.process.terminate()  # Safely terminate the process
            self.process.waitForFinished()  # Wait for the process to finish

        event.accept()  # Accept the event to close the window

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
        self.navbar.add_button("Open Folder", "resources/assets/icons/windows/imageres-10.ico", self.open_folder)

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

        # Capture user input from the terminal
        terminal.keyPressEvent = self.custom_keypress_event(terminal.keyPressEvent)

        return terminal

    def custom_keypress_event(self, original_keypress_event):
        """
        Captures key press events to allow the terminal to execute commands.
        """
        def new_keypress_event(event):
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                command = self.terminal.toPlainText().splitlines()[-1]
                self.send_command_to_process(command)  # Send command to the process
            original_keypress_event(event)
        return new_keypress_event

    def send_command_to_process(self, command: str) -> None:
        """
        Sends the command to the command prompt process.
        """
        command += "\n"  # Append newline to simulate Enter key
        self.process.write(command.encode())  # Write command to process

    def handle_output(self):
        """
        Handles output from the command prompt and appends it to the terminal widget.
        """
        data = self.process.readAllStandardOutput()
        self.terminal.append(data.data().decode())

    def handle_error(self):
        """
        Handles error output from the command prompt.
        """
        data = self.process.readAllStandardError()
        self.terminal.append(data.data().decode())

    def run_command_in_terminal(self, command: str) -> None:
        """
        Executes a system command and displays the output in the terminal widget.
        """
        try:
            # Execute the command and get the output
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Display the output in the terminal
            self.terminal.append(result.stdout)
            self.terminal.append(result.stderr)
        except Exception as e:
            self.terminal.append(f"Error running command: {str(e)}")

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
    window = MainWindow()
    window.show()
    sys.exit(app.exec())