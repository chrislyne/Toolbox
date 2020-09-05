import maya.cmds as cmds


def rigWindow_UI():
	form = cmds.formLayout(bgc=(0.14,0.14,0.14))


	flow = cmds.flowLayout( columnSpacing=2,wrap=True)
	cmds.iconTextButton(height=60,width=80, flat=True,useAlpha=True,style='iconOnly',highlightImage='logicGrp_over.svg',image='logicGrp.svg',l="Logic Group",en=True,c='makeBlendshapes()')
	cmds.button( height=60,width=80,label='Blendshapes', command='makeBlendshapes()', bgc=(0.14,0.14,0.14))
	cmds.button( height=60,width=80,label='Joints',command='makeJoints()', bgc=(0.14,0.14,0.14))
	cmds.button( height=60,width=80,label='Mirror Joints',command='mirrorJoints()',bgc=(0.14,0.14,0.14))
	cmds.iconTextButton('btn_viewport',height=60,width=80, flat=True,style='iconAndTextVertical',image='textured.png',l="Viewport",h=60,en=True,c='switchToViewport()',bgc=(0.14,0.14,0.14))
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