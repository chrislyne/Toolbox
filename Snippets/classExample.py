import maya.cmds as cmds

class createMyLayoutCls(object):
    def __init__(self, *args):
        pass
    def show(self):
        self.createMyLayout()
    def createMyLayout(self):
        self.window = cmds.window(widthHeight=(1000, 600), title="lalala",   resizeToFitChildren=1)
        cmds.rowLayout("button1, button2, button3", numberOfColumns=5)

        cmds.columnLayout(adjustableColumn=True, columnAlign="center", rowSpacing=10)

        self.button2 = cmds.textFieldButtonGrp(label="LocatorCurve",
                                        text="Please key in your coordinates",
                                        changeCommand=self.edit_curve,
                                        buttonLabel="Execute",
                                        buttonCommand=self.locator_curve)
        cmds.setParent(menu=True)

        cmds.showWindow(self.window)

    def locator_curve(self,*args):
        # Coordinates of the locator-shaped curve.
        crv = cmds.curve(degree=1,
                     point=[(1, 0, 0),
                            (-1, 0, 0),
                            (0, 0, 0),
                            (0, 1, 0),
                            (0, -1, 0),
                            (0, 0, 0),
                            (0, 0, 1),
                            (0, 0, -1),
                            (0, 0, 0)])
        return crv

    def edit_curve(self,*args):
        parts = self.button2.split(",")
        print parts
        txt_val = cmds.textFieldButtonGrp(self.button2, q=True,text=True)
        print txt_val


b_cls = createMyLayoutCls()  
b_cls.show()