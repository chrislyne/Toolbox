def getNodeClassType(nodeType):
    #get type of node 
    #nodeType = cmds.nodeType(node)
    nodeClass = ''
    #list of shading nodes
    nodeClasses = ['utility','shader','texture']
    #find type of class
    for c in nodeClasses:
        if cmds.getClassification(nodeType,satisfies=c):
            nodeClass = c
    
    return nodeClass

def listShadingNodes(objects):
    #list ALL of the objects shape nodes
    allShapes = []
    for o in objects:
        shapes = cmds.listRelatives( o, allDescendents=True,type='shape')
        allShapes += shapes
    
    for shape in allShapes:
        #find connected shading networks
        con = cmds.listConnections( shape, scn=True, type='shadingEngine' )
        #remove duplicate materials  
        allMaterials = []
        allConnections = []
        allNodes = list(set(con))
        #add objects back into the list while it's being iterated 
        for m in allNodes:
            materials = cmds.listConnections( m, source=True,scn=True,destination=False,plugs=True)
            
            if materials:
                for matConnection in materials:
                    mat = matConnection.split('.')[0]
                    #add recursive shading nodes to the list
                    nodeType = cmds.nodeType(mat)
                    nodeClass = getNodeClassType(nodeType)
                    if any(nodeClass in s for s in ['utility','shader','texture']) and nodeClass:
                        allNodes.append(mat)
                        destinations = cmds.connectionInfo(matConnection, destinationFromSource=True)
                        matching = [x for x in destinations if m in x]
                        for mDest in matching:
                            allConnections.append('%s,%s'%(matConnection,mDest))
                        allMaterials.append(mat)
        return (list(set(allMaterials)),list(set(allConnections)))

sel = cmds.ls(sl=True)
materials,connections = listShadingNodes(sel)
for c in connections:
    print c.split(',')