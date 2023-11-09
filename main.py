# main.py
from PyQt6.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6 import QtGui
from PyQt6.QtGui import QImage, QPixmap, QPainter
import sys
import pygame
from simulation import PhysarumSimulation
from config import Config

class ImageWidget(QWidget):
    def __init__(self,surface,parent=None):
        super(ImageWidget,self).__init__(parent)
        w=surface.get_width()
        h=surface.get_height()
        self.data=surface.get_buffer().raw
        self.image=QImage(self.data,w,h,QImage.Format.Format_RGB32)

    def paintEvent(self,event):
        qp=QtGui.QPainter()
        qp.begin(self)
        qp.drawImage(0,0,self.image)
        qp.end()

class SliderWidget(QWidget):
    def __init__(self,orientation,name,parent=None):
        super(SliderWidget,self).__init__(parent)
        self.name=name
        self.slider=QSlider(orientation)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.value_changed)
        self.label=QLabel(self.name)
        self.layout=QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)
        self.setLayout(self.layout)

    def value_changed(self,value):
        self.label.setText(self.name+": "+str(value))

class MainWindow(QMainWindow):
    def __init__(self, simulation, parent=None):
        super(MainWindow, self).__init__(parent)
        self.simulation = simulation
        self.image_widget = ImageWidget(simulation.renderer.window)
        self.setCentralWidget(self.image_widget)
        self.init_ui()

    def init_ui(self):
        self.slider_decay = SliderWidget(Qt.Orientation.Horizontal, "Decay")
        self.slider_diffusion = SliderWidget(Qt.Orientation.Horizontal, "Diffusion")

        # Set initial slider values based on simulation config
        self.slider_decay.slider.setValue(int(Config.DECAY * 100))
        self.slider_diffusion.slider.setValue(int(Config.DIFFUSION * 100))

        # Connect sliders to the simulation parameter update methods
        self.slider_decay.slider.valueChanged.connect(self.simulation.update_decay)
        self.slider_diffusion.slider.valueChanged.connect(self.simulation.update_diffusion)

        # Arrange widgets in the layout
        layout = QVBoxLayout()
        layout.addWidget(self.slider_decay)
        layout.addWidget(self.slider_diffusion)
        self.centralWidget().setLayout(layout)

        # Timer to update the Pygame simulation
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(1000 // Config.FRAMERATE)  # Update as per simulation frame rate

    def update_simulation(self):
        # Code to update simulation and Pygame display
        self.simulation.run_step()  
        self.image_widget.update()  # Refresh the PyQt6 widget displaying the Pygame surface


if __name__ == "__main__":
    pygame.init()
    simulation = PhysarumSimulation(Config.GRID_SIZE, Config.AGENT_COUNT, Config.FOOD_COUNT)

    app = QApplication(sys.argv)
    window = MainWindow(simulation)
    window.show()
    sys.exit(app.exec())


    

#  main.py :
# from simulation import PhysarumSimulation
# from config import Config


# if __name__ == "__main__":

#     simulation = PhysarumSimulation(Config.GRID_SIZE, Config.AGENT_COUNT, Config.FOOD_COUNT)
#     simulation.run()
