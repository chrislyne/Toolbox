from PySide2 import QtWidgets
import maya.cmds as cmds
import maya.OpenMayaUI as mui
import shiboken2
import baseIO.qtBase as qtBase
from random import randint
from random import uniform
import ramenRig.createCtrl as createCtrl
import ramenRig.createCtrl_resources

def colourAtPoint(rampName,point):

    rampData = cmds.gradientControlNoAttr(rampName,q=True,asString=True)
    rampList = rampData.split(',')

    def channelGrad(channel,point):
        
        channelDict = {'R':0,'G':1,'B':2}
        channelInt = channelDict[channel]
        
        cmds.optionVar(stringValue=['tempRChannelOptVar', '%s,%s,1'%(rampList[channelInt],rampList[3])])
    
        positions = rampList[3::5]
        for i,c in enumerate(positions[1:]):
            cmds.optionVar(stringValueAppend=['tempRChannelOptVar', '%s,%s,1'%(rampList[channelInt::5][i+1],c)])
        
        tempGrad = cmds.gradientControlNoAttr(h=90,m=False)
        cmds.gradientControlNoAttr(tempGrad, e=True, optionVar='tempRChannelOptVar' )
        
        channelValue = cmds.gradientControlNoAttr(tempGrad, q=True, valueAtPoint=point )
        cmds.deleteUI(tempGrad, control=True )
        return channelValue
    
    R = channelGrad('R',point)
    G = channelGrad('G',point)
    B = channelGrad('B',point)
    
    return([R,G,B])

def randomColor():
    #randomise colours
    hue = randint(0,359)
    sat = uniform(0.5,1)
    val = 1 - sat + 0.5
    return[hue,sat,val]

def createNewCtrl(shape,shapeName,pos,pointOnRamp):
    #widget locations
    win = ctrlWindow.mainWidget

    newCtrl = createCtrl.MakeCtrlCurve()
    newCtrl.shape = shape
    newCtrl.ctrlName = shapeName
    newCtrl.ctrlColour = colourAtPoint('falloffCurve',pointOnRamp)
    #newCtrl.ctrlColour = cmds.colorSliderGrp('ctrlColour',q=True,rgb=True)
    newCtrl.thickness = win.spinBox_lineThickness.value()
    newCtrl.scl = [win.doubleSpinBox.value(),win.doubleSpinBox.value(),win.doubleSpinBox.value()]
    newCtrl.pos = pos
    if win.radioButton_x.isChecked():
        newCtrl.rot = [0,90,0]
        if win.radioButton_pointZ.isChecked():
            newCtrl.aim = [90,0,0]
    if win.radioButton_y.isChecked():
        newCtrl.rot = [90,0,0]
        if win.radioButton_pointX.isChecked():
            newCtrl.aim = [0,90,0]
    if win.radioButton_z.isChecked():
        newCtrl.rot = [0,0,0]
        if win.radioButton_pointX.isChecked():
            newCtrl.aim = [0,0,-90]

    ctrl = newCtrl.makeCtrl(newCtrl.makeShape())
    return ctrl

def createBtn(shape):
    win = ctrlWindow.mainWidget
    sel = cmds.ls(sl=True)

    ctrlNameInputText = win.lineEdit_name.text()
    ctrlNames = ctrlNameInputText.split(',')


    if sel and win.checkBox_selection.isChecked() == True:

        if len(sel) > 1:
            gradSplit = 1.0/float(len(sel)-1)
        else:
            gradSplit = 1
        for i,o in enumerate(sel):
            objPos2 = cmds.xform(o,q=True,t=True,ws=True)
            objRo = cmds.xform(o,q=True,ro=True,ws=True)

            side = ''
            nameComboBox = win.comboBox_name.currentText()  
            if nameComboBox == 'Auto':
                if objPos2[0] > 0:
                    side = '_L'
                if objPos2[0] < 0:
                    side = '_R'
            elif nameComboBox != 'None':
                side = nameComboBox

            ctrlName = o.split('_')[0]
            if len(ctrlNames[0])>0:
                ctrlName = ctrlNames[i % len(ctrlNames)]
            ctrlFullName = '%s_CTRL%s'%(ctrlName,side)
            if cmds.objExists(ctrlFullName):
                ctrlFullName = '%s_CTRL%s#'%(ctrlName,side)

            ctrl = createNewCtrl(shape,ctrlFullName,[objPos2[0],objPos2[1],objPos2[2]],gradSplit*i)
            if win.checkBox_group.isChecked():
                ctrlGrp = cmds.group(ctrl,n='%s_GRP'%(ctrl[0]))
                cmds.xform(ctrlGrp,piv=[objPos2[0],objPos2[1],objPos2[2]],ws=True)
                cmds.xform(ctrlGrp,ro=[objRo[0],objRo[1],objRo[2]],ws=True)
            if win.checkBox_constraint.isChecked():
                cmds.parentConstraint(ctrl,o,mo=True)
    else:
        side = ''
        nameComboBox = win.comboBox_name.currentText()  
        if nameComboBox != 'Auto' and nameComboBox != 'None':
            side = nameComboBox

        if len(ctrlNames[0]) == 0:
            ctrlNames = [shape]
        if len(ctrlNames) > 1:
            gradSplit = 1.0/float(len(ctrlNames)-1)
        else:
            gradSplit = 1
        for i,n in enumerate(ctrlNames):
            ctrlName = '%s_CTRL%s'%(n,side)
            if cmds.objExists(ctrlName):
                ctrlName = '%s_CTRL#%s'%(n,side)
            ctrl = createNewCtrl(shape,ctrlName,[0,0,0],gradSplit*i)
            if win.checkBox_group.isChecked():
                ctrlGrp = cmds.group(ctrl,n='%s_GRP'%(ctrl[0]))
                cmds.xform(ctrlGrp,piv=[0,0,0],ws=True)

        

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

def setRampCol():
    col = cmds.colorSliderGrp('ctrlColour',q=True,rgbValue=True)
    col00 = cmds.gradientControlNoAttr( 'falloffCurve',e=True,currentKeyColorValue=col)

def setColour():
    col00 = cmds.gradientControlNoAttr( 'falloffCurve',q=True,currentKeyColorValue=True)
    cmds.colorSliderGrp('ctrlColour',e=True,rgbValue=col00)

def createCTRL_ui():
    window = qtBase.BaseWindow(qtBase.GetMayaWindow(),'createCtrl.ui')
    window._windowTitle = 'Create CTRL Window'
    window._windowName = 'createCtrlWindow'
    window.pathModify = 'ramenRig/'
    window.BuildUI()
    #layout for color slider
    qtLayout = window.mainWidget.ctrlColorLayout
    paneLayoutName = cmds.columnLayout()
    # Create slider widget
    csg = cmds.colorSliderGrp('ctrlColour',hsvValue=randomColor(),cc='ramenRig.createCtrlUi.setRampCol()')
    rgbColour = cmds.colorSliderGrp('ctrlColour',q=True,rgbValue=True)
    cmds.optionVar(stringValue=['falloffCurveOptionVar', '1,1,1'])
    cmds.optionVar(stringValueAppend=['falloffCurveOptionVar', '1,0,1'])
    cmds.gradientControlNoAttr( 'falloffCurve', h=70,w=250,rac=True)
    cmds.gradientControlNoAttr( 'falloffCurve', e=True, optionVar='falloffCurveOptionVar',clv=rgbColour )
    cmds.gradientControlNoAttr( 'falloffCurve', e=True,currentKey=1,clv=rgbColour,cc='ramenRig.createCtrlUi.setColour()' )

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

def openCtrlWindow():
    global ctrlWindow
    ctrlWindow = createCTRL_ui()


#import ramenRig;ramenRig.createCtrlUi.openCtrlWindow()
