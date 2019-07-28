import maya.cmds as cmds
import maya.OpenMaya as om

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
            opts = self.attr[attrName]
            cmds.addAttr(ctrl,ln=attrName,at='double',dv=0,**opts)
            cmds.setAttr('%s.%s'%(ctrl[0],attrName),e=True,keyable=True)
        
        self.setColour(ctrl)
        self.setThickness(ctrl)
        
        return ctrl
#newCtrl = MakeCtrlCurve()
#newCtrl.ctrlColour = [1,0,1]
#newCtrl.makeCtrl(newCtrl.makeCross())