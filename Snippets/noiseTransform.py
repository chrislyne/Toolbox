import maya.cmds as cmds
from random import uniform

grps = cmds.ls(sl=True)

for g in grps:
    
    cmds.addAttr(g,ln='offsetX',at='double',dv=0)
    cmds.setAttr('%s.offsetX'%(g),e=True,keyable=True)
    cmds.setAttr('%s.offsetX'%(g),uniform(0,30))
    
    cmds.addAttr(g,ln='offsetY',at='double',dv=0)
    cmds.setAttr('%s.offsetY'%(g),e=True,keyable=True)
    cmds.setAttr('%s.offsetY'%(g),uniform(0,30))
    
    cmds.addAttr(g,ln='offsetZ',at='double',dv=0)
    cmds.setAttr('%s.offsetZ'%(g),e=True,keyable=True)
    cmds.setAttr('%s.offsetZ'%(g),uniform(0,30))
    
    cmds.addAttr(g,ln='speed',at='double',dv=0)
    cmds.setAttr('%s.speed'%(g),e=True,keyable=True)
    cmds.setAttr('%s.speed'%(g),uniform(0.05,0.2))
    
    cmds.addAttr(g,ln='amountX',at='double',dv=0)
    cmds.setAttr('%s.amountX'%(g),e=True,keyable=True)
    cmds.setAttr('%s.amountX'%(g),0.1)
    
    cmds.addAttr(g,ln='amountY',at='double',dv=0)
    cmds.setAttr('%s.amountY'%(g),e=True,keyable=True)
    cmds.setAttr('%s.amountY'%(g),0.1)
    
    cmds.addAttr(g,ln='amountZ',at='double',dv=0)
    cmds.setAttr('%s.amountZ'%(g),e=True,keyable=True)
    cmds.setAttr('%s.amountZ'%(g),0)
    
    cmds.addAttr(g,ln='delay',at='double',dv=0)
    cmds.setAttr('%s.delay'%(g),e=True,keyable=True)
    cmds.setAttr('%s.delay'%(g),2)
    
    cmds.expression(o=g,s="$transX = (noise((time+offsetX)*speed))*amountX;\n$transY = (noise((time+offsetY)*speed))*amountY;\n$transZ = (noise((time+offsetZ)*speed))*amountZ;\n\n$cTime = time*25-delay;\n\ntranslateX = `getAttr -time $cTime locator1.translateX`+$transX;\ntranslateY = `getAttr -time $cTime locator1.translateY`+$transY;\ntranslateZ = `getAttr -time $cTime locator1.translateZ`+$transZ;") 
    
