import maya.cmds as cmds
import baseIO.loadSave as IO
import baseIO.sceneVar as sceneVar
import baseIO.qtBase as qtBase
import baseIO.getProj as getProj
import baseIO.stringFormat as stringFormat
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore
import os

def setType(key,projectsDict):
    project = assetManagerUIWindow.mainWidget.project_comboBox.currentText()
    typePath = '%s/scenes/REF/%s'%(projectsDict[project]["projectPath"],key)

    print typePath
    assetFolders = []
    files = os.listdir(typePath)
    for name in files:
        if os.path.isdir(os.path.join(os.path.abspath(typePath), name)):
            #remove hidden folders
            if name[0] != '.':
                assetFolders.append(name)

    assetManagerUIWindow.mainWidget.listWidget_assets.clear()
    assetManagerUIWindow.mainWidget.listWidget_assets.addItems(assetFolders)


def setProject(key,projectsDict):
    projectPath = projectsDict[key]["projectPath"]

    assetTypeFolders = []
    path = '%s/scenes/REF/'%projectPath
    files = os.listdir(path)
    for name in files:
        if os.path.isdir(os.path.join(os.path.abspath(path), name)):
            #remove hidden folders
            if name[0] != '.':
                assetTypeFolders.append(name)
    #populate listWidget with folders
    assetManagerUIWindow.mainWidget.listWidget_assetType.clear()
    assetManagerUIWindow.mainWidget.listWidget_assetType.addItems(assetTypeFolders)

    #assetManagerUIWindow.mainWidget.listWidget_assetType.currentTextChanged.connect(lambda: setType(assetManagerUIWindow.mainWidget.listWidget_assetType.currentItem().text(),path))


def assetManagerUI():
    window = qtBase.BaseWindow(qtBase.GetMayaWindow(),'lm_assetManager.ui')
    window._windowTitle = 'Asset Manager'
    window._windowName = 'assetManager'
    window.pathModify = 'pipelime/'
    window.BuildUI()
    window.show(dockable=True)

    projectsDict = IO.loadDictionary('C:/Users/Admin/Documents/Toolbox/config/projects.json')
    print projectsDict

    projectLines = []
    for key in projectsDict:
        try:
            projectLines.append(key)
        except:
            pass

    try:
        buttonIcon = QtGui.QIcon("%s/icons/%s.svg"%(qtBase.self_path(), "multiRef"))
        window.mainWidget.pushButton_reference.setIcon(buttonIcon)
    except:
        pass
    try:
        buttonIcon = QtGui.QIcon("%s/icons/%s.svg"%(qtBase.self_path(), "parentShape"))
        window.mainWidget.pushButton_import.setIcon(buttonIcon)
    except:
        pass
    try:
        buttonIcon = QtGui.QIcon("%s/icons/%s.svg"%(qtBase.self_path(), "io_Llama"))
        window.mainWidget.pushButton_edit.setIcon(buttonIcon)
    except:
        pass

    window.mainWidget.project_comboBox.addItems(projectLines)
    window.mainWidget.project_comboBox.currentTextChanged.connect(lambda: setProject(window.mainWidget.project_comboBox.currentText(),projectsDict))

    window.mainWidget.listWidget_assetType.currentTextChanged.connect(lambda: setType(window.mainWidget.listWidget_assetType.currentItem().text(),projectsDict))

    try:
        buttonIcon = QtGui.QIcon("%s/icons/%s.jpg"%(qtBase.self_path(), "tap"))
        window.mainWidget.pushButton_thumb.setIcon(buttonIcon)
        window.mainWidget.pushButton_thumb.setText("")
    except:
        pass

    return window

assetManagerUIWindow = assetManagerUI()
#prefWidget 
#get render layers from scene
