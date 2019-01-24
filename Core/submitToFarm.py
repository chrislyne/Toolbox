import maya.cmds as cmds
import baseIO.loadSave as IO
import baseIO.sceneVar as sceneVar
import baseIO.qtBase as qtBase
import baseIO.getProj as getProj
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore
import subprocess
import os
import sys



class LayerWidget(qtBase.BaseWidget):

    layerWidgets = []
    previousValue = ''

    def __init__(self,layers,parentWindow):
        self.uiFile = 'submitToFarmWidget.ui'
        self.parent = parentWindow
        self.previousValue = parentWindow.mainWidget.prioritySlider.value()
        for l in layers:
            self.BuildUI()
            self.aWidget.checkBox_layerEnable.setText(l[0]) 
            self.aWidget.checkBox_layerEnable.setChecked(l[1]) 
            self.layerWidgets.append(self.aWidget)

            #read attributes from layer
            widgets = self.aWidget.findChildren(QtWidgets.QWidget)
            for w in widgets:
                try:
                    if w.parent() == self.aWidget:
                        value = cmds.getAttr('%s.%s'%(l[0],w.objectName()))
                        type = w.metaObject().className()
                        if type == 'QLineEdit':
                            w.setText(value)
                        if type == 'QComboBox':
                            w.setCurrentText(value)
                        if type == 'QSpinBox':
                            w.setValue(int(value))
                except:
                    pass
            
        #connect main controls to layer controls
        parentWindow.mainWidget.prioritySlider.valueChanged.connect(self.slide01)
        parentWindow.mainWidget.spinBox_packetSize.valueChanged.connect(self.packetSize)
        parentWindow.mainWidget.comboBox_pool.currentTextChanged.connect(self.pool)
        parentWindow.mainWidget.lineEdit_range.textChanged.connect(self.range)
        parentWindow.mainWidget.checkBox_enable.stateChanged.connect(self.enabled)
        height = 50*len(layers)
        parentWindow.mainWidget.scrollAreaWidgetContents.setMaximumHeight(height)
        parentWindow.mainWidget.scrollAreaWidgetContents.setMinimumHeight(height)

        
    #widget functions
    
    def slide01(self,value):
        difference = self.previousValue - value
        for layer in self.layerWidgets:
            #print addValue
            layer.layerPrioritySlider.setValue(layer.layerPrioritySlider.value()-difference)
        self.previousValue = value

    def packetSize(self,value):
        for layer in self.layerWidgets:
            layer.spinBox_layerPacketSize.setValue(value)
          
    def pool(self,value):
        for layer in self.layerWidgets:
            layer.comboBox_layerPool.setCurrentText(value)
    
    def range(self,value):
        for layer in self.layerWidgets:
            layer.lineEdit_layerRange.setText(value)
    
    def enabled(self,value):
        for layer in self.layerWidgets:
            layer.checkBox_layerEnable.setChecked(value)

    


def globalDict():
    #print 'global'
    prefData = []
    prefData.append(['window.mainWidget.lineEdit_render','setText','\'%s\''%window.mainWidget.lineEdit_render.text()])
    prefData.append(['window.mainWidget.lineEdit_submitExe','setText','\'%s\''%window.mainWidget.lineEdit_submitExe.text()])
    IO.writePrefsToFile(prefData,'%s/globalPrefs.json'%qtBase.self_path())

def projectDict():
    prefData = []
    prefData.append(['window.mainWidget.lineEdit_render','setText','\'%s\''%window.mainWidget.lineEdit_render.text()])
    prefData.append(['window.mainWidget.lineEdit_trelloBoard','setText','\'%s\''%window.mainWidget.lineEdit_trelloBoard.text()])
    IO.writePrefsToFile(prefData,'%s/data/projectPrefs.json'%getProj.getProject())

def localDict():
    prefData = []
    prefData.append(['window.mainWidget.lineEdit_name','setText','\'%s\''%window.mainWidget.lineEdit_name.text()])
    prefData.append(['window.mainWidget.lineEdit_slack','setText','\'%s\''%window.mainWidget.lineEdit_slack.text()])
    prefData.append(['window.mainWidget.checkBox_paused','setChecked',window.mainWidget.checkBox_paused.isChecked()])
    prefData.append(['window.mainWidget.prioritySlider','setValue',window.mainWidget.prioritySlider.value()])
    prefData.append(['window.mainWidget.comboBox_pool','setCurrentText','\'%s\''%window.mainWidget.comboBox_pool.currentText()])
    prefData.append(['window.mainWidget.spinBox_packetSize','setValue',window.mainWidget.spinBox_packetSize.value()])
    IO.writePrefsToFile(prefData,'%s/localPrefs.json'%qtBase.local_path())

def fileDict():
    prefData = []
    prefData.append(['window.mainWidget.prioritySlider','setValue',window.mainWidget.prioritySlider.value()])
    prefData.append(['window.mainWidget.lineEdit_range','setText','\'%s\''%window.mainWidget.lineEdit_range.text()])
    prefData.append(['window.mainWidget.lineEdit_note','setText','\'%s\''%window.mainWidget.lineEdit_note.text()])
    prefData.append(['window.mainWidget.spinBox_packetSize','setValue',window.mainWidget.spinBox_packetSize.value()])
    prefData.append(['window.mainWidget.comboBox_pool','setCurrentText','\'%s\''%window.mainWidget.comboBox_pool.currentText()])

    prefData.append(['img','imgpath','path'])
    prefData.append(['img','imgname','name'])
    prefData.append(['user','trelloID','name'])
    prefData.append(['user','trelloAddress','name'])
    prefData.append(['user','emailAddress','name'])
    prefData.append(['user','slackID','name'])

    IO.writePrefsToFile(prefData,'%s/data/%s.json'%(getProj.sceneFolder(),getProj.sceneName()))

#button functions
def selectSubmitExe():
    filename = QtWidgets.QFileDialog.getOpenFileName(filter='*.exe')
    window.mainWidget.lineEdit_submitExe.setText(filename[0])

def selectRenderExe():
    filename = QtWidgets.QFileDialog.getOpenFileName(filter='*.exe')
    window.mainWidget.lineEdit_render.setText(filename[0])

def submitButton():
    print 'submit'
    
    for l in layerWidget.layerWidgets:
        if l.checkBox_layerEnable.isChecked() == 1:
            widgets = l.findChildren(QtWidgets.QWidget)
            for w in widgets:
                try:
                    value = ''
                    type = w.metaObject().className()
                    if type == 'QLineEdit':
                        value = w.text()
                    if type == 'QComboBox':
                        value = w.currentText()
                    if type == 'QSpinBox':
                        value = w.value()
                    if value and w.parent() == l:
                        if cmds.attributeQuery(w.objectName(),node=l.checkBox_layerEnable.text(),ex=True) == False:
                            cmds.addAttr(l.checkBox_layerEnable.text(),ln=w.objectName(),dt='string')
                        cmds.setAttr('%s.%s'%(l.checkBox_layerEnable.text(),w.objectName()),value,type="string")       
                except:
                    pass

            #create string
            submitString = ''
            submitString += '%s '%window.mainWidget.lineEdit_submitExe.text()
            submitString += ' -Type Redshift for Maya'
            submitString += ' -Scene %s'%getProj.filepath()
            submitString += ' -Project %s'%getProj.getProject()
            submitString += ' -Name maya: %s (%s)'%(getProj.sceneName(),l.checkBox_layerEnable.text())
            submitString += ' -Extra \"-rl %s\"'%l.checkBox_layerEnable.text()
            submitString += ' -Priority %s'%l.layerPrioritySlider.value()
            submitString += ' -PacketSize %s'%l.spinBox_layerPacketSize.value()
            submitString += ' -Pool %s'%l.comboBox_layerPool.currentText()
            submitString += ' -Range %s'%l.lineEdit_layerRange.text()
            submitString += ' -Executable %s'%window.mainWidget.lineEdit_render.text()
            if window.mainWidget.checkBox_paused.isChecked() == 1:
                submitString += ' -Paused'
            submitString += ' -Creator %s'%window.mainWidget.lineEdit_name.text()
            submitString += ' -Note %s'%window.mainWidget.lineEdit_note.text()
            if window.mainWidget.checkBox_errors.isChecked() == 1:
                submitString += ' -DetectErrors 0'
            submitString += ' -CPUs 1 -GPUs 1 -RAM 0 -DistributeMode 0'
            send = subprocess.call(submitString,stdout=open(os.devnull, 'wb'))
            print submitString
            #Submit.exe Script -Type Redshift for Maya -Scene Z:/Job_2/Amstel/maya/scenes/RENDER/SH0040/SH0040_RENDER_v018_cl.mb -Project Z:/Job_2/Amstel/maya -im fooBar -Name maya: SH0040_RENDER_v018_cl "(rs_snow)" -Range 0-230 -PacketSize 8 -Priority 50 -Paused -Pool Redshift -Creator Chris -CPUs 1 -GPUs 1 -RAM 0 -Note  -Extra "-rl rs_snow" -DistributeMode 0
    #projectDict()
    localDict()
    fileDict()

def globalVariables():

    varibales = []
    gpus = 1

    return varibales

def setOptionsFromFile(f,window):
    try:
        data = IO.loadJSON(f)
        for o in data:
            oe = eval(o)
            type = oe.metaObject().className()
            try:
                for v in data[o]:
                    for i in v:
                        print i
                        #eval('%s.%s(%s)'%(o,i,v[i]))  
                        if type == 'QLineEdit':
                            oe.setText(v[i].strip('\''))
                        if type == 'QComboBox':
                            oe.setCurrentText(v[i].strip('\''))
                        if type == 'QSpinBox':
                            oe.setValue(v[i].strip('\''))
                        if type == 'QSlider':
                            oe.setValue(v[i].strip('\''))
                        if type == 'QCheckBox':
                            oe.setChecked(v[i].strip('\''))
            except:
                pass
    except:
        pass

def submitRenderUI():
    window = qtBase.BaseWindow(qtBase.GetMayaWindow(),'submitToFarm.ui')
    window._windowTitle = 'Submit to Farm'
    window._windowName = 'SubmitToFarm'
    window.BuildUI()
    window.show(dockable=True)
    #hide config panel 
    window.mainWidget.configPanel.setVisible(False)
    #connect buttons
    window.mainWidget.submitButton.clicked.connect(submitButton)
    window.mainWidget.pushButton_globals.clicked.connect(globalDict)
    window.mainWidget.pushButton_project.clicked.connect(projectDict)
    window.mainWidget.pushButton_user.clicked.connect(localDict)
    window.mainWidget.pushButton_render.clicked.connect(selectRenderExe)
    window.mainWidget.pushButton_submitExe.clicked.connect(selectSubmitExe)
    #icon on button
    buttonIcon = QtGui.QIcon("%s/icons/%s.png"%(os.path.dirname(__file__), "gear"))
    window.mainWidget.pushButton_settings.setIcon(buttonIcon)



    setOptionsFromFile('%s/globalPrefs.json'%qtBase.self_path(),window)
    setOptionsFromFile('%s/localPrefs.json'%qtBase.local_path(),window)
    setOptionsFromFile('%s/data/projectPrefs.json'%getProj.getProject(),window)
    window.mainWidget.lineEdit_range.setText('%s-%s'%(sceneVar.getStartFrame(),sceneVar.getEndFrame()))
    setOptionsFromFile('%s/data/%s.json'%(getProj.sceneFolder(),getProj.sceneName()),window)




    return window


window = submitRenderUI()

#get render layers from scene
layers = sceneVar.getRenderLayers()
layerWidget = LayerWidget(layers,window)
        







    

    

    










