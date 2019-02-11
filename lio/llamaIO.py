import maya.cmds as cmds
import maya.mel as mel


def LlamaIOWindow():
    
    buttonColour = [0.33,0.58,0.74]
    
    installForm = cmds.formLayout(bgc=[0.1,0.4,0.55])

    modelTitle = cmds.text(fn='boldLabelFont',label="Modeling")
    publishModel_btn = cmds.iconTextButton('publishModel_btn',fla=0,hlc=[0,1,1],olc=[0,0,0],st='iconAndTextVertical',i='io_publishModel.svg',bgc=buttonColour,height=50,width=100,label='Publish REF',ann='Select top node to publish',c='from lio.io_publishModel import IO_publishModel_window,PublishModelCheckText;lio.io_publishModel.IO_publishModel(0)')
    cmds.popupMenu( parent='publishModel_btn')
    cmds.menuItem(label='Advanced',c='from lio.io_publishModel import IO_publishModel_window;lio.io_publishModel.IO_publishModel(1)',stp='python')

    sep1t = cmds.separator( hr=1,style='none' ,height=1,backgroundColor=[0.0,0.2,0.35])
    sep1 = cmds.separator( hr=1,style='none' ,height=10,backgroundColor=[0.25,0.25,0.25])
    sep1b = cmds.separator( hr=1,style='none' ,height=1,backgroundColor=[0.4,0.6,0.75])
    
    animTitle = cmds.text(fn='boldLabelFont',label="Animation")
    publishAnim_btn = cmds.iconTextButton('publishAnim_btn',fla=0,st='iconAndTextVertical',i='io_publishAnim.svg',bgc=buttonColour,height=50,width=100,label='Publish Anim',c='from lio.io_publishAnimation import IO_publishAnim_window, runWithUI;lio.io_publishAnimation.IO_publishAnim(0)',stp='python')
    cmds.popupMenu( parent='publishAnim_btn')
    cmds.menuItem(label='Advanced',c='from lio.io_publishAnimation import IO_publishAnim_window, runWithUI;lio.io_publishAnimation.IO_publishAnim(0)',stp='python')
    publishCam_btn = cmds.iconTextButton('publishCam_btn',fla=0,st='iconAndTextVertical',i='io_publishCam.svg',bgc=buttonColour,height=50,width=100,label='Publish Camera',c='from lio.io_publishCamera import io_exportCamera_window, runWithUI;lio.io_publishCamera.io_exportCamera(0)',stp='python')
    cmds.popupMenu( parent='publishCam_btn')
    cmds.menuItem(label='Advanced',c=';from lio.io_publishCamera import io_exportCamera_window, runWithUI;lio.io_publishCamera.io_exportCamera(0)',stp='python')
    megaPublish_btn = cmds.iconTextButton('megaPublish_btn',fla=0,st='iconAndTextVertical',i='io_publishModel.svg',bgc=buttonColour,height=50,width=100,label='Publish to NEW SCENE',c='import io_publishToNewScene;io_publishToNewScene.runExportScripts()',stp='python')
    
    sep2 = cmds.separator( hr=1,style='in' ,height=2)
    
    sceneTitle = cmds.text(fn='boldLabelFont',label="Scene Reconstruction")
    importAnim_btn = cmds.iconTextButton(st='iconAndTextVertical',i='io_importAnim.svg',bgc=buttonColour,height=50,width=100,label='Import Anim',c='lio.io_importAnimation.importAnimation()')
    importCam_btn = cmds.iconTextButton(st='iconAndTextVertical',i='io_importCam.svg',bgc=buttonColour,height=50,width=100,label='Import Camera',c='lio.io_importCamera.importCameraDialog()')
    importMat_btn = cmds.iconTextButton(st='iconAndTextVertical',i='io_importAnim.svg',bgc=buttonColour,height=50,width=100,label='Import Materials',c='lio.io_importMaterials.assignMaterials()')
    importAll_btn = cmds.iconTextButton(en=False,hlc=[1,1,1],st='iconAndTextVertical',i='io_importAnim.svg',bgc=buttonColour,height=50,width=100,label='I\'m Feeling Lucky',c='')
     
    
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
                     (sep1t, 'bottom', 0,sep1),
                     (sep1b, 'top', 0,sep1),
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
                     (sep1t, 'right', 0,100),
                     (sep1t, 'left', 0,0),
                     (sep1, 'right', 0,100),
                     (sep1, 'left', 0,0),
                     (sep1b, 'right', 0,100),
                     (sep1b, 'left', 0,0),
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


#LlamaIO()

#import installToolbox
#installToolbox.toolbox_install()