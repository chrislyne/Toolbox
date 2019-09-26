#extrude along a curve

#must specify a profile curve

import maya.cmds as cmds

profileCurve = 'nurbsCircle1'

sel = cmds.ls(sl=True)
for c in sel:
    shapes = cmds.listRelatives(c,s=True,path=True)
    curve0Pos = cmds.xform('%s.cv[0]'%shapes[0],q=True,t=True,ws=True) 
    curve1Pos = cmds.xform('%s.cv[1]'%shapes[0],q=True,t=True,ws=True) 
    
    newProfileCuve = cmds.duplicate(profileCurve)
    cmds.xform(newProfileCuve,t=curve0Pos,ws=True)
    
    aimPoint = cmds.spaceLocator(p=[0,0,0])
    cmds.xform(aimPoint,t=curve1Pos,ws=True)
    
    tempConstraint = cmds.aimConstraint(aimPoint,newProfileCuve,aimVector=[0,1,0],upVector=[0,1,0])
    
    cmds.delete(tempConstraint)
    cmds.delete(aimPoint)
    
    cmds.extrude(newProfileCuve,c,ch=True,rn=False,po=1,et=2,ucp=0,fpt=0,upn=1,rotation=0,scale=1,rsp=1)  

