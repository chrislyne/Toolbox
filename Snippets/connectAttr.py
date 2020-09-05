import maya.cmds as cmds

sel = cmds.ls(sl=True)

for s in sel:
    
    ctrlNode = s
    connectionNode = s.replace("CTRL", "connection")

    cmds.connectAttr("%s.translate"%ctrlNode,"%s.translate"%connectionNode,f=True)
    cmds.connectAttr("%s.rotate"%ctrlNode,"%s.rotate"%connectionNode,f=True)
    cmds.connectAttr("%s.scale"%ctrlNode,"%s.scale"%connectionNode,f=True)
    try:
    	cmds.connectAttr("%s.follow"%ctrlNode,"%s.follow"%connectionNode,f=True)
    except:
    	pass
    try:
    	cmds.connectAttr("%s.topLipWeight"%ctrlNode,"%s.topLipWeight"%connectionNode,f=True)
    except:
    	pass
	