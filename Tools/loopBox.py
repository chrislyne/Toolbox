import maya.cmds as cmds

def clickAddRow():
	#Instatiate AddRow with blank values
	newRow = AddRow()
	newRow.makeNewRow()

def dropAddRow( dragControl, dropControl, messages, x, y, dragType ): 
	#Instatiate AddRow with values from dragged attribute
	newRow = AddRow()
	newRow.attributeName = messages[0].split('.')[-1]
	newRow.attrType = cmds.getAttr(messages[0],type=True)
	newRow.attrValue= cmds.getAttr(messages[0])
	newRow.makeNewRow()

class AddRow():

	attributeName = ''
	attrType = "float"
	attrValue = ""

	def makeNewRow(self):

		def queryCheckBox(self):
			value = cmds.checkBox(valueField,q=True,v=True)
			return value

		def queryFloat(self):
			value = cmds.floatSliderGrp(valueField,q=True,v=True)
			print value
			return float(value)

		def doLoop(self):

			attr = cmds.textField(attrText,q=True,text=True)

			print attrType

			valueDict = {"bool" : queryCheckBox,
                "double" : queryFloat,
                "float" : queryFloat,
                "long" : makeTextField,
                "enum" : makeTextField,
                "doubleAngle" : makeTextField,
                "string" : makeTextField,
                "none" : makeTextField,
			}
			value = valueDict[attrType](self)
			print value

			sel = cmds.ls(sl=True)
			for obj in sel:
				if cmds.attributeQuery(attr, node=obj,exists=True):
					cmds.setAttr('%s.%s'%(obj,attr),value) 
				else:
					objChildren = cmds.listRelatives(obj,children=True)
					for objChild in objChildren:
						if cmds.attributeQuery(attr, node=objChild,exists=True):
							cmds.setAttr('%s.%s'%(objChild,attr),value) 



		def makeCheckBox(self):
			valueField = cmds.checkBox('valueField',l='',v=self.attrValue)
			return valueField
		def makeFloatSlider(self):
			valueField = cmds.floatSliderGrp('valueField',l='',field=True,v=float(self.attrValue))
			return valueField
		def makeTextField(self):
			valueField = cmds.textField('valueField',w=50,text=self.attrValue)
			return valueField

		def makeFloat3(self):
			valueField = cmds.textField('valueField',w=50)
			return valueField

		#set parent to layout
		cmds.setParent('atrributeCol')
		#make row layout
		cmds.rowLayout(h=30,adj=4,columnAttach=(5,"right",0),dpc='',nc=5)
		#make delete row button
		delBtn = cmds.button(l='x',h=20,w=20)
		thisParent = cmds.button(delBtn,q=True,parent=True)
		cmds.button(delBtn,e=True,c=('cmds.deleteUI(\'%s\')'%thisParent))
		#make text field to display attribute
		attrText = cmds.textField('attrText',w=150,text=self.attributeName)
		#display attribute value
		uiTypeDict = {"bool" : makeCheckBox,
                "double" : makeTextField,
                "float" : makeFloatSlider,
                "long" : makeTextField,
                "enum" : makeTextField,
                "doubleAngle" : makeTextField,
                "string" : makeTextField,
                "none" : makeTextField,
                "float3" : makeFloat3
		}
		attrType = self.attrType
		print self.attrType
		valueField = uiTypeDict[self.attrType](self)
		#visually separate button
		cmds.separator(st="none")
		#make individual loop button
		loopBtn = cmds.button("loopBtn",l="Loop",c=doLoop)



def LoopboxWindow():

	loopBoxForm = cmds.formLayout('loopBoxForm')
	cl = cmds.columnLayout("cl",adj=1, rs=6)
	atrributeCol = cmds.columnLayout("atrributeCol",adj=1, rs=6)

	cmds.setParent('..')

	cmds.columnLayout('dropAreaCol',adj=1,h=30) 
	cmds.button(l="Drop Attribute Here",h=30,dpc=dropAddRow,c="clickAddRow()",bgc=(0.3,0.3,0.3))


	cmds.setParent(loopBoxForm)

	#loopBoxForm = cmds.formLayout('loopBoxForm')
	btn_loop = cmds.button('btn_loop',l="Loop",h=50,en=True,c='')
	btn_close = cmds.button('btn_close',l="Close",h=50,en=True,c='')


	
	cmds.formLayout(loopBoxForm,edit=True,
		attachForm=[
		 (cl,'left',0),
		 (cl,'right',0),
		 (btn_loop,'bottom',0),
		 (btn_loop,'left',0),
		 (btn_close,'bottom',0),
		 (btn_close,'right',0)
		],
		attachControl=[
		 (btn_close,'left',0,btn_loop)
		],
		ap=[
		 (btn_loop,'right',0,50)
		] 
	)

	loopBoxForm;


def dockingLoopbox():
	WorkspaceName = 'Loopbox'
	if (cmds.workspaceControl('Loopbox', exists=True)):
		cmds.deleteUI('Loopbox')
	cmds.workspaceControl( WorkspaceName,initialHeight=500,initialWidth=320, uiScript = 'LoopboxWindow()' )

dockingLoopbox()