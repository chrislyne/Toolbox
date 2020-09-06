import maya.cmds as cmds

def rigWindow_UI():
	form = cmds.formLayout(bgc=(0.14,0.14,0.14))
	flow = cmds.flowLayout( columnSpacing=2,wrap=True)
	buttons = [
		{
		"highlightImage":"logicGrp.svg",
		"image":"logicGrp.svg",
		"l":"Logic Group",
		"c":"makeBlendshapes()"
		},
		{
		"highlightImage":"blendshapes.svg",
		"image":"blendshapes.svg",
		"l":"Blendshapes",
		"c":"makeBlendshapes()"
		},
		{
		"highlightImage":"makeJoints.svg",
		"image":"makeJoints.svg",
		"l":"Joints",
		"c":"makeJoints()"
		},
		{
		"highlightImage":"mirrorJoints.svg",
		"image":"mirrorJoints.svg",
		"l":"Mirror Joints",
		"c":"mirrorJoints()"
		}
	]
	for b in buttons:
		cmds.iconTextButton(height=60,width=60, flat=True,useAlpha=True,style='iconOnly',highlightImage=b["highlightImage"],image=b["image"],l=b["l"],en=True,c=b["c"])
	cmds.setParent('..')

	cmds.formLayout(form,  edit=True, 
	                     attachForm=[ (flow, 'left', 0),
	                     (flow, 'top', 0),
	                     (flow, 'right', 0),
	                     (flow, 'bottom', 0),])

def rigWindow():
	workspaceName = 'rigWindow'
        if(cmds.workspaceControl(workspaceName, exists=True)):
            cmds.deleteUI(workspaceName)
        cmds.workspaceControl(workspaceName,initialHeight=100,initialWidth=300,uiScript = 'rigWindow_UI()')

rigWindow()