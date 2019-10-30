import maya.cmds as cmds

loctor = 'locator7'
direction = -1
axis = 0

sel = cmds.ls(sl=True)

for obj in sel:
    worldPos = cmds.xform(obj,q=True,piv=True,ws=True)
    cond = cmds.shadingNode('condition',asUtility=True)
    cmds.setAttr( "%s.secondTerm"%cond,worldPos[axis])
    if direction == 1:
        cmds.setAttr ('%s.operation'%cond,2)
    else:
        cmds.setAttr ('%s.operation'%cond,4)
    cmds.connectAttr('%s.outColorR'%cond,'%s.visibility'%obj,f=True)
    axisDirection = 'translateX'
    if axis == 1:
        axisDirection = 'translateY'
    if axis == 2:
        axisDirection = 'translateZ'
    cmds.connectAttr('%s.translate.%s'%(loctor,axisDirection),'%s.firstTerm'%cond,f=True)
    