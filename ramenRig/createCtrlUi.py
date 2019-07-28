import baseIO.qtBase as qtBase
from PySide2.QtWidgets import QColorDialog
from PySide2.QtGui import QColor
from random import randint

def createCTRL_ui():
    window = qtBase.BaseWindow(qtBase.GetMayaWindow(),'createCTRL.ui')
    window._windowTitle = 'Create CTRL Window'
    window._windowName = 'crateCtrlWindow'
    window.pathModify = 'ramenRig/'
    window.BuildUI()
    window.show(dockable=False)

def colourDialog():
    #randomise colours
    hue = randint(0,359)
    sat = randint(128,255)
    val = 255 - sat + 128
    #open dialog
    newColor = QColorDialog.getColor(title='Colour Foo',initial=QColor.fromHsv(hue,sat,val))
    return newColor.getRgb()

createCTRL_ui()