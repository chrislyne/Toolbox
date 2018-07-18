import maya.cmds as cmds
import maya.mel as mel

def LlamaIOWindow():
    
    buttonColour = [0.33,0.58,0.74]
    
    installForm = cmds.formLayout(bgc=[0.1,0.4,0.55])

    modelTitle = cmds.text(fn='boldLabelFont',label="Modeling")
    publishModel_btn = cmds.iconTextButton(hlc=[1,1,1],olc=[0,0,0],st='iconAndTextVertical',i='io_publishModel.svg',bgc=buttonColour,height=50,width=100,label='Publish REF',ann='Select top node to publish',c='')
    
    sep1 = cmds.separator( hr=1,style='in' ,height=2)
    
    animTitle = cmds.text(fn='boldLabelFont',label="Animation")
    publishAnim_btn = cmds.iconTextButton(st='iconAndTextVertical',i='io_publishAnim.svg',bgc=buttonColour,height=50,width=100,label='Publish Anim',c='')
    publishCam_btn = cmds.iconTextButton(st='iconAndTextVertical',i='io_publishCam.svg',bgc=buttonColour,height=50,width=100,label='Publish Camera',c='')
    megaPublish_btn = cmds.iconTextButton(st='iconAndTextVertical',i='io_publishModel.svg',bgc=buttonColour,height=50,width=100,label='Publish to NEW SCENE',c='')
    
    sep2 = cmds.separator( hr=1,style='in' ,height=2)
    
    sceneTitle = cmds.text(fn='boldLabelFont',label="Scene Reconstruction")
    importAnim_btn = cmds.iconTextButton(st='iconAndTextVertical',i='io_importAnim.svg',bgc=buttonColour,height=50,width=100,label='Import Anim',c='')
    importCam_btn = cmds.iconTextButton(st='iconAndTextVertical',i='io_importCam.svg',bgc=buttonColour,height=50,width=100,label='Import Camera',c='')
    importMat_btn = cmds.iconTextButton(st='iconAndTextVertical',i='io_importAnim.svg',bgc=buttonColour,height=50,width=100,label='Import Materials',c='')
    importAll_btn = cmds.iconTextButton(hlc=[1,1,1],st='iconAndTextVertical',i='io_importAnim.svg',bgc=buttonColour,height=50,width=100,label='I\'m Feeling Lucky',c='')
     
    
    cmds.formLayout(installForm,  edit=True, 
                     attachForm=[
                     (modelTitle, 'left', 10),
                     (modelTitle, 'top', 10),
                     (publishModel_btn, 'left', 10),
                     (animTitle, 'top', 120),
                     (animTitle, 'left', 10),
                     (publishCam_btn, 'right', 10),
                     (publishAnim_btn, 'left', 10),
                     (megaPublish_btn, 'left', 10),
                     (megaPublish_btn, 'right', 10),
                     (sceneTitle, 'left', 10),
                     (importCam_btn, 'left', 10),
                     (importMat_btn, 'right', 10),
                     (importAll_btn, 'left', 10),
                     (importAll_btn, 'right', 10)
                     ],
                     attachControl=[
                     (publishModel_btn, 'top', 10,modelTitle),
                     (sep1, 'top', 24,publishModel_btn),
                     (publishAnim_btn, 'top', 10,animTitle),
                     (publishCam_btn, 'top', 10,animTitle),
                     (megaPublish_btn, 'top', 1,publishCam_btn),
                     (importAnim_btn, 'top', 10,sceneTitle),
                     (sep2, 'top', 24,megaPublish_btn),
                     (sceneTitle, 'top', 10,sep2),
                     (importCam_btn, 'top', 10,sceneTitle),
                     (importMat_btn, 'top', 10,sceneTitle),
                     (importAll_btn, 'top', 1,importMat_btn)
                     ],
                     attachPosition=[
                     (sep1, 'right', 0,100),
                     (sep1, 'left', 0,0),
                     (publishAnim_btn, 'right', 0, 50),
                     (publishCam_btn, 'left', 1, 50),
                     (sep2, 'right', 0,100),
                     (sep2, 'left', 0,0),
                     (importCam_btn, 'right', 0, 33),
                     (importAnim_btn, 'right', 0, 66),
                     (importAnim_btn, 'left', 1, 33),
                     (importMat_btn, 'left', 1, 66),
                     (publishModel_btn, 'right', 10, 100)
                     ]
                     )

def LlamaIO():
    workspaceName = 'Llama IO'
    if(cmds.workspaceControl('Llama IO', exists=True)):
        cmds.deleteUI('Llama IO')
    cmds.workspaceControl(workspaceName,initialHeight=100,initialWidth=300,uiScript = 'LlamaIOWindow()')


LlamaIO()

#import installToolbox
#installToolbox.toolbox_install()