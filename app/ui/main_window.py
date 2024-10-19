import threading
import sys
import os
import subprocess
from .widgets.pie_chart import PieChart
from PyQt6.QtCore import QProcess, Qt, QDir, QModelIndex
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
from ..logs import showlogs as logs_showlogs
from .chatbot_tab import ChatbotTab
from PyQt6.QtGui import QTextOption, QIcon  # Added QIcon here
import queue


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

        self.result_queue = queue.Queue()

        # Window-Settings
        self.setWindowTitle(AppConfig.APP_NAME)
        self.setGeometry(100, 100, 600, 200)

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

        # Create the "logs" navbar
        self.navbar = QWidget()
        self.navbar.setStyleSheet("background-color: #333333; color: white; font-weight: bold; font-size: 16px; padding: 5px;")  # Adjust font-size here
        self.navbar.setFixedHeight(40)
        self.logs_button = QPushButton("Errors Log Info", self)
        self.logs_button.setFlat(True)
        self.logs_button.setCheckable(True)
        self.logs_button.setChecked(True)
        self.logs_button.clicked.connect(self.click_logs_tab)
        self.logs_button.setStyleSheet("background-color: #4d4d4d; color: white; font-weight: bold; font-size: 16px; padding: 5px;")  # Adjust font-size here
        self.chatbot_button = QPushButton("Chatbot", self)
        self.chatbot_button.setFlat(True)
        self.chatbot_button.setCheckable(True)
        self.chatbot_button.clicked.connect(self.click_chatbot_tab)
        self.chatbot_button.setStyleSheet("background-color: #4d4d4d; color: white; font-weight: bold; font-size: 16px; padding: 5px;")  # Adjust font-size here
        navbar_layout = QHBoxLayout()
        navbar_layout.addWidget(self.logs_button)
        navbar_layout.addWidget(self.chatbot_button)
        navbar_layout.setContentsMargins(0,0,0,0)
        navbar_layout.setSpacing(0)
        self.navbar.setLayout(navbar_layout)
        self.right_layout.addWidget(self.navbar)
        
        self.right_layout.setContentsMargins(0,0,0,0)
        self.right_layout.setSpacing(0)
        
        self.logs_widget = QWidget()
        logs_widget_layout = QVBoxLayout()
        self.logs_widget.setLayout(logs_widget_layout)
        
        self.chatbot_widget = ChatbotTab()

        self.log_critical = AccordionSection("Critical", self, 'red')    
        self.log_non_critical = AccordionSection("Non-Critical", self, 'orange')        
        self.log_info = AccordionSection("Information", self, 'green')        

        logs_widget_layout.setContentsMargins(5,5,5,5)
        logs_widget_layout.setSpacing(3)
        logs_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        logs_widget_layout.addWidget(self.log_critical, stretch=4)
        logs_widget_layout.addWidget(self.log_non_critical, stretch=4)  
        logs_widget_layout.addWidget(self.log_info, stretch=4)

        # Create a spacer to push the pie chart frame to the bottom
        spacer = QWidget()  # Create a spacer widget
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Set it to expand
        logs_widget_layout.addWidget(spacer)  # Add the spacer to the layout

        # Create a box (QFrame) at the bottom for the pie chart
        # After creating the pie chart frame
        self.pie_chart_frame = QFrame(self.logs_widget)
        self.pie_chart_frame.setStyleSheet("background-color: #f0f0f0; border: 1px solid #cccccc;")
        self.pie_chart_frame.setFixedHeight(400)  # Set the height for the pie chart area

        self.pie_chart_frame_layout = QVBoxLayout(self.pie_chart_frame)  # Create a layout for the pie chart frame
        # Add the pie chart frame to the bottom of the logs widget layout
        logs_widget_layout.addWidget(self.pie_chart_frame, stretch=2)  # You can adjust the stretch factor

            # Create the PieChart instance and add it to the pie chart frame
        self.pie_chart = PieChart()  # Create an instance of the PieChart
        self.pie_chart.colors = ['Red', 'orange', 'green']  # Set specific colors for each section        self.pie_chart_frame_layout = QVBoxLayout(self.pie_chart_frame)  # Create a layout for the pie chart frame
        self.pie_chart_frame_layout.addWidget(self.pie_chart)  # Add the pie chart to the layout

        
        self.right_layout.addWidget(self.logs_widget)
        self.tab="logs"

        # Add the left layout and right container to the main layout
        layout.addLayout(self.left_layout)  # Add the left layout to the main layout
        layout.addWidget(self.right_container)  # Add right container to the main layout

        # Set margins and spacing to zero to eliminate gaps
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins around the main layout
        layout.setSpacing(0)  # Remove spacing between left and right columns

        # Create and add the menu bar
        self.setMenuBar(MenuBar(self))  # Pass the main window to MenuBar
    
    def click_logs_tab(self):
        self.chatbot_button.setChecked(False)
        if self.tab != "logs":
            self.right_layout.addWidget(self.logs_widget)
            self.right_layout.removeWidget(self.chatbot_widget)
            self.chatbot_widget.setParent(None)
            self.tab="logs"

    def click_chatbot_tab(self):
        self.logs_button.setChecked(False)
        if self.tab != "chatbot":
            self.right_layout.addWidget(self.chatbot_widget)
            self.right_layout.removeWidget(self.logs_widget)
            self.logs_widget.setParent(None)
            self.tab="chatbot"

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
        self.treeview.clicked.connect(self.showlogs)
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
        treeview.setMinimumHeight(400)  # Ensure minimum height
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

    def remove_all_widgets(self, layout):
        # Iterate over the layout items and remove them
        while layout.count():
            widget = layout.itemAt(0).widget()     # Get the first widget
            if widget is not None:                    # Check if widget is valid
                widget.deleteLater()                  # Safely delete the widget
            layout.removeItem(layout.itemAt(0)) 
        
    def showlogs(self, index: QModelIndex):
        file_path = self.model.filePath(index)
        critical, non_critical, info = sortlogs(file_path)

        self.log_critical.show_list(critical)
        self.log_non_critical.show_list(non_critical)
        self.log_info.show_list(info)

        # Update the pie chart data based on the log counts
        self.pie_chart.data = [len(critical), len(non_critical), len(info)]  # Update the data
        self.pie_chart.update_chart()  # Refresh the pie chart




# Standard PyQt app initialization
if __name__ == "__main__":
    app = QApplication(sys.argv)
    palette = app.palette()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
