import maya.cmds as cmds
import baseIO.loadSave as IO
import baseIO.sceneVar as sceneVar
import baseIO.qtBase as qtBase
import baseIO.getProj as getProj
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore

class LayerWidget(qtBase.BaseWidget):

    layerWidgets = []

    def __init__(self,layers,parentWindow):
        self.uiFile = 'projectConfigWidget.ui'
        self.parent = parentWindow
        for l in layers:
            self.BuildUI()
            self.aWidget.label.setText(l[0]) 
            self.aWidget.lineEdit.setText(l[1]) 
            self.layerWidgets.append(self.aWidget)

def submitButton():
    prefData = []
    for l in prefWidget.layerWidgets:

        prefData.append([l.label.text(),'value','%s'%l.lineEdit.text()])
    IO.writePrefsToFile(prefData,'%s/data/projectPrefs.json'%getProj.getProject())

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


def mergeDictionaries(dict1,dict2):
    try:
        dict1.update(dict2)
    except:
        pass
    return dict1

def submitRenderUI():
    window = qtBase.BaseWindow(qtBase.GetMayaWindow(),'projectConfig.ui')
    window._windowTitle = 'Configure Project'
    window._windowName = 'configureProject'
    window.BuildUI()
    window.show(dockable=True)
    #connect buttons
    window.mainWidget.pushButton_accept.clicked.connect(submitButton)

    #merge all dictionaries into one
    comboDict = {}
    comboDict = mergeDictionaries(comboDict,IO.loadDictionary('%s/globalPrefs.json'%qtBase.self_path()))
    comboDict = mergeDictionaries(comboDict,IO.loadDictionary('%s/data/projectPrefs.json'%getProj.getProject()))

    lines = []
    for key in comboDict:
        try:
            lines.append([key,comboDict[key]["value"]])
        except:
            pass
    #layers = sceneVar.getRenderLayers()
    global prefWidget
    prefWidget = LayerWidget(lines,window)
    return window


window = submitRenderUI()
prefWidget 
#get render layers from scene
