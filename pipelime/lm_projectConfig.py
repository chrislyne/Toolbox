import maya.cmds as cmds
import baseIO.loadSave as IO
import baseIO.sceneVar as sceneVar
import baseIO.qtBase as qtBase
import baseIO.getProj as getProj
import baseIO.stringFormat as stringFormat
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore


class LayerWidget(qtBase.BaseWidget):

    layerWidgets = []

    def __init__(self,layers,parentWindow):
        self.uiFile = 'lm_projectConfigWidget.ui'
        self.pathModify = 'pipelime/'
        self.parent = parentWindow
        for l in layers:
            try:
                self.BuildUI()
                #prefName = stringFormat.convertCamel(l[0])
                self.aWidget.label.setText(l[0]) 
                
                self.aWidget.lineEdit.setText(str(l[1])) 
                self.layerWidgets.append(self.aWidget)
            except:
                pass
            

def submitButton():
    prefData = []
    for l in prefWidget.layerWidgets:

        prefData.append([l.label.text(),'value','%s'%l.lineEdit.text()])
    IO.writePrefsToFile(prefData,'%s/data/projectPrefs.json'%getProj.getProject())

def setUiValue(uiObject,value,prefConfigUIWindow):

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


def mergeDictionaries(dict1,dict2):
    try:
        dict1.update(dict2)
    except:
        pass
    return dict1

def prefConfigUI():
    window = qtBase.BaseWindow(qtBase.GetMayaWindow(),'lm_projectConfig.ui')
    window._windowTitle = 'Configure Project'
    window._windowName = 'configureProject'
    window.pathModify = 'pipelime/'
    window.BuildUI()
    window.show(dockable=True)
    #connect buttons
    window.mainWidget.pushButton_accept.clicked.connect(submitButton)

    #merge all dictionaries into one
    comboDict = {"userName": {"value": ""},"userInitials": {"value": ""},"userSlackID": {"value": "@"}}
    #comboDict = mergeDictionaries(comboDict,IO.loadDictionary('C:/Users/Admin/Documents/Toolbox/config/globalPrefs.json'))
    comboDict = mergeDictionaries(comboDict,IO.loadDictionary('%s/localPrefs.json'%qtBase.local_path()))
    projectDict = IO.loadDictionary('%s/../.projectData/projectPrefs.json'%getProj.getProject())
    print projectDict

    projectLines = []
    for key in projectDict:
        try:
            projectLines.append([key,projectDict[key]["value"]])
        except:
            pass

    lines = []
    for key in comboDict:
        try:
            lines.append([key,comboDict[key]["value"]])
        except:
            pass
    #layers = sceneVar.getRenderLayers()
    global prefWidget
    prefWidget = LayerWidget(lines,window.mainWidget.verticalLayout_user)
    global projectPrefsWidget
    prefWidget = LayerWidget(projectLines,window.mainWidget.verticalLayout_project)
    global globalPrefsWidget
    prefWidget = LayerWidget(lines,window.mainWidget.verticalLayout_global)
    return window


prefConfigUIWindow = prefConfigUI()
#prefWidget 
#get render layers from scene
