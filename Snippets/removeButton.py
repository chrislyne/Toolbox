import maya.cmds as cmds

def removeButton(shelfName,iconName):
    shelfButtons = cmds.shelfLayout(shelfName,q=True,childArray=True)

    for btn in shelfButtons:
        label = ''

        #Assert that this is a shelfButton
        if cmds.objectTypeUI(btn,isType='shelfButton'):

            label = cmds.shelfButton(btn,q=True,image=True)

            #If this button has the label we're looking for,
            #delete the button.
            if iconName == label:
                cmds.deleteUI(btn)
                
#removeButton('Toolbox','abc_reassignShaders.svg')