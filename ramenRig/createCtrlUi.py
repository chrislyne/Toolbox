from PySide2 import QtWidgets
import maya.cmds as cmds
import maya.OpenMayaUI as mui
import shiboken2
import baseIO.qtBase as qtBase
from random import randint
from random import uniform
import ramenRig.createCtrl as createCtrl

def randomColor():
    #randomise colours
    hue = randint(0,359)
    sat = uniform(0.5,1)
    val = 1 - sat + 0.5
    return[hue,sat,val]

def createBtn():
    win = ctrlWindow.mainWidget

    
    newCtrl = createCtrl.MakeCtrlCurve()
    newCtrl.shape = win.comboBox.currentText()
    newCtrl.ctrlColour = [1,0,1]
    newCtrl.thickness = win.spinBox_lineThickness.value()
    newCtrl.scl = [win.doubleSpinBox.value(),win.doubleSpinBox.value(),win.doubleSpinBox.value()]
    if win.radioButton_x.isChecked():
        newCtrl.rot = [0,90,0]
    if win.radioButton_y.isChecked():
        newCtrl.rot = [90,0,0]

    newCtrl.makeCtrl(newCtrl.makeShape())

def sizeSlider(val):
    win = ctrlWindow.mainWidget
    win.doubleSpinBox.setValue(float(val)*0.1)

def sizeSpinbox(val):
    win = ctrlWindow.mainWidget
    #increase range of slider if needed
    sliderMax = win.horizontalSlider_2.maximum()
    if int(val*10) > sliderMax:
        win.horizontalSlider_2.setMaximum(int(val*20))
    win.horizontalSlider_2.setValue(int(val*10))

def createCTRL_ui():
    window = qtBase.BaseWindow(qtBase.GetMayaWindow(),'createCtrl.ui')
    window._windowTitle = 'Create CTRL Window'
    window._windowName = 'createCtrlWindow'
    window.pathModify = 'ramenRig/'
    window.BuildUI()
    #layout for color slider
    qtLayout = window.mainWidget.ctrlColorLayout
    paneLayoutName = cmds.paneLayout()
    # Create slider widget
    csg = cmds.colorSliderGrp(hsvValue=randomColor())
    # Find a pointer to the paneLayout that we just created using Maya API
    ptr = mui.MQtUtil.findControl(paneLayoutName)
    # Wrap the pointer into a python QObject. Note that with PyQt QObject is needed. In Shiboken we use QWidget.
    paneLayoutQt = shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)
    # Now that we have a QtWidget, we add it to our Qt layout
    qtLayout.addWidget(paneLayoutQt)
    window.show(dockable=False)

    #connect buttons
    window.mainWidget.pushButton_newCtrl.clicked.connect(createBtn)
    window.mainWidget.horizontalSlider_2.sliderMoved.connect(sizeSlider)
    window.mainWidget.doubleSpinBox.valueChanged.connect(sizeSpinbox)

    return window

ctrlWindow = createCTRL_ui()