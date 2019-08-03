from PySide2 import QtWidgets
import maya.cmds as cmds
import maya.OpenMayaUI as mui
import shiboken2
import baseIO.qtBase as qtBase
from random import randint
from random import uniform
import ramenRig.createCtrl as createCtrl
import ramenRig.createCtrl_resources

def randomColor():
    #randomise colours
    hue = randint(0,359)
    sat = uniform(0.5,1)
    val = 1 - sat + 0.5
    return[hue,sat,val]

def createNewCtrl(shape,shapeName,pos):
    #widget locations
    win = ctrlWindow.mainWidget

    newCtrl = createCtrl.MakeCtrlCurve()
    newCtrl.shape = shape
    newCtrl.ctrlName = shapeName
    newCtrl.ctrlColour = cmds.colorSliderGrp('ctrlColour',q=True,rgb=True)
    newCtrl.thickness = win.spinBox_lineThickness.value()
    newCtrl.scl = [win.doubleSpinBox.value(),win.doubleSpinBox.value(),win.doubleSpinBox.value()]
    newCtrl.pos = pos
    if win.radioButton_x.isChecked():
        newCtrl.rot = [0,90,0]
    if win.radioButton_y.isChecked():
        newCtrl.rot = [90,0,0]

    newCtrl.makeCtrl(newCtrl.makeShape())

def createBtn(shape):
    win = ctrlWindow.mainWidget
    sel = cmds.ls(sl=True)

    if sel:
        for o in sel:
            objPos2 = cmds.xform(o,q=True,t=True,ws=True)

            side = ''
            nameComboBox = win.comboBox_name.currentText()  
            if nameComboBox == 'Auto':
                if objPos2[0] > 0:
                    side = '_L'
                if objPos2[0] < 0:
                    side = '_R'
            elif nameComboBox != 'None':
                side = nameComboBox

            ctrlName = o
            if win.lineEdit_name.text():
                ctrlName = win.lineEdit_name.text()
            ctrlName = '%s_CTRL%s'%(ctrlName,side)

            createNewCtrl(shape,ctrlName,[objPos2[0],objPos2[1],objPos2[2]])
    else:
        side = ''
        nameComboBox = win.comboBox_name.currentText()  
        if nameComboBox != 'Auto' and nameComboBox != 'None':
            side = nameComboBox
        ctrlName = shape
        if win.lineEdit_name.text():
            ctrlName = win.lineEdit_name.text()
        ctrlName = '%s_CTRL%s'%(ctrlName,side)
        createNewCtrl(shape,ctrlName,[0,0,0])
        

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
    csg = cmds.colorSliderGrp('ctrlColour',hsvValue=randomColor())
    # Find a pointer to the paneLayout that we just created using Maya API
    ptr = mui.MQtUtil.findControl(paneLayoutName)
    # Wrap the pointer into a python QObject. Note that with PyQt QObject is needed. In Shiboken we use QWidget.
    paneLayoutQt = shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)
    # Now that we have a QtWidget, we add it to our Qt layout
    qtLayout.addWidget(paneLayoutQt)
    window.show(dockable=False)

    #connect buttons
    window.mainWidget.btn_circle.clicked.connect(lambda: createBtn('circle'))
    window.mainWidget.btn_square.clicked.connect(lambda: createBtn('square'))
    window.mainWidget.btn_star.clicked.connect(lambda: createBtn('star'))
    window.mainWidget.btn_diamond.clicked.connect(lambda: createBtn('diamond'))
    window.mainWidget.btn_plus.clicked.connect(lambda: createBtn('plus'))
    window.mainWidget.btn_cross.clicked.connect(lambda: createBtn('cross'))
    window.mainWidget.btn_arch.clicked.connect(lambda: createBtn('arch'))
    window.mainWidget.btn_pin.clicked.connect(lambda: createBtn('pin'))
    window.mainWidget.btn_arrow.clicked.connect(lambda: createBtn('arrow'))
    window.mainWidget.btn_doubleArrow.clicked.connect(lambda: createBtn('doubleArrow'))
    window.mainWidget.horizontalSlider_2.sliderMoved.connect(sizeSlider)
    window.mainWidget.doubleSpinBox.valueChanged.connect(sizeSpinbox)

    return window

ctrlWindow = createCTRL_ui()
