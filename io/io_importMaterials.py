import maya.cmds as cmds
import maya.mel as mel
import json

def findRefs():
    refs = []
    shapes = []
    
    grpSel = cmds.ls(sl=True)
    allDecending = cmds.listRelatives(grpSel,allDescendents=True )
    allDecendingShapes = cmds.ls(allDecending,s=True,l=True)
    for shape in allDecendingShapes:
        try:
            originRef = cmds.getAttr('%s.alembicName'%(shape))
            refs.append(originRef)
            shapes.append(shape)
        except:
            pass
    refs = list(set(refs))
    return (refs,shapes)

refs = findRefs()[0]
print refs

for ref in refs:

    project = cmds.workspace( q=True, directory=True, rd=True)
    JSONPath = project +'renderData/alembicShaders/%s/%s.json'%(ref,ref)
    with open(JSONPath) as data_file:    
            data = json.load(data_file)
            for obj in (data["shapes"]):
                print obj["IOID"]
                for material in (obj["materials"]):
                    print material.keys()[0]
                    print material.values()[0]
            
            
            
            
            
            
            
            