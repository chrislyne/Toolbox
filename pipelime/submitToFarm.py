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
        self.pathModify = 'pipelime/'
        self.parent = parentWindow.mainWidget.verticalLayout_3
        self.previousValue = parentWindow.mainWidget.prioritySlider.value()
        for l in layers:
            self.BuildUI()
            self.aWidget.checkBox_layerEnable.setText(l[0]) 
            self.aWidget.checkBox_layerEnable.setChecked(l[1]) 
            self.layerWidgets.append(self.aWidget)
            #set attributes from global controls
            self.aWidget.spinBox_layerPacketSize.setValue(parentWindow.mainWidget.spinBox_packetSize.value())
            #set pools from global pools
            allPools = [parentWindow.mainWidget.comboBox_pool.itemText(i) for i in range(parentWindow.mainWidget.comboBox_pool.count())]
            self.aWidget.comboBox_layerPool.clear()
            self.aWidget.comboBox_layerPool.addItems(allPools)
            self.aWidget.comboBox_layerPool.setCurrentText(parentWindow.mainWidget.comboBox_pool.currentText())
            self.aWidget.lineEdit_layerRange.setText(parentWindow.mainWidget.lineEdit_range.text())
            self.aWidget.layerPrioritySlider.setValue(parentWindow.mainWidget.prioritySlider.value())
            
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

def listCameras():
    #list renderable cameras
    cameraSel = cmds.ls(type=('camera'), l=True)
    renderableCameras = []
    for cam in cameraSel:
        if cmds.getAttr("%s.renderable"%cam) == 1:
            renderableCameras.append(cam)
    return renderableCameras

def fetchPools():
    #use submit path to get poolManager 
    submitPath = stf_window.mainWidget.lineEdit_submitExe.text()
    updatePools = submitPath.replace('submit.exe','PoolManager list NAME')
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    upd = subprocess.check_output(updatePools, startupinfo=si)
    pools = (upd.replace('\r','')).split('\n')
    pools = filter(None, pools)
    prefData = []
    prefData.append(['pools','value','\'%s\''%pools])
    IO.writePrefsToFile(prefData,'%s/config/globalPrefs.json'%qtBase.self_path())
    stf_window.mainWidget.comboBox_pool.addItems(pools)
    for l in layerWidget.layerWidgets:
        l.comboBox_layerPool.addItems(pools)
    #return pools

def globalDict():
    prefData = []
    prefData.append(['pathToRenderExe','value','\'%s\''%stf_window.mainWidget.lineEdit_render.text()])
    prefData.append(['pathToSubmitExe','value','\'%s\''%stf_window.mainWidget.lineEdit_submitExe.text()])
    IO.writePrefsToFile(prefData,'%s/config/globalPrefs.json'%qtBase.self_path())

def projectDict():
    prefData = []
    prefData.append(['pathToRenderExe','value','\'%s\''%stf_window.mainWidget.lineEdit_render.text()])
    prefData.append(['trelloBoard','value','\'%s\''%stf_window.mainWidget.lineEdit_trelloBoard.text()])
    IO.writePrefsToFile(prefData,'%s/data/projectPrefs.json'%getProj.getProject())

def localDict():
    prefData = []
    prefData.append(['userName','value','\'%s\''%stf_window.mainWidget.lineEdit_name.text()])
    prefData.append(['userSlackID','value','\'%s\''%stf_window.mainWidget.lineEdit_slack.text()])
    prefData.append(['checkBox_Paused','value',stf_window.mainWidget.checkBox_paused.isChecked()])
    prefData.append(['prioritySlider','value',stf_window.mainWidget.prioritySlider.value()])
    prefData.append(['comboBox_pool','value','\'%s\''%stf_window.mainWidget.comboBox_pool.currentText()])
    prefData.append(['spinBox_packetSize','value',stf_window.mainWidget.spinBox_packetSize.value()])
    IO.writePrefsToFile(prefData,'%s/localPrefs.json'%qtBase.local_path())

def fileDict():
    prefData = []
    prefData.append(['prioritySlider','value',stf_window.mainWidget.prioritySlider.value()])
    prefData.append(['comboBox_pool','value','\'%s\''%stf_window.mainWidget.comboBox_pool.currentText()])
    prefData.append(['spinBox_packetSize','value',stf_window.mainWidget.spinBox_packetSize.value()])
    prefData.append(['staggerStart','value',stf_window.mainWidget.lineEdit_stagger.text()])

    versionlessSceneName = ''.join([c for c in getProj.sceneName() if c not in "1234567890"])
    IO.writePrefsToFile(prefData,'%s/.data/%s.json'%(getProj.sceneFolder(),versionlessSceneName))

def layerDict(l):
    prefData = []
    #get image path for the render layer
    rendeFilePath = cmds.renderSettings(fin=True,fp=True,cts=True,lyr=l)
    path = rendeFilePath[0].rsplit('/',1)[0]
    filename = rendeFilePath[0].split('/')[-1]

    prefData.append(['img','imgpath','%s/'%path])
    prefData.append(['img','imgname',filename])
    prefData.append(['user','trelloID','name'])
    prefData.append(['user','trelloAddress','name'])
    prefData.append(['user','name',stf_window.mainWidget.lineEdit_name.text()])
    prefData.append(['user','slackID',stf_window.mainWidget.lineEdit_slack.text()])

    IO.writePrefsToFile(prefData,'%s/.data/%s.%s.json'%(getProj.sceneFolder(),getProj.sceneName(),l))

#button functions
def selectSubmitExe():
    filename = QtWidgets.QFileDialog.getOpenFileName(filter='*.exe')
    stf_window.mainWidget.lineEdit_submitExe.setText(filename[0])

def selectRenderExe():
    filename = QtWidgets.QFileDialog.getOpenFileName(filter='*.exe')
    stf_window.mainWidget.lineEdit_render.setText(filename[0])

def submitButton():

    #progress bar
    countActiveLayers = 0
    for l in layerWidget.layerWidgets:
        if l.checkBox_layerEnable.isChecked() == 1:
            countActiveLayers +=1
    if stf_window.mainWidget.checkBox_paused.isChecked() == 0:
        countActiveLayers *=2
    countActiveLayers +=2
    progressWindow = cmds.window(title='Submit Progress')
    cmds.columnLayout(adjustableColumn=True)
    progressControl = cmds.progressBar(maxValue=countActiveLayers, width=500,height=40)
    progressLabel = cmds.text( label='',width=100,height=40,align='center')
    cmds.showWindow( progressWindow )

    #save file
    cmds.text(progressLabel, edit=True, label='Saving File')
    cmds.file(save=True)
    cmds.progressBar(progressControl, edit=True, step=1)

    updateStrings = []

    #loop through layers in layerWidget
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
            submitString += '%s Script '%stf_window.mainWidget.lineEdit_submitExe.text()
            submitString += ' -Type Redshift for Maya'
            submitString += ' -Scene %s'%getProj.filepath()
            submitString += ' -Project %s'%getProj.getProject()
            submitString += ' -Name maya: %s (%s)'%(getProj.sceneName(),l.checkBox_layerEnable.text())
            submitString += ' -Extra \"-rl %s\"'%l.checkBox_layerEnable.text()
            submitString += ' -Priority %s'%l.layerPrioritySlider.value()
            submitString += ' -PacketSize %s'%l.spinBox_layerPacketSize.value()
            submitString += ' -Pool %s'%l.comboBox_layerPool.currentText()
            submitString += ' -Range %s'%l.lineEdit_layerRange.text()
            submitString += ' -Executable %s'%stf_window.mainWidget.lineEdit_render.text()
            submitString += ' -Paused'
            submitString += ' -Creator %s'%stf_window.mainWidget.lineEdit_name.text()
            submitString += ' -StaggerStart %s'%stf_window.mainWidget.lineEdit_stagger.text()
            submitString += ' -Note %s'%stf_window.mainWidget.lineEdit_note.text()
            if stf_window.mainWidget.checkBox.isChecked() == 1:
                width = cmds.getAttr("defaultResolution.width")/2
                height = cmds.getAttr("defaultResolution.height")/2
                submitString += ' -Extra \"-x %s -y %s -preRender \"setAttr \\\"redshiftOptions.unifiedMaxSamples\\\" 16; setAttr \\\"redshiftOptions.unifiedMinSamples\\\" 4;\"\"'%(width,height)
            if stf_window.mainWidget.checkBox_errors.isChecked() == 1:
                submitString += ' -DetectErrors 0'
            submitString += ' -CPUs -1 -GPUs 1 -RAM -1 -DistributeMode 0 -StaggerCount 1 -StaggerMode 1'
            try:
            	#que the files paused
                #send = subprocess.check_output(submitString, stdin=None, stderr=None, shell=False)
                cmds.text(progressLabel, edit=True, label='Submitting Layer - %s'%l.checkBox_layerEnable.text())
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                send = subprocess.check_output(submitString, startupinfo=si)
                jobID = send.rsplit(' ',1)[-1]
                jobID = jobID.replace('\n', '').replace('\r', '')
                updateString = submitString.replace("-Paused","-ID %s"%jobID)
                updateStrings.append(updateString) 
                cmds.progressBar(progressControl, edit=True, step=1)
                
            except:
                print 'failed to submit, check path to submit.exe exists'
            print submitString
            layerDict(l.checkBox_layerEnable.text())
    
    #save file with added metadata
    cmds.text(progressLabel, edit=True, label='Writing Metadata')
    cmds.file(save=True)
    cmds.progressBar(progressControl, edit=True, step=1)

    if stf_window.mainWidget.checkBox_paused.isChecked() == 0:
        for updateLayer in updateStrings:
            cmds.text(progressLabel, edit=True, label='Updating Layer Status')
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.check_output(updateLayer, startupinfo=si)
            cmds.progressBar(progressControl, edit=True, step=1)
    cmds.text(progressLabel, edit=True, label='DONE!')
    #projectDict()
    localDict()
    fileDict()

def setUiValue(uiObject,value,window):

    type = uiObject.metaObject().className()

    if type == 'QLineEdit':
        uiObject.setText(value["value"].strip('\''))
    if type == 'QComboBox':
        uiObject.setCurrentText(value["value"].strip('\''))
    if type == 'QSpinBox':
        uiObject.setValue(value["value"])
    if type == 'QSlider':
        uiObject.setValue(value["value"])
    if type == 'QCheckBox':
        uiObject.setChecked(value["value"].strip('\''))


def setOptions(data,window):

    UIinputs = [
                    [window.mainWidget.lineEdit_render,"pathToRenderExe"],
                    [window.mainWidget.lineEdit_submitExe,"pathToSubmitExe"],
                    [window.mainWidget.lineEdit_trelloBoard,"trelloBoard"],
                    [window.mainWidget.lineEdit_name,"userName"],
                    [window.mainWidget.lineEdit_slack,"userSlackID"],
                    [window.mainWidget.checkBox_paused,"checkBox_Paused"],
                    [window.mainWidget.prioritySlider,"prioritySlider"],
                    [window.mainWidget.comboBox_pool,"comboBox_pool"],
                    [window.mainWidget.spinBox_packetSize,"spinBox_packetSize"],
                    [window.mainWidget.lineEdit_range,"lineEdit_range"],
                    [window.mainWidget.lineEdit_stagger,"staggerStart"]
                ]
    for d in UIinputs:
        try:
            setUiValue(d[0],data[d[1]],window)
        except:
            pass

def mergeDictionaries(dict1,dict2):
    try:
        dict1.update(dict2)
    except:
        pass
    return dict1

def submitRenderUI():
    stf_window = qtBase.BaseWindow(qtBase.GetMayaWindow(),'submitToFarm.ui')
    stf_window._windowTitle = 'Submit to Farm'
    stf_window._windowName = 'SubmitToFarm'
    stf_window.pathModify = 'pipelime/'
    stf_window.BuildUI()
    stf_window.show(dockable=True)
    #hide config panel 
    stf_window.mainWidget.configPanel.setVisible(False)
    #connect buttons
    stf_window.mainWidget.submitButton.clicked.connect(submitButton)
    stf_window.mainWidget.pushButton_globals.clicked.connect(globalDict)
    stf_window.mainWidget.pushButton_pools.clicked.connect(fetchPools)
    stf_window.mainWidget.pushButton_project.clicked.connect(projectDict)
    stf_window.mainWidget.pushButton_user.clicked.connect(localDict)
    stf_window.mainWidget.pushButton_render.clicked.connect(selectRenderExe)
    stf_window.mainWidget.pushButton_submitExe.clicked.connect(selectSubmitExe)
    #icon on button
    try:
        buttonIcon = QtGui.QIcon("%s/icons/%s.png"%(qtBase.self_path(), "gear"))
        stf_window.mainWidget.pushButton_settings.setIcon(buttonIcon)
    except:
        pass
    #merge all dictionaries into one
    comboDict = {}
    comboDict = mergeDictionaries(comboDict,IO.loadDictionary('%s/config/globalPrefs.json'%qtBase.self_path()))
    comboDict = mergeDictionaries(comboDict,IO.loadDictionary('%s/data/projectPrefs.json'%getProj.getProject()))
    comboDict = mergeDictionaries(comboDict,IO.loadDictionary('%s/localPrefs.json'%qtBase.local_path()))
    rangeFromTimeline =  '%s-%s'%(sceneVar.getStartFrame(),sceneVar.getEndFrame())
    comboDict = mergeDictionaries(comboDict,{"lineEdit_range": {"value":rangeFromTimeline}})
    versionlessSceneName = ''.join([c for c in getProj.sceneName() if c not in "1234567890"])
    comboDict = mergeDictionaries(comboDict,IO.loadDictionary('%s/.data/%s.json'%(getProj.sceneFolder(),versionlessSceneName)))
    #populate pool comboBox from /config/globalPrefs.json
    try:
        poolsList = ((comboDict["pools"]["value"])[2:-2]).replace('\'','').split(',')
        stf_window.mainWidget.comboBox_pool.addItems(poolsList)
    except:
        pass

    setOptions(comboDict,stf_window)
    return stf_window


def openSubmitWindow():

    try:
        del stf_window
        del layers
        del layerWidget
    except:
        pass

    global stf_window
    global layers
    global layerWidget

    stf_window = submitRenderUI()
    #get render layers from scene
    layers = sceneVar.getRenderLayers()
    layerWidget = LayerWidget(layers,stf_window)


#import pipelime.submitToFarm as submitToFarm
#submitToFarm.openSubmitWindow()

#openSubmitWindow()