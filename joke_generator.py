from maya import cmds

from PySide2 import QtCore, QtWidgets

import maya.OpenMayaUI as omui
import sys
import time
import shiboken2 as shiboken

import requests

class MyEventHandler(QtCore.QObject):
    def __init__(self):
        cmds.inViewMessage(hide=False)
        super(MyEventHandler, self).__init__()
        cmds.setFocus("outlinerPanel1")
        self.count = 1
        self.joke = None
        
        # first joke appears unprompted
        self.newJoke()
        
        cmds.inViewMessage(amg=f'<hl>{self.joke[0]}</hl>.', pos='midCenterTop', dragKill=True )
        

    def newJoke(self):
        r = requests.get(
            'https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=twopart&contains=%3F')
        joke = r.json()
        setup = joke['setup']
        delivery = joke['delivery']
        self.joke = (setup, delivery)

    def eventFilter(self, qobj, event):
        if event.type() == event.KeyPress:

            key = event.key()

            if (key == QtCore.Qt.Key_Left
                or key == QtCore.Qt.Key_Up
                or key == QtCore.Qt.Key_Right
                or key == QtCore.Qt.Key_Down
            ):

                if self.count == 0:
                    self.newJoke()
                    cmds.inViewMessage(amg=f'<hl>{self.joke[0]}</hl>.', pos='midCenterTop', dragKill=True)
                elif self.count == 1:
                    cmds.inViewMessage(amg=f'<hl style="color: #A2CCE0;">{self.joke[1]}</hl>.', pos='midCenter', dragKill=True)
                else:
                    if self.count%2 == 0:
                        cmds.inViewMessage(clear='midCenter')
                        self.newJoke()
                        cmds.inViewMessage(amg=f'<hl>{self.joke[0]}</hl>.', pos='midCenterTop', dragKill=True)
                    else:
                        cmds.inViewMessage(amg=f'<hl style="color: #A2CCE0;">{self.joke[1]}</hl>.', pos='midCenter', dragKill=True)

                self.count += 1

            try:
                if (
                        key == QtCore.Qt.Key_Escape
                        or key == QtCore.Qt.Key_Enter
                        or key == QtCore.Qt.Key_Return
                        or key == 16777216
                    ): # QtCore.Qt.Key_Escape is a value that equates to what the operating system passes to python from the keyboard when the escape key is pressed.
                    cmds.inViewMessage(clear='midCenterTop')
                    cmds.inViewMessage(clear='midCenter')
                    qobj.removeEventFilter(self)
            except AttributeError:
                pass
        return super(MyEventHandler, self).eventFilter(qobj, event)

def get_maya_main_window():
    pointer = omui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(int(pointer), QtWidgets.QWidget)


handler = MyEventHandler()
maya_window = get_maya_main_window()
maya_window.installEventFilter(handler)
