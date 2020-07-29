import maya.cmds as cmds


def getShadingEngineNodes():
	shadingEngines = []
	sel = cmds.ls(sl=True)
	allChildNodes = []
	for obj in sel:
		childNodes = cmds.listRelatives(obj,allDescendents=True,fullPath=True)
		allChildNodes += childNodes
		
	allChildNodes = list(dict.fromkeys(allChildNodes))

	for shapeNode in allChildNodes:
		shadingEng = cmds.listConnections(shapeNode,type="shadingEngine")
		if shadingEng:
			shadingEngines += shadingEng
			
	shadingEngines = list(set(shadingEngines))
	print shadingEngines
	return shadingEngines



def addHoldingAttrs():
	shadingEngines = getShadingEngineNodes()

	for shdEngNode in shadingEngines:
		
		if cmds.attributeQuery('displayMaterial',node=shdEngNode,ex=True) != 1:
			cmds.addAttr(shdEngNode,longName='displayMaterial',writable=True, dt='float3' )
		if cmds.attributeQuery('renderMaterial',node=shdEngNode,ex=True) != 1:
			cmds.addAttr(shdEngNode,longName='renderMaterial',writable=True, dt='float3' )



def switchToViewport():
	shadingEngines = getShadingEngineNodes()

	for shdEngNode in shadingEngines:
		
		if cmds.attributeQuery('displayMaterial',node=shdEngNode,ex=True):
			try:
				connected = cmds.connectionInfo('%s.displayMaterial'%shdEngNode,sourceFromDestination=True)
				cmds.connectAttr(connected,'%s.surfaceShader'%shdEngNode,f=True)
			except:
				pass


def switchToRender():
	shadingEngines = getShadingEngineNodes()

	for shdEngNode in shadingEngines:
		if cmds.attributeQuery('renderMaterial',node=shdEngNode,ex=True):
			try:
				connected = cmds.connectionInfo('%s.renderMaterial'%shdEngNode,sourceFromDestination=True)
				cmds.connectAttr(connected,'%s.surfaceShader'%shdEngNode,f=True)
			except:
				pass