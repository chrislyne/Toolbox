def materialSwitchWindow():

	window = cmds.window(toolbox=True,title=" ",titleBar=True,widthHeight=(160, 112),sizeable=False )

	formLayout = cmds.formLayout('formLayout')
	cl = cmds.columnLayout("cl",adj=1, rs=6)
	atrributeCol = cmds.columnLayout("atrributeCol",adj=1, rs=6)

	cmds.setParent('..')

	cmds.button(l="Add Material Switch",h=30,c="clickAddRow()") #add switch attributes button

	cmds.setParent(formLayout)

	btn_viewport = cmds.iconTextButton('btn_viewport', flat=False,style='iconAndTextVertical',image='textured.png',l="Viewport",h=60,en=True,c='')
	btn_render =  cmds.iconTextButton('btn_render', flat=False,style='iconAndTextVertical',image='shaded.png',l="Render",h=60,en=True,c='')


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

materialSwitchWindow()

