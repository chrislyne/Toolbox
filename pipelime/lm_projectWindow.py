import maya.cmds as cmds
import baseIO.loadSave as IO
import baseIO.sceneVar as sceneVar
import baseIO.qtBase as qtBase
import baseIO.getProj as getProj
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
        varients.append(v.variant_lineEdit.text())

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
    
    folderStructureDict = IO.loadDictionary('C:/Users/Admin/Documents/Toolbox/pipelime/lm_folderStructure.json')

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
                    sourcePath = 'C:/Users/Admin/Documents/Toolbox/pipelime/files'
                    sourceFile = '%s/%s'%(sourcePath,i["source"])
                    destFile = '%s/%s/%s'%(projectRoot,i["dest"],i["source"])
                    shutil.copyfile(sourceFile, destFile)
            except:
                pass

    #loop through variants
    


def removeWidget():
    print 'delete'

def addButton():
    bwidget = VariantWidget(lm_projectWin)

class VariantWidget(qtBase.BaseWidget):

    layerWidgets = []

    def __init__(self,parentWindow):
        self.uiFile = 'lm_projectWidget.ui'
        self.parent = parentWindow.mainWidget.VariantsLayout
        self.BuildUI()
        #self.aWidget.label.setText(l[0]) 
        #self.aWidget.lineEdit.setText(l[1]) 
        self.layerWidgets.append(self.aWidget)

        self.aWidget.delete_pushButton.clicked.connect(removeWidget)

def lm_projectWindow():
    window = qtBase.BaseWindow(qtBase.GetMayaWindow(),'lm_projectWindow.ui')
    window._windowTitle = 'Create New Project'
    window._windowName = 'createNewProject'
    window.BuildUI()
    window.show(dockable=True)
    #connect buttons
    window.mainWidget.variant_pushButton.clicked.connect(addButton)
    window.mainWidget.create_pushButton.clicked.connect(createButton)

    

    folderStructureDict = IO.loadDictionary('C:/Users/Admin/Documents/Toolbox/pipelime/lm_folderStructure.json')
    list1 = folderStructureDict["root"]
    window.mainWidget.comboBox_root.clear()
    window.mainWidget.comboBox_root.addItems(list1)

    return window


lm_projectWin = lm_projectWindow()
bwidget = VariantWidget(lm_projectWin)

