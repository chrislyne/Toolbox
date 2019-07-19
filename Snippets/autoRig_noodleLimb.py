#cmds.select('shoulder_guideJoint_L',r=True)
#cmds.select('elbow_guideJoint_L',add=True)
#cmds.select('wrist_guideJoint_L',add=True)

#AUTO RIG NOODLE LIMB
#
#
import maya.cmds as cmds

class MakeCtrlCurve:
    
    ctrlName = 'newCtrl'
    pos = [0,0,0]
    rot = [0,0,0]
    scl = [1,1,1]
    ctrlColour = []
    thickness = 2
    attr = {}
    
    #set colour
    def setColour(self,ctrl):
        if self.ctrlColour:
            curveShapes = cmds.listRelatives(ctrl,s=True)
            #set colours of curve shapes
            for s in curveShapes:
                cmds.setAttr('%s.overrideEnabled'%s,1) 
                cmds.setAttr('%s.overrideRGBColors'%s,1) 
                cmds.setAttr('%s.overrideColorRGB'%s,self.ctrlColour[0],self.ctrlColour[1],self.ctrlColour[2])
            
    def setThickness(self,ctrl):
        #find shape nodes
        curveShapes = cmds.listRelatives(ctrl,s=True)
        for s in curveShapes:
            #set curve thickness
            cmds.setAttr( '%s.lineWidth'%s,self.thickness)
       
            
    def makeSquare(self):
        #make circle
        ctrl = cmds.circle(r=0.3,s=4,ut=0,d=1,ch=0,sw=360,tol=0.01,n=self.ctrlName)
        cmds.xform(ctrl,ro=[0,0,45],t=self.pos)
        return ctrl
        
    def makeDiamond(self):
        #make circle
        ctrl = cmds.circle(r=0.3,s=4,ut=0,d=1,ch=0,sw=360,tol=0.01,n=self.ctrlName)
        cmds.xform(ctrl,t=self.pos)
        return ctrl
        
    def makePlus(self):
        #make circle
        ctrl = cmds.circle(r=0.3,s=12,ut=0,d=1,ch=0,sw=360,tol=0.01,n=self.ctrlName)
        cmds.xform(ctrl,ro=[0,0,15],t=self.pos)
        #shape plus
        cvs = ['%s.cv[1]'%ctrl[0],'%s.cv[10]'%ctrl[0],'%s.cv[7]'%ctrl[0],'%s.cv[4]'%ctrl[0]]
        cmds.scale(0.361464,0.361464,0.361464,cvs,r=True,) 
        return ctrl
        
    def makeStar(self):
        #make circle
        ctrl = cmds.circle(r=0.3,s=8,ut=0,d=0,ch=0,sw=360,tol=0.01,n=self.ctrlName)
        cmds.xform(ctrl,t=self.pos)
        #shape star
        cvs = ['%s.cv[0]'%ctrl[0],'%s.cv[2]'%ctrl[0],'%s.cv[4]'%ctrl[0],'%s.cv[6]'%ctrl[0]]
        cmds.scale(0.0876642,0.0876642,0.0876642,cvs,r=True,) 
        return ctrl
        
    def makeCircle(self):
        #make circle
        ctrl = cmds.circle(r=0.3,s=8,ut=0,d=0,ch=0,sw=360,tol=0.01,n=self.ctrlName)
        cmds.xform(ctrl,t=self.pos)
        return ctrl
        
    def makeCross(self):
        ctrl = cmds.nurbsSquare(c=[0,0,0],nr=[0,1,0],sl1=1,sl2=1,sps=1,d=3,ch=0,n=self.ctrlName)
        children = cmds.listRelatives(ctrl[0],c=True,pa=True)
        #move curves into place
        cmds.xform(children[0],t=[0,0,-0.5])
        cmds.xform(children[1],t=[0.5,0,0])
        cmds.xform(children[2],t=[0,0,0.5],ro=[0,0,90])
        #parent childrens shapes to top transform
        cmds.makeIdentity(ctrl,apply=True,t=1,r=1,s=1)
        cmds.parent(cmds.listRelatives(children[0],s=True,pa=True),cmds.listRelatives(children[1],s=True,pa=True),cmds.listRelatives(children[2],s=True,pa=True),ctrl[0],add=True,s=True)
        #clean up original transforms
        cmds.delete(children)
        #set position
        cmds.xform(ctrl,t=self.pos)

        return ctrl


    
    def makeCtrl(self,ctrl):
        #set transformations
        cmds.makeIdentity(ctrl,apply=True,t=1,r=1,s=1)
        cmds.xform(ctrl,ro=self.rot,s=self.scl)
        cmds.makeIdentity(ctrl,apply=True,t=1,r=1,s=1)
        #set attributes
        for attrName in self.attr:
            cmds.addAttr(ctrl,ln=attrName,at='double',dv=0)
            try:
                cmds.addAttr('%s.%s'%(ctrl[0],attrName),e=True,min=self.attr[attrName]['min'])
            except:
                pass
            try:
                cmds.addAttr('%s.%s'%(ctrl[0],attrName),e=True,max=self.attr[attrName]['max'])
            except:
                pass
            
            cmds.setAttr('%s.%s'%(ctrl[0],attrName),e=True,keyable=True)
        
        self.setColour(ctrl)
        self.setThickness(ctrl)
        
        return ctrl
    

    
#newCtrl = MakeCtrlCurve()
#newCtrl.ctrlName = 'bar'
#newCtrl.ctrlColour = [1,0,1]
#newCtrl.makeCtrl(newCtrl.makeCross())


def midpoint(p1,p2):
    #return midpoint 
    m1 = []
    m1.append((p1[0] + p2[0])/2)
    m1.append((p1[1] + p2[1])/2)
    m1.append((p1[2] + p2[2])/2)
    return m1
    
def createJoints(type,jointType,lockMidJoints):
    cmds.select(cl=True)
    newJoints = []
    parentJRot = [0,0,0]
    for i,j in enumerate(guideJoints):
        #get joint position
        jPos = cmds.xform(j,q=True,t=True,ws=True)
        jRotWs = cmds.xform(j,q=True,ro=True,os=False,ws=True)
            
        jRot = [parentJRot[0]*-1 + jRotWs[0],parentJRot[1]*-1 + jRotWs[1],parentJRot[2]*-1 + jRotWs[2] ]

        parentJRot = jRotWs

    
        if guideJoints[i-1] and i > 0:
            #create midpoint joint
            mjPos = midpoint(jPos,cmds.xform(guideJoints[i-1],q=True,t=True,ws=True))
            newJointName = guideJoints[i-1].replace('_guide','Mid_%s'%jointType)
            newJoint = cmds.joint(n=newJointName,p=[mjPos[0],mjPos[1],mjPos[2]])
            newJoints.append(newJoint)
            #lock mid joints
            if lockMidJoints == 1:
                 cmds.setAttr('%s.rx'%newJoint,lock=True)
                 cmds.setAttr('%s.ry'%newJoint,lock=True)
                 cmds.setAttr('%s.rz'%newJoint,lock=True)
        #create new joint
        newJointName = j.replace('guide',jointType)
        newJoint = cmds.joint(n=newJointName,p=[jPos[0],jPos[1],jPos[2]],o=[jRot[0],jRot[1],jRot[2]])
        newJoints.append(newJoint)
    #group joints
    groupPiv = cmds.xform(newJoints[0],q=True,t=True,ws=True)
    jointGrp = cmds.group(newJoints[0],n='%s_%sJoint_GRP_%s'%(type,jointType,guideJoints[0][-1]))
    cmds.xform(jointGrp,piv=groupPiv)
    
    return newJoints
    
def locatorChild(obj,hierarchy):
    #create locator
    newLocator = cmds.spaceLocator(n='%s_LOC'%obj)
    #position and parent locator to obj
    pPos = cmds.xform(obj,q=True,piv=True,ws=True)
    cmds.move(pPos[0],pPos[1],pPos[2],newLocator,ws=True)
    if hierarchy:
        cmds.parent(newLocator[0],obj)
    return newLocator[0]
    
#list joints
guideJoints = cmds.ls(sl=True)

restDistance = 0
for i,j in enumerate(guideJoints):
    if i > 0:
        restDistance += cmds.getAttr('%s.translateX'%j)

side = guideJoints[0][-1]
type = 'arm'

#create joints
blendJoints = createJoints(type,'blend',0)
fkJoints = createJoints(type,'FK',1)
ikJoints = createJoints(type,'IK',1)
bendJoints = createJoints(type,'bend',0)

#create main CTRL
#get position
startPos = cmds.xform(guideJoints[0],q=True,t=True,ws=True)
mainCtrl = MakeCtrlCurve()
mainCtrl.ctrlName = '%s_CTRL_%s'%(type,side)
mainCtrl.pos = startPos
mainCtrl.rot = [0,90,0]
mainCtrl.scl = [restDistance/2,restDistance/2,restDistance/2]
mainCtrl.ctrlColour = [0,1,0]
mainCtrl = mainCtrl.makeCtrl(mainCtrl.makeDiamond())

mainCtrlGrp = cmds.group(mainCtrl,name='%s_CTRL_GRP_%s'%(type,side))
guideJRot = cmds.xform(guideJoints[0],q=True,ro=True,ws=True)
cmds.xform(mainCtrlGrp,ro=guideJRot)
mainCtrl = '%s|%s'%(mainCtrlGrp,mainCtrl[0])
#parent ik joints to main ctrl
cmds.parentConstraint(mainCtrl,cmds.listRelatives(ikJoints[0],p=True),mo=True)

#create fkIk switch control
middleIndex = (len(guideJoints) - 1)/2
mPos = cmds.xform(guideJoints[middleIndex],q=True,t=True,ws=True)

#fkIk control
fkIkCtrl0 = MakeCtrlCurve()
fkIkCtrl0.ctrlName = 'IKFK_%s_switch_CTRL_%s'%(type,side)
fkIkCtrl0.pos = mPos
fkIkCtrl0.ctrlColour = [0,1,0]
fkIkCtrl0.attr = {'IKFK':{'min':0,'max':10}}
fkIkCtrl = fkIkCtrl0.makeCtrl(fkIkCtrl0.makePlus())

#connect fkIk switch control
multNode = cmds.shadingNode('multiplyDivide',asUtility=True)
cmds.connectAttr('%s.IKFK'%fkIkCtrl[0],'%s.input1X'%multNode)
cmds.setAttr('%s.operation'%multNode,1)
cmds.setAttr('%s.input2X'%multNode,0.1)
revNode = cmds.shadingNode('reverse',asUtility=True)
cmds.connectAttr('%s.outputX'%multNode,'%s.inputX'%revNode)
#make visibility switches
fkVisCondition = cmds.shadingNode('condition',asUtility=True)
cmds.setAttr('%s.secondTerm'%fkVisCondition,0.5) 
cmds.setAttr('%s.operation'%fkVisCondition,2) 
cmds.setAttr('%s.colorIfTrueR'%fkVisCondition,1) 
cmds.setAttr('%s.colorIfFalseR'%fkVisCondition,0) 
cmds.connectAttr('%s.IKFK'%fkIkCtrl[0],'%s.firstTerm'%fkVisCondition)

ikVisCondition = cmds.shadingNode('condition',asUtility=True)
cmds.setAttr('%s.secondTerm'%ikVisCondition,9.5) 
cmds.setAttr('%s.operation'%ikVisCondition,4) 
cmds.setAttr('%s.colorIfTrueR'%ikVisCondition,1)
cmds.setAttr('%s.colorIfFalseR'%ikVisCondition,0) 
cmds.connectAttr('%s.IKFK'%fkIkCtrl[0],'%s.firstTerm'%ikVisCondition)

curvePoints = []
for i,j in enumerate(blendJoints):
    pconst = cmds.parentConstraint(fkJoints[i],ikJoints[i],j)
    cmds.connectAttr('%s.outputX'%multNode,'%s.%sW0'%(pconst[0],fkJoints[i]))
    cmds.connectAttr('%s.outputX'%revNode,'%s.%sW1'%(pconst[0],ikJoints[i]))
    jPos = cmds.xform(j,q=True,t=True,ws=True)
    curvePoints.append(tuple(jPos))
    
#fk control
fkParent = ''
nextInt = 0
for i,j in enumerate(fkJoints):
    if i == nextInt:
        fkJpos = cmds.xform(j,q=True,t=True,ws=True)
        fkCtrl = MakeCtrlCurve()
        fkCtrl.ctrlName = 'FK_%s_CTRL_%s'%(j.split('_')[0],side)
        fkCtrl.pos = fkJpos
        fkCtrl.rot = [0,90,0]
        fkCtrl.scl = [restDistance/4,restDistance/4,restDistance/4]
        fkCtrl.ctrlColour = [0,0,1]
        fkCtrl = fkCtrl.makeCtrl(fkCtrl.makeSquare())

        fkCtrlGrp = cmds.group(fkCtrl,name='%s_GRP'%fkCtrl[0])
        fkjRot = cmds.xform(j,q=True,ro=True,ws=True)
        cmds.xform(fkCtrlGrp,ro=fkjRot)
        fkCtrl = '%s|%s'%(fkCtrlGrp,fkCtrl[0])
        cmds.parentConstraint(fkCtrl,j)
        nextInt += 2
        if fkParent:
            cmds.parent(fkCtrlGrp,fkParent)
        fkParent = fkCtrl
        if i == 0:
            #connect ikfk switch to group visibility
            cmds.connectAttr('%s.outColorR'%fkVisCondition,'%s.visibility'%fkCtrlGrp)

            cmds.parent(fkCtrlGrp,mainCtrl)
         
#ik control
#create controller
ikjPos = cmds.xform(ikJoints[-1],q=True,t=True,ws=True)
ikjRot = cmds.xform(ikJoints[-1],q=True,ro=True,ws=True)
newIKControl = MakeCtrlCurve()
newIKControl.ctrlName = 'IK_%s_CTRL_%s'%(type,side)
newIKControl.ctrlColour = [1,0,0]
newIKControl.pos = ikjPos
newIKControl.rot = [ikjRot[0],ikjRot[1]-90,ikjRot[2]]
newIKControl.attr = {'bendy':{'min':0,'max':10},'stretchy':{'min':0,'max':10},'preserveVol':{}}
newIKControl = newIKControl.makeCtrl(newIKControl.makeCircle())
#orient constrain end ikJoint to ik CTRL
cmds.orientConstraint(newIKControl[0],ikJoints[-1],mo=True)
#add additional attributes
for i,j in enumerate(guideJoints[:-1]):
    i = i+1
    cmds.addAttr(newIKControl,ln='length%s'%i,at='double')
    cmds.setAttr('%s.length%s'%(newIKControl[0],i),e=True,keyable=True)
#create IK handle 
newIkHandle = cmds.ikHandle(sj=ikJoints[0],ee=ikJoints[-1])
cmds.parent(newIkHandle[0],newIKControl)
#create distance
startLoc = locatorChild(ikJoints[0],0)
cmds.parent(startLoc,mainCtrl)
endLoc = locatorChild(newIKControl[0],1)
distanceNode = cmds.shadingNode('distanceBetween',asUtility=True)
cmds.connectAttr('%s.worldPosition[0]'%startLoc,'%s.point1'%distanceNode)
cmds.connectAttr('%s.worldPosition[0]'%endLoc,'%s.point2'%distanceNode)
#math nodes
floatComp = cmds.shadingNode('floatComposite',asUtility=True)
stretchMultiply = cmds.shadingNode('floatComposite',asUtility=True)
cmds.setAttr('%s.operation'%stretchMultiply,3)
cmds.setAttr('%s.floatB'%stretchMultiply,0.1)
cmds.connectAttr('%s.stretchy'%newIKControl[0],'%s.floatA'%stretchMultiply)
cmds.connectAttr('%s.outFloat'%stretchMultiply,'%s.factor'%floatComp)
cmds.setAttr('%s.operation'%floatComp,2)

cmds.setAttr('%s.floatB'%floatComp,restDistance)
cmds.connectAttr('%s.distance'%distanceNode,'%s.floatA'%floatComp)
multNode = cmds.shadingNode('multiplyDivide',asUtility=True)
cmds.connectAttr('%s.distance'%distanceNode,'%s.input1X'%multNode)
cmds.connectAttr('%s.outFloat'%floatComp,'%s.input2X'%multNode)
cmds.setAttr('%s.operation'%multNode,2)


#scale IK controller
cmds.xform(newIKControl,s=[restDistance/4,restDistance/4,restDistance/4])
cmds.makeIdentity(newIKControl,apply=True,s=1)

condishNode = cmds.shadingNode('condition',asUtility=True)
cmds.connectAttr('%s.distance'%distanceNode,'%s.firstTerm'%condishNode)
cmds.connectAttr('%s.input2X'%multNode,'%s.secondTerm'%condishNode)
cmds.setAttr('%s.operation'%condishNode,2)
cmds.connectAttr('%s.outputX'%multNode,'%s.colorIfTrueR'%condishNode)
#group IK parts
#groupPiv = cmds.xform(startLoc,q=True,t=True,ws=True)
#IKGrp = cmds.group([startLoc,ikJoints[0]],n='%s_IK_RIG_%s'%(ikJoints[0].split('_')[0],side))
#cmds.xform(IKGrp,piv=groupPiv)


ikCtrlGrp = cmds.group(newIKControl,n='%s_IK_CTRL_GRP_%s'%(type,side))
cmds.xform(ikCtrlGrp,piv=startPos,ws=True)
cmds.connectAttr('%s.outColorR'%ikVisCondition,'%s.visibility'%ikCtrlGrp)


#create curve
ikCurve = cmds.curve(d=3,p=curvePoints,n='%s_ikSpline_curve_%s'%(type,side))
#attach joints
ikSplineHandle = cmds.ikHandle(sj=bendJoints[0], ee=bendJoints[-1],c=ikCurve,sol='ikSplineSolver',ccv=False,pcv=False,n='%s_ikSpline_handle_%s'%(type,side))
splineMultNode = cmds.shadingNode('multiplyDivide',asUtility=True)
cmds.setAttr('%s.operation'%splineMultNode,2)
cmds.setAttr('%s.input2X'%splineMultNode,cmds.arclen(ikCurve))
curveInfoNode = cmds.arclen(ikCurve, ch=True)
cmds.connectAttr('%s.arcLength'%curveInfoNode,'%s.input1X'%splineMultNode)
#group ikSpline parts
ikSpline_GRP = cmds.group(ikCurve,ikSplineHandle[0],n='%s_ikSpline_GRP_%s'%(type,side))

for i,j in enumerate(bendJoints):
    if i < len(bendJoints)-1:
        cmds.connectAttr('%s.outputX'%splineMultNode,'%s.scaleX'%j)

#get curve cvs
curveCVs = cmds.ls('{0}.cv[:]'.format(ikCurve), fl=True)
#create clusters
bendGrp = cmds.group(em=True,n='bend_%s_GRP_%s'%(type,side))
cmds.xform(bendGrp,piv=startPos,ws=True)
for i,cv in enumerate(curveCVs):
    newCluster = cmds.cluster(cv)
    #make control
    cPos = cmds.xform(newCluster[1],q=True,piv=True,ws=True)
    newStarCtrl = MakeCtrlCurve()
    newStarCtrl.ctrlName = 'IKFK_%s_switch_CTRL_%s'%(type,side)
    newStarCtrl.ctrlColour = [1,0.7,0]
    bendCtrl = newStarCtrl.makeCtrl(newStarCtrl.makeStar())
    cmds.xform(bendCtrl,ro=[0,-90,0],s=[restDistance/4,restDistance/4,restDistance/4])
    cmds.makeIdentity(apply=True,r=True,s=True)
    bendCtrlGrp = cmds.group(bendCtrl,n='bend_%s_CTRL_GRP_%s'%(type,side))
    cmds.xform(bendCtrlGrp,t=[cPos[0],cPos[1],cPos[2]],ws=True)
    cmds.makeIdentity(bendCtrlGrp,apply=True,t=1)
    cmds.parent(newCluster[1],'%s|%s'%(bendCtrlGrp,bendCtrl[0]))
    cmds.parentConstraint(blendJoints[i],bendCtrlGrp,mo=True)
    cmds.parent(bendCtrlGrp,bendGrp)

cmds.parent(fkIkCtrl[0],mainCtrl)

#volume preservation
preserveVolFloatMath = cmds.shadingNode('floatMath',asUtility=True)
cmds.setAttr('%s.floatB'%preserveVolFloatMath,0.1)
cmds.setAttr('%s.operation'%preserveVolFloatMath,2)
cmds.connectAttr('%s.preserveVol'%newIKControl[0],'%s.floatA'%preserveVolFloatMath)
preserveVolCompNode = cmds.shadingNode('floatComposite',asUtility=True)
cmds.setAttr('%s.operation'%preserveVolCompNode,6)
cmds.connectAttr('%s.outFloat'%preserveVolFloatMath,'%s.floatA'%preserveVolCompNode)
for i,j in enumerate(bendJoints[1:-1]):
    floatMathNode = cmds.shadingNode('floatMath',asUtility=True)
    cmds.setAttr('%s.operation'%floatMathNode,3)
    cmds.connectAttr('%s.scaleX'%j,'%s.floatB'%floatMathNode)
    clampNode = cmds.shadingNode('clamp',asUtility=True)
    cmds.setAttr('%s.maxR'%clampNode,1)
    cmds.connectAttr('%s.outFloat'%preserveVolCompNode,'%s.minR'%clampNode)
    cmds.connectAttr('%s.outFloat'%floatMathNode,'%s.inputR'%clampNode)
    cmds.connectAttr('%s.outputR'%clampNode,'%s.scaleY'%j)
    cmds.connectAttr('%s.outputR'%clampNode,'%s.scaleZ'%j)

#connect end last bendJoint orientation to last bendJoint
cmds.orientConstraint(blendJoints[-1],bendJoints[-1])

for i,j in enumerate(ikJoints):
    if i < len(ikJoints)-1:
        cmds.connectAttr('%s.outColorR'%condishNode,'%s.scaleX'%j)

#final grouping
CTRL_constraint_GRP = cmds.group(mainCtrlGrp,ikCtrlGrp,n='%s_CTRL_constraint_GRP_%s'%(type,side))
cmds.xform(CTRL_constraint_GRP,piv=[0,0,0],ws=True)
CTRL_GRP = cmds.group(CTRL_constraint_GRP,bendGrp,n='%s_CTRL_GRP_%s'%(type,side))
joint_GRP = cmds.group(cmds.listRelatives(ikJoints[0],p=True),cmds.listRelatives(fkJoints[0],p=True),cmds.listRelatives(blendJoints[0],p=True),cmds.listRelatives(bendJoints[0],p=True),n='%s_joint_GRP_%s'%(type,side))
cmds.group(ikSpline_GRP,CTRL_GRP,joint_GRP,n='%s_RIG_%s'%(type,side))




