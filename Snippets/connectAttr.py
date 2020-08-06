import maya.cmds as cmds

sel = cmds.ls(sl=True)

cmds.connectAttr("%s.translate"%sel[0],"%s.translate"%sel[1],f=True)
cmds.connectAttr("%s.rotate"%sel[0],"%s.rotate"%sel[1],f=True)
cmds.connectAttr("%s.scale"%sel[0],"%s.scale"%sel[1],f=True)
try:
	cmds.connectAttr("%s.follow"%sel[0],"%s.follow"%sel[1],f=True)
except:
	pass