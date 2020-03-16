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
		allNodes = list(set(con))
		#add objects back into the list while it's being iterated 
		for m in allNodes:
			materials = cmds.listConnections( m, source=True,scn=True,destination=False)
			if materials:
				for mat in materials:
					allNodes.append(mat)
					#add file textures to the list 
					nodeType = cmds.nodeType(mat)
					nodeClass = getNodeClassType(nodeType)
					if any(nodeClass in s for s in ['utility','shader','texture']) and nodeClass:
					#if cmds.ls(mat,materials=True) or cmds.ls(mat,tex=True):
						allMaterials.append(mat)
		return (list(set(allMaterials)))
	
	
sel = cmds.ls(sl=True)
shadingNodes = listShadingNodes(sel)
print shadingNodes