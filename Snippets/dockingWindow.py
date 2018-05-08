def buildWin():
    WinLayout = cmds.columnLayout( adjustableColumn=True )
    cmds.button( label='Do Nothing' )
    cmds.button( label='Close', command=('cmds.deleteUI(\"' + WorkspaceName + '\" )') )

def dockingIO():
    import maya.cmds as cmds
    WorkspaceName = 'WorkspaceWin1'
    if (cmds.window("WorkspaceWin1", exists=True)):
        cmds.deleteUI("WorkspaceWin1")
    cmds.workspaceControl( WorkspaceName, uiScript = 'buildWin()' )

dockingIO()