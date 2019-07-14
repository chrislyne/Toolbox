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
    ctrlColour = []
    thickness = 2
    
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
        #freeze transformations
        cmds.makeIdentity(ctrl,apply=True,t=1,r=1,s=1)
        
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
    
def createJoints(jointType,lockMidJoints):
    newJoints = []
    for i,j in enumerate(guideJoints):
        #get joint position
        jPos = cmds.xform(j,q=True,t=True,ws=True)
        jRot = cmds.xform(j,q=True,ro=True,ws=True)

    
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
        if i == 0:
            newJoint = cmds.joint(n=newJointName,p=[jPos[0],jPos[1],jPos[2]],o=[jRot[0],jRot[1],jRot[2]])
        else:
            newJoint = cmds.joint(n=newJointName,p=[jPos[0],jPos[1],jPos[2]])
        newJoints.append(newJoint)
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
side = guideJoints[0][-1]
type = 'arm'

cmds.select(cl=True)
blendJoints = createJoints('blend',0)
cmds.select(cl=True)
fkJoints = createJoints('FK',1)
cmds.select(cl=True)
ikJoints = createJoints('IK',1)
cmds.select(cl=True)
bendJoints = createJoints('bend',0)

#create fkIk switch control
middleIndex = (len(guideJoints) - 1)/2
mPos = cmds.xform(guideJoints[middleIndex],q=True,t=True,ws=True)

fkIkCtrl = MakeCtrlCurve()
fkIkCtrl.ctrlName = 'IKFK_%s_switch_CTRL_%s'%(type,side)
fkIkCtrl.pos = mPos
fkIkCtrl.ctrlColour = [1,0,1]
fkIkCtrl = fkIkCtrl.makeCtrl(fkIkCtrl.makePlus())


#fkIkCtrl = createPlusCtrl(mPos,'IKFK_%s_switch_CTRL_%s'%(type,side))
cmds.addAttr(fkIkCtrl,ln='IKFK',at='double',min=0,max=10,dv=0)
cmds.setAttr('%s.IKFK'%fkIkCtrl[0],e=True,keyable=True)
#connect fkIk switch control
multNode = cmds.shadingNode('multiplyDivide',asUtility=True)
cmds.connectAttr('%s.IKFK'%fkIkCtrl[0],'%s.input1X'%multNode)
cmds.setAttr('%s.operation'%multNode,1)
cmds.setAttr('%s.input2X'%multNode,0.1)
revNode = cmds.shadingNode('reverse',asUtility=True)
cmds.connectAttr('%s.outputX'%multNode,'%s.inputX'%revNode)


curvePoints = []
for i,j in enumerate(blendJoints):
    pconst = cmds.parentConstraint(fkJoints[i],ikJoints[i],j)
    cmds.connectAttr('%s.outputX'%multNode,'%s.%sW0'%(pconst[0],fkJoints[i]))
    cmds.connectAttr('%s.outputX'%revNode,'%s.%sW1'%(pconst[0],ikJoints[i]))
    jPos = cmds.xform(j,q=True,t=True,ws=True)
    curvePoints.append(tuple(jPos))

#create controller
ikjPos = cmds.xform(ikJoints[-1],q=True,t=True,ws=True)
ikjRot = cmds.xform(ikJoints[-1],q=True,ro=True,ws=True)
newIKControl = MakeCtrlCurve()
newIKControl.ctrlName = 'IK_%s_CTRL_%s'%(type,side)
newIKControl.ctrlColour = [1,0,1]
newIKControl = newIKControl.makeCtrl(newIKControl.makeCircle())
#newIKControl = cmds.circle(n='IK_%s_CTRL_%s'%(type,side),ch=0,r=0.3)
cmds.xform(newIKControl,ro=[0,-90,0])
cmds.makeIdentity(newIKControl,apply=True,t=1,r=1)
cmds.xform(newIKControl,t=ikjPos,ro=ikjRot,ws=True)
cmds.makeIdentity(newIKControl,apply=True,t=1,r=1)
#add attributes
cmds.addAttr(newIKControl,ln='bendy',at='double',min=0,max=10,dv=0)
cmds.setAttr('%s.bendy'%newIKControl[0],e=True,keyable=True)
cmds.addAttr(newIKControl,ln='stretchy',at='double',min=0,max=10,dv=0)
cmds.setAttr('%s.stretchy'%newIKControl[0],e=True,keyable=True)
cmds.addAttr(newIKControl,ln='length1',at='double')
cmds.setAttr('%s.length1'%newIKControl[0],e=True,keyable=True)
cmds.addAttr(newIKControl,ln='length2',at='double')
cmds.setAttr('%s.length2'%newIKControl[0],e=True,keyable=True)
#create IK handle 
newIkHandle = cmds.ikHandle(sj=ikJoints[0],ee=ikJoints[-1])
cmds.parent(newIkHandle[0],newIKControl)


#create distance
startLoc = locatorChild(ikJoints[0],0)
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
restDistance = 0
for i,j in enumerate(ikJoints):
    if i > 0:
        restDistance += cmds.getAttr('%s.translateX'%j)
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
groupPiv = cmds.xform(startLoc,q=True,t=True,ws=True)
IKGrp = cmds.group([startLoc,ikJoints[0]],n='%s_IK_RIG_%s'%(ikJoints[0].split('_')[0],side))
cmds.xform(IKGrp,piv=groupPiv)


#create curve
ikCurve = cmds.curve(d=3,p=curvePoints,n='%s_ikSpline_curve_%s'%(type,side))
#attach joints
ikSplineHandle = cmds.ikHandle(sj=bendJoints[0], ee=bendJoints[-1],c=ikCurve,sol='ikSplineSolver',ccv=False,pcv=False,n='%s_ikSpline_handle_%s'%(type,side))
splineMultNode = cmds.shadingNode('multiplyDivide',asUtility=True)
cmds.setAttr('%s.operation'%splineMultNode,2)
cmds.setAttr('%s.input2X'%splineMultNode,cmds.arclen(ikCurve))
curveInfoNode = cmds.arclen(ikCurve, ch=True)
cmds.connectAttr('%s.arcLength'%curveInfoNode,'%s.input1X'%splineMultNode)

for i,j in enumerate(bendJoints):
    if i < len(bendJoints)-1:
        cmds.connectAttr('%s.outputX'%splineMultNode,'%s.scaleX'%j)

#get curve cvs
curveCVs = cmds.ls('{0}.cv[:]'.format(ikCurve), fl=True)
#create clusters
bendGrp = cmds.group(em=True,n='bend_leg_GRP_%s'%side)
for i,cv in enumerate(curveCVs):
    newCluster = cmds.cluster(cv)
    #make control
    cPos = cmds.xform(newCluster[1],q=True,piv=True,ws=True)
    newStarCtrl = MakeCtrlCurve()
    newStarCtrl.ctrlName = 'IKFK_%s_switch_CTRL_%s'%(type,side)
    newStarCtrl.ctrlColour = [1,0.7,0]
    bendCtrl = newStarCtrl.makeCtrl(newStarCtrl.makeStar())
    cmds.xform(bendCtrl,ro=[0,-90,0],s=[restDistance/4,restDistance/4,restDistance/4])
    cmds.makeIdentity(apply=True,r=True)
    bendCtrlGrp = cmds.group(bendCtrl,n='bend_leg_CTRL_GRP_%s'%side)
    cmds.xform(bendCtrlGrp,t=[cPos[0],cPos[1],cPos[2]],ws=True)
    cmds.makeIdentity(bendCtrlGrp,apply=True,t=1)
    cmds.parent(newCluster[1],'%s|%s'%(bendCtrlGrp,bendCtrl[0]))
    cmds.parentConstraint(blendJoints[i],bendCtrlGrp,mo=True)
    cmds.parent(bendCtrlGrp,bendGrp)
    

for i,j in enumerate(ikJoints):
    if i < len(ikJoints)-1:
        cmds.connectAttr('%s.outColorR'%condishNode,'%s.scaleX'%j)


