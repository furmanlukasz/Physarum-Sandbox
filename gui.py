from PyQt6.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6 import QtGui
from PyQt6.QtGui import QImage, QPixmap, QPainter

import pygame
import sys

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
    def __init__(self,surface,parent=None):
        super(MainWindow,self).__init__(parent)
        self.setCentralWidget(ImageWidget(surface))
        self.slider_decay=SliderWidget(Qt.Orientation.Horizontal,"Decay")
        self.slider_diffusion=SliderWidget(Qt.Orientation.Horizontal,"Diffusion")
        self.slider_decay.slider.setValue(50)
        self.slider_diffusion.slider.setValue(50)
        self.slider_decay.slider.valueChanged.connect(self.update_decay)
        self.slider_diffusion.slider.valueChanged.connect(self.update_diffusion)
        self.layout=QVBoxLayout()
        self.layout.addWidget(self.slider_decay)
        self.layout.addWidget(self.slider_diffusion)
        self.centralWidget().setLayout(self.layout)

    def update_decay(self,value):
        print("Decay: "+str(value))

    def update_diffusion(self,value):
        print("Diffusion: "+str(value))



pygame.init()
s=pygame.Surface((640,480))
s.fill((64,128,192,224))
pygame.draw.circle(s,(255,255,255,255),(100,100),50)

app=QApplication(sys.argv)
w=MainWindow(s)
w.show()
app.exec()