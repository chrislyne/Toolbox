import maya.cmds as cmds

sel = cmds.ls(sl=True)
for item in sel:
    objPivot = cmds.xform(item,q=True,piv=True,ws=True)
    groupName = item
    side = ''
    if item[-1] == 'L' or item[-1] == 'R':
        groupName = item.rsplit('_',1)[0]
        side = '_%s'%item.rsplit('_',1)[1]
        
    objGrp = cmds.group(item,n='%s%s_GRP'%(groupName,side))
    cmds.xform(objGrp,piv=[objPivot[0],objPivot[1],objPivot[2]],ws=True)
    
    