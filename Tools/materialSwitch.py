import maya.cmds as cmds

def getShadingEngineNodes():
	shadingEngines = [] #hold all connected shading engines
	sel = cmds.ls(sl=True) #list selected nodes
	if sel: #check if anything is selected
		allChildNodes = [] #hold all decendents of selection
		for obj in sel: #loop through selected objects
			childNodes = cmds.listRelatives(obj,allDescendents=True,fullPath=True) #list child nodes
			allChildNodes += childNodes #add child nodes to the main list of decendents 
		allChildNodes = list(dict.fromkeys(allChildNodes)) #remove duplicates from list
		for shapeNode in allChildNodes: #loop through all child nodes
			shadingEng = cmds.listConnections(shapeNode,type="shadingEngine") #find connected shading engine
			if shadingEng: #<-- redundant?
				shadingEngines += shadingEng #add to list of all connected shading engines
		shadingEngines = list(set(shadingEngines)) #remove duplicate shading engines from list
	else: #if nothing is selected
		shadingEngines = cmds.ls(type="shadingEngine") #list all shading engines in scene
		shadingEngines.remove('initialParticleSE') #remove 'initialParticleSE' from list
		shadingEngines.remove('initialShadingGroup') #remove 'initialShadingGroup' from list
	return shadingEngines #return requested shading engines

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

def materialSwitchWindow():

	window = cmds.window(toolbox=True,title=" ",titleBar=True,widthHeight=(160, 112),sizeable=False )

	formLayout = cmds.formLayout('formLayout')
	cl = cmds.columnLayout("cl",adj=1, rs=6)
	atrributeCol = cmds.columnLayout("atrributeCol",adj=1, rs=6)

	cmds.setParent('..')

	cmds.button(l="Add Material Switch",h=30,c="addHoldingAttrs()") #add switch attributes button

	cmds.setParent(formLayout)

	btn_viewport = cmds.iconTextButton('btn_viewport', flat=False,style='iconAndTextVertical',image='textured.png',l="Viewport",h=60,en=True,c='switchToViewport()')
	btn_render =  cmds.iconTextButton('btn_render', flat=False,style='iconAndTextVertical',image='shaded.png',l="Render",h=60,en=True,c='switchToRender()')

 
 
	cmds.formLayout(formLayout,edit=True,
		attachForm=[
		 (cl,'left',5),
		 (cl,'right',5),
		 (btn_viewport,'bottom',6),
		 (btn_viewport,'left',6),
		 (btn_render,'bottom',6),
		 (btn_render,'right',6)
		],
		attachControl=[
		 (btn_render,'left',6,btn_viewport)
		],
		ap=[
		 (btn_viewport,'right',6,50)
		] 
	)

	formLayout;

	cmds.showWindow( window )

#materialSwitchWindow()

