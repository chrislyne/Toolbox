import maya.cmds as cmds

def listFilePaths(allTextures):
	#paths to texture files
	textureFiles = []
	#find the file path from the textures 
	for t in allTextures:
		filePath = cmds.getAttr('%s.fileTextureName'%t)
		if filePath:
			textureFiles.append(filePath)
	#return a list of file paths without duplicates
	return list(set(textureFiles))

#return a list of file paths from the selected objects
def listShadingNodes(objects,nodeType):
	#texture nodes
	allTextures = []
	#list ALL of the objects shape nodes
	allShapes = []
	for o in objects:
		shapes = cmds.listRelatives( o, allDescendents=True,type='shape')
		allShapes += shapes
	
	for shape in allShapes:
		#find connected shading networks
		con = cmds.listConnections( shape, scn=True, type='shadingEngine' )
		#remove duplicate materials  
		allMaterials = list(set(con))
		#add objects back into the list while it's being iterated 
		for m in allMaterials:
			materials = cmds.listConnections( m, source=True,scn=True,destination=False)
			if materials:
				for mat in materials:
					allMaterials.append(mat)
					#add file textures to the list 
					if cmds.ls(mat,type=nodeType):
						allTextures.append(mat)
	return allTextures	

#sel = cmds.ls(sl=True)
#fileNodes = listShadingNodes(sel,'file')
#if fileNodes:
#	print listFilePaths(fileNodes)