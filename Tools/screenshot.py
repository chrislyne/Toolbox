import sys
import argparse
from PySide2 import QtWidgets, QtCore, QtUiTools, QtGui
import maya.OpenMayaUI as omui
import os
import baseIO as IO

class ScreenShot(QtWidgets.QWidget):

    global app
    app = QtWidgets.QApplication.instance()

    def __init__(self):
        super(ScreenShot, self).__init__()
        self.outPath = None
        screen_rect = app.desktop().screenGeometry()
        width, height = screen_rect.width()*2, screen_rect.height()
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle('Screen Capture')
        self.setCursor(QtCore.Qt.CrossCursor)
        self.setWindowOpacity(0.1)
        self.rubberband = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberband.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
        self.rubberband.show()
        QtWidgets.QWidget.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.rubberband.isVisible():
            self.rubberband.setGeometry(
                QtCore.QRect(self.origin, event.pos()).normalized())
        QtWidgets.QWidget.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self.rubberband.isVisible():
            self.rubberband.hide()
            selected = []
            rect = self.rubberband.geometry()
            desktop = QtWidgets.QApplication.instance().desktop()
            
            imgmap = QtGui.QPixmap.grabWindow(desktop.winId(), rect.x(), rect.y(), rect.width(), rect.height())
            imgmap.save(self.outPath)
            #sys.exit()
            self.destroy()
        QtWidgets.QWidget.mouseReleaseEvent(self, event)

    def launch(self, imagePath):
        self.outPath = imagePath
        f = imagePath.rsplit('/',1)[0]
        if not os.path.exists(f):
                os.makedirs(f)
        self.show()

'''
def takeScreenshot():

    global lch
    lch = screenshot.ScreenShot()

    imageFileName = '%s/.data/%s_thm.jpg'%(IO.getProj.sceneFolder(),IO.getProj.sceneName())
    lch.launch(imageFileName)


takeScreenshot()

'''



