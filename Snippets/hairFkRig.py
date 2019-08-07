import maya.cmds as cmds

sel = cmds.ls(sl=True)

hairControls = []
hairGrps = []
hairJoints = []
for i,c in enumerate(sel):
    curvePos = cmds.xform(c,q=True,piv=True,ws=True)
    curveGrp = cmds.group(c,n='%s_GRP'%c)
    cmds.xform(curveGrp,piv=[curvePos[0],curvePos[1],curvePos[2]],ws=True)
    hairGrps.append(curveGrp)
    cmds.select(cl=True)
    if hairJoints:
        cmds.select(hairJoints[-1])
    
    newJoint = cmds.joint(p=[curvePos[0],curvePos[1],curvePos[2]],n='%s_joint%s'%(c.split('_')[0],i))
    hairJoints.append(newJoint)
    
for i,j in enumerate(hairJoints):
    cmds.joint(j,e=True,oj='xzy',secondaryAxisOrient='zup',zso=True)
    jRo = cmds.xform(j,q=True,ro=True,ws=True)
    print jRo
    cmds.xform(hairGrps[i],ro=jRo,ws=True)
    
for i,c in enumerate(sel):
    cmds.xform(c,ro=[0,0,0],ws=True)
    cmds.makeIdentity(c,apply=True,r=True,s=True)
    cmds.parentConstraint(c,hairJoints[i],mo=True)
    
for i,g in enumerate(hairGrps):
    if i > 0:
        cmds.parent(g,sel[i-1])
    