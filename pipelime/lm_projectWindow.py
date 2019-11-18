import baseIO.qtBase as qtBase
import baseIO.loadSave as loadSave
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore
import os
import shutil


def makeFolders(folderNames):
    for f in folderNames:
        if not os.path.exists(f):
            os.makedirs(f)

def createButton():
    folderNames = []

    varients = []
    
    for v in bwidget.layerWidgets:
        try:
            if not v.isHidden():
                varients.append(v.variant_lineEdit.text())
        except:
            pass
    if not varients:
        varients = ['']


    parentFolder = lm_projectWin.mainWidget.comboBox_root.currentText()
    clientName = lm_projectWin.mainWidget.lineEdit_client.text()
    projectName = lm_projectWin.mainWidget.lineEdit_project.text()

    projectRoot = '%s/untitledProject'%(parentFolder)

    if clientName and projectName:
        projectRoot = '%s/%s_%s'%(parentFolder,clientName,projectName)
    elif clientName:
        projectRoot = '%s/%s'%(parentFolder,clientName)
    elif projectName:
        projectRoot = '%s/%s'%(parentFolder,projectName)
    
    folderStructureDict = loadSave.loadDictionary('%s/pipelime/lm_folderStructure.json'%qtBase.self_path())

    #create general folders
    for i in folderStructureDict["general"]["folders"]:
        folderNames.append('%s/%s'%(projectRoot,i))

    #perform options
    checkBoxes = [[lm_projectWin.mainWidget.checkBox_3D,'3D'],[lm_projectWin.mainWidget.checkBox_anim,'anim'],[lm_projectWin.mainWidget.checkBox_FX,'FX'],[lm_projectWin.mainWidget.checkBox_track,'tracking'],[lm_projectWin.mainWidget.checkBox_2D,'2D Animation'],[lm_projectWin.mainWidget.checkBox_render,'render'],[lm_projectWin.mainWidget.checkBox_comp,'Comp'],[lm_projectWin.mainWidget.checkBox_edit,'Edit'],[lm_projectWin.mainWidget.checkBox_live,'Live action'],[lm_projectWin.mainWidget.checkBox_board,'Storyboard'],[lm_projectWin.mainWidget.checkBox_matte,'Matte Painting']]
    for c in checkBoxes:
        if c[0].isChecked() == 1:
            #create folders
            for i in folderStructureDict["options"][c[1]]["folders"]:
                if '<var>' not in i:
                    folderNames.append('%s/%s'%(projectRoot,i))
                else:
                    for v in varients:
                        vi = i.replace('<var>', v)
                        folderNames.append('%s/%s'%(projectRoot,vi))

    #make all of the folders
    makeFolders(folderNames)

    for c in checkBoxes:
        if c[0].isChecked() == 1:
            #copy files
            try:
                for i in folderStructureDict["options"][c[1]]["files"]:
                    sourcePath = '%s/pipelime/files'%qtBase.self_path()
                    sourceFile = '%s/%s'%(sourcePath,i["source"])
                    destFile = '%s/%s/%s'%(projectRoot,i["dest"],i["source"])
                    sourceFile = os.path.realpath(sourceFile)
                    destFile = os.path.realpath(destFile)
                    shutil.copyfile(sourceFile, destFile)
            except:
                pass

    #set prefs for project
    projectDict('%s/.projectData'%projectRoot)

    #open window
    path=os.path.realpath(projectRoot)
    os.startfile(path)

def deleteWidget(self):
        self.aWidget.hide()

def addButton():
    bwidget = VariantWidget(lm_projectWin)

class VariantWidget(qtBase.BaseWidget):

    layerWidgets = []

    def __init__(self,parentWindow):
        self.uiFile = 'lm_projectWidget.ui'
        self.uiFilePath = qtBase.self_path()
        #self.uiFilePath = 'C:/Users/Admin/Documents/Toolbox'
        self.pathModify = 'pipelime/'
        self.parent = parentWindow.mainWidget.VariantsLayout
        self.BuildUI()
        self.layerWidgets.append(self.aWidget)

        self.aWidget.delete_pushButton.clicked.connect(lambda: deleteWidget(self))

def resolutionChange(text):
    folderStructureDict = loadSave.loadDictionary('%s/pipelime/lm_folderStructure.json'%qtBase.self_path())
    lm_projectWin.mainWidget.lineEdit_resW.setText(folderStructureDict["settings"]["resolution"][text][0])
    lm_projectWin.mainWidget.lineEdit_resH.setText(folderStructureDict["settings"]["resolution"][text][1])

def projectDict(folder):
    prefData = []
    prefData.append(['frameRate','value','%s'%lm_projectWin.mainWidget.comboBox_frameRate.currentText()])
    prefData.append(['resolutionW','value','%s'%lm_projectWin.mainWidget.lineEdit_resW.text()])
    prefData.append(['resolutionH','value','%s'%lm_projectWin.mainWidget.lineEdit_resH.text()])
    loadSave.writePrefsToFile(prefData,'%s/projectPrefs.json'%folder)
    

def lm_projectWindow():
    window = qtBase.BaseWindow(qtBase.GetMayaWindow(),'lm_projectWindow.ui')
    window._windowTitle = 'Create New Project'
    window._windowName = 'createNewProject'
    #self.uiFilePath = 'C:/Users/Admin/Documents/Toolbox'
    window.pathModify = 'pipelime/'
    window.BuildUI()
    window.show(dockable=True)
    #connect buttons
    window.mainWidget.variant_pushButton.clicked.connect(addButton)
    window.mainWidget.create_pushButton.clicked.connect(createButton)

    folderStructureDict = loadSave.loadDictionary('%s/pipelime/lm_folderStructure.json'%qtBase.self_path())
    rootFolders = folderStructureDict["root"]
    window.mainWidget.comboBox_root.clear()
    window.mainWidget.comboBox_root.addItems(rootFolders)

    resolutions = folderStructureDict["settings"]["resolution"]
    window.mainWidget.comboBox_resolution.clear()
    window.mainWidget.comboBox_resolution.addItems(resolutions.keys())

    window.mainWidget.comboBox_resolution.currentTextChanged.connect(resolutionChange)

    return window

def openProjectWindow():
    global lm_projectWin
    global bwidget
    lm_projectWin = lm_projectWindow()
    bwidget = VariantWidget(lm_projectWin)


#import pipelime.lm_projectWindow as lm_projectWindow
#lm_projectWindow.openProjectWindow()


#openProjectWindow()