import maya.cmds as cmds

sel = cmds.ls(sl=True)
for item in sel:
    if cmds.attributeQuery('IKaimObject', n=str(item), ex=True):
        connected = cmds.listConnections('%s.IKaimObject'%item,d=False, s=True)
        axis = cmds.getAttr('%s.IK_aimAxis'%sel[0])
        tempAim = cmds.aimConstraint(connected[0],item,offset=[0,0,0],weight=1,aimVector=[axis[0][0],axis[0][2],axis[0][2]],upVector=[0,1,0],worldUpVector=[0,1,0])
        cmds.delete(tempAim[0])
        
    if cmds.attributeQuery('IKConstaintObject', n=str(item), ex=True):
        connectedParent = cmds.listConnections('%s.IKConstaintObject'%item,d=False, s=True)
        tempParent = cmds.parentConstraint( connectedParent[0], item )
        cmds.delete(tempParent[0])
    


################################################
##tag ctrl as fk 
##select ctrl first followed by IK joint to aim to
import maya.cmds as cmds
 
sel = ls(sl=True)
if not cmds.attributeQuery('IKaimObject', n=str(sel[0]), ex=True):
    cmds.addAttr('%s'%sel[0],ln="IKaimObject",dt="string")
    
cmds.connectAttr('%s.message'%sel[1],'%s.IKaimObject'%sel[0],f=True)

if not cmds.attributeQuery('IK_aimAxis', n=str(sel[0]), ex=True):
    cmds.addAttr('%s'%sel[0],ln="IK_aimAxis",at="double3")
    cmds.addAttr('%s'%sel[0],ln="IK_aimAxisX",at="double",p="IK_aimAxis")
    cmds.addAttr('%s'%sel[0],ln="IK_aimAxisY",at="double",p="IK_aimAxis")
    cmds.addAttr('%s'%sel[0],ln="IK_aimAxisZ",at="double",p="IK_aimAxis")
