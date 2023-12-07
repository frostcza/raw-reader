# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsPixmapItem, QGraphicsScene, QFileDialog

from raw_viewer_ui import Ui_Form
from qt_material import apply_stylesheet

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import glob

import numpy as np


class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        
        extra = {'font_family': 'Times New Roman', 'font_size': 20}
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        path_css = os.path.abspath(os.path.join(bundle_dir, 'custom.css'))
        apply_stylesheet(app, 'light_blue.xml', invert_secondary=True, extra=extra, css_file=path_css)
        
        path_ico = os.path.abspath(os.path.join(bundle_dir, 'viewer.ico'))
        self.setWindowIcon(QIcon(path_ico))
        
        self.pushButton_4.clicked.connect(self.control_open)
        self.pushButton.clicked.connect(self.control_prev)
        self.pushButton_2.clicked.connect(self.control_next)
        self.pushButton_3.clicked.connect(self.control_exit)
        
        self.row = 480
        self.col = 640
        self.channel = 1
        
        self.index = -1
        self.file_count = 0
        
    def show_next_image(self, foward=1):
        self.index = self.index + foward
        self.label.setText("filename: " + os.path.basename(self.file_name_list[self.index]))
        
        image = np.fromfile(self.file_name_list[self.index], dtype='uint16')
        image = image.reshape(self.row, self.col, self.channel)
        
        minval = np.min(np.min(image))
        maxval = np.max(np.max(image))
        target = 255.0 * (image.astype(np.float32) - minval) / (maxval - minval)
        target = target.astype(np.uint8)

        frame = QtGui.QImage(target, self.col, self.row, QtGui.QImage.Format_Grayscale8)
        pix = QtGui.QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)
        self.scene = QGraphicsScene()
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)
        
    def control_open(self):
        self.source_image_path = 'E:/FLIR A700/python/spinnaker_python/Examples/my_demo/images/'
        self.source_image_path = QFileDialog.getExistingDirectory(self, "select a folder", "./")
        self.source_image_path = self.source_image_path + '/'
        
        self.file_count = len(glob.glob(self.source_image_path + "*.raw"))
        if self.file_count == 0:
            self.index = -1
            self.scene = QGraphicsScene()
            self.graphicsView.setScene(self.scene)
            self.label.setText("filename")
            return
        
        self.file_name_list = sorted(glob.glob(self.source_image_path + "*.raw"), key=lambda name: name[:-4])
        self.index = -1
        self.show_next_image(1)
    
    def control_prev(self):
        if self.index > 0:
            self.show_next_image(-1)
    
    def control_next(self):
        if self.index < self.file_count-1:
            self.show_next_image(1)
        
    def control_exit(self):
        app.quit()
        self.close()
    
    def closeEvent(self, event):
        app.quit()
        self.close()
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())