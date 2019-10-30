import maya.cmds as cmds

def removePasted(objs):
    for obj in objs:
        cleanObj = obj.replace("pasted__", "")
        if cleanObj != obj:
            cmds.rename(obj,cleanObj)

def heirachy(objs):
    allChildren = []
    for obj in sel:
    	children = cmds.listRelatives(allDescendents=True)
    	allChildren = allChildren + children
    
    allChildren = allChildren + sel
    allChildren = list(set(allChildren))
    allChildren.sort(key=len)
    return allChildren
    
mode = 1
sel = cmds.ls(sl=True)

if (mode == 1):
    sel = heirachy(sel)
#print sel
removePasted(sel)