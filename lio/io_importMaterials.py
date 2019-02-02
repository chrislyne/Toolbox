import maya.cmds as cmds
import maya.mel as mel
import json

def processSelection():
    refs = []
    shapes = []
    
    grpSel = cmds.ls(sl=True)
    allDecending = cmds.listRelatives(grpSel,allDescendents=True,f=True )
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

def assignMaterials():
    materialData = processSelection()
    refs = materialData[0]
    shapes = materialData[1]

    IDOnShapes = []

    for shape in shapes:
        try:
            shapeID = cmds.getAttr('%s.IOID'%(shape))
            IDOnShapes.append([shape,shapeID])
        except:
            pass


    for ref in refs:
        materialSets = []
        materials = []
        project = cmds.workspace( q=True, directory=True, rd=True)
        JSONPath = project +'renderData/alembicShaders/%s/%s.json'%(ref,ref)
        with open(JSONPath) as data_file:    
                data = json.load(data_file)
                for obj in (data["shapes"]):
                    for objSet in IDOnShapes:
                        if obj["IOID"] in (objSet[1]):

                            for material in (obj["materials"]):
                                #print material.keys()[0]
                                
                                setName = '%s_%s'%(ref,material.keys()[0])
                                
                                for f in material.values()[0]:
                                    objSetf = '%s%s'%(objSet[0],f)
                                    try:
                                        cmds.sets(objSetf,add=setName)
                                    except:
                                        createSetResult = cmds.sets(em=True,name=setName)
                                        cmds.sets(objSetf,add=setName)
                                    
                                materialSets.append([setName,(material.keys()[0])])

        materialSets = [list(tupl) for tupl in {tuple(item) for item in materialSets }]         
        
        for m in materialSets:
            materialPath = project +'renderData/alembicShaders/%s/%s_%s.mb'%(ref,ref,m[1])
            cmds.file(materialPath,i=True,type='mayaBinary',ignoreVersion=True,mergeNamespacesOnClash=True,namespace=ref)
            materialName = '%s:%s'%(ref,m[1])
            try:
                cmds.sets(cmds.sets( m[0], q=True ),e=True,forceElement=materialName) 
            except:
                print 'failed to assign %s'%materialName
            #remove temporary sets
            cmds.delete( m[0])

#assignMaterials()      