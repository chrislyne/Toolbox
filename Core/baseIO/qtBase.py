import maya.OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore, QtUiTools
import os
import maya.cmds as cmds
import baseIO.getProj as getProj
import baseIO.sceneVar as sceneVar

def local_path():
    userDocs = os.path.expanduser('~/maya/prefs')
    return userDocs

def self_path():
    path = os.path.dirname(__file__)
    path = path.rsplit('\\',1)[0]
    #path = 'C:/Users/Chris/Dropbox/Projects/Qt'
    print path
    if not path:
        path = '.'
    return path

def GetMayaWindow():
    '''Get Main Maya Window'''
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtWidgets.QWidget)

def qtWindow(uiFilePath): 
        #load .ui file
        loader = QtUiTools.QUiLoader() 
        uifile = QtCore.QFile(uiFilePath) 
        uifile.open(QtCore.QFile.ReadOnly) 
        qt_widget = loader.load(uifile,None)
        #close .ui file
        uifile.close() 
        return qt_widget

class BaseWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    #set defaults
    _windowName = 'BaseUI'
    _windowTitle = 'Base UI'
    uiFile = ''
    
    def __init__(self,parent,uiFile):
        super(BaseWindow, self).__init__(parent)
        self.uiFile = uiFile

    def BuildUI(self):

        if cmds.window(self._windowName, exists=True):
            cmds.deleteUI(self._windowName)
        if cmds.window('%sWorkspaceControl'%self._windowName, exists=True):
            cmds.deleteUI('%sWorkspaceControl'%self._windowName)

        self.setObjectName(self._windowName)
        self.setWindowTitle(self._windowTitle)
        self.mainWidget = qtWindow('%s/%s'%(self_path(),self.uiFile))
        self.setCentralWidget(self.mainWidget)

class BaseWidget():
    uiFile = ''
    parent = ''
    def BuildUI(self):
        self.aWidget = qtWindow('%s/%s'%(self_path(),self.uiFile))
        self.parent.mainWidget.verticalLayout_3.addWidget(self.aWidget)