import maya.cmds as cmds

#adds value to an attribute
def addAttribute(shape,attrName,attrValue):
    if not cmds.attributeQuery(attrName,node=shape,exists=True):
        cmds.addAttr(shape,ln=attrName,dt='string')
    cmds.setAttr('%s.%s'%(shape,attrName),e=True,keyable=True)
    cmds.setAttr('%s.%s'%(shape,attrName),attrValue,type='string')

#clean padding
def addPadding(s,padding):
    while len(s) < padding:
        s = '0%s'%s
    return s

#check if string contains any digits
def containsDigits(s):
    for char in list(s):
        if char.isdigit():
            return True
            break
    return False 