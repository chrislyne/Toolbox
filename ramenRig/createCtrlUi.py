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
    shapeType = win.comboBox.currentText()


    newCtrl = createCtrl.MakeCtrlCurve()
    newCtrl.ctrlColour = [1,0,1]
    newCtrl.thickness = win.spinBox_lineThickness.value()
    newCtrl.scl = [win.doubleSpinBox.value(),win.doubleSpinBox.value(),win.doubleSpinBox.value()]
    if win.radioButton_x.isChecked():
        newCtrl.rot = [0,90,0]
    if win.radioButton_y.isChecked():
        newCtrl.rot = [90,0,0]
    if shapeType == 'Square':
        newCtrl.makeCtrl(newCtrl.makeSquare())
    if shapeType == 'Diamond':
        newCtrl.makeCtrl(newCtrl.makeDiamond())
    if shapeType == 'Plus':
        newCtrl.makeCtrl(newCtrl.makePlus())
    if shapeType == 'Star':
        newCtrl.makeCtrl(newCtrl.makeStar())
    if shapeType == 'Cross':
        newCtrl.makeCtrl(newCtrl.makeCross())
    if shapeType == 'Circle':
        newCtrl.makeCtrl(newCtrl.makeCircle())
    

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

    return window

ctrlWindow = createCTRL_ui()