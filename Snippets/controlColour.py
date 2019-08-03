import maya.cmds as cmds

ctrlColour = [0.4,0,0.2]

sel = cmds.ls(sl=True)
for c in sel:

    cmds.setAttr('%s.overrideEnabled'%c,1) 
    cmds.setAttr('%s.overrideRGBColors'%c,1) 
    cmds.setAttr('%s.overrideColorRGB'%c,ctrlColour[0],ctrlColour[1],ctrlColour[2])
    cmds.setAttr( '%s.lineWidth'%c,2)