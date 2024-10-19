import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QWidget, QVBoxLayout

class PieChart(QWidget):
        def __init__(self):
            super().__init__()
            self.figure, self.ax = plt.subplots()  # Create a figure and axes
            self.canvas = FigureCanvas(self.figure)  # Create a canvas to display the figure

            # Set the layout for the PieChart widget
            layout = QVBoxLayout()
            layout.addWidget(self.canvas)
            self.setLayout(layout)

            # Initial data (empty)
            self.data = [0, 0, 0]  # [Critical, Non-Critical, Info]
            self.labels = ['Critical', 'Non-Critical', 'Information']
            self.colors = ['red', 'orange', 'green']  # Default colors
            self.update_chart()  # Initial chart

        def update_chart(self):
            self.ax.clear()  # Clear the previous chart

            # Only draw the chart if there are counts to display
            if any(self.data):
                self.ax.pie(self.data, labels=self.labels, autopct='%1.1f%%', startangle=90, colors=self.colors)  # Use self.colors here
                self.ax.axis('equal')  # Equal aspect ratio ensures pie chart is circular
            else:
                self.ax.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=16)

            self.canvas.draw()  # Refresh the canvas

