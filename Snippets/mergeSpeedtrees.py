import maya.cmds as cmds

sel = cmds.ls(sl=True)

newName = sel[0].split('|')[-1]
combinedMesh = cmds.polyUnite (sel[0], sel[1],mergeUVSets=True,centerPivot=True,n=newName)

vertCount =  cmds.polyEvaluate(combinedMesh,v=True )

cmds.polyMergeVertex('%s.vtx[0:%d]'%(combinedMesh[0],vertCount-1),am=True,ch=False,d=0.001)
cmds.delete(combinedMesh[0],ch=True) 
cmds.select(combinedMesh[0],r=True) 

