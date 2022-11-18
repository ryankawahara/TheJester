from maya import cmds
from Qt import QtCore, QtWidgets
import maya.OpenMayaUI as omui
import shiboken2 as shiboken
import sys
import time


import requests


class MyEventHandler(QtCore.QObject):
    def __init__(self):
        super(MyEventHandler, self).__init__()
        self.count=0
        self.joke = None
        self.newJoke()
        print(self.joke[0])
        cmds.inViewMessage(amg=f'<hl>{self.joke[0]}</hl>.', pos='midCenter', dragKill=True )

        self.count+=1

    def newJoke(self):
        r = requests.get(
            'https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=twopart&contains=%3F')
        joke = r.json()
        setup = joke['setup']
        delivery = joke['delivery']
        self.joke = (setup, delivery)
    def eventFilter(self, qobj, event):
        if event.type() == event.KeyPress:
            print(self.count)

            if self.count == 0:
                self.newJoke()
                # self.count+=1
                print(self.joke[0])
            elif self.count == 1:
                print(self.joke[1])
            else:
                if self.count%2 == 0:
                    self.newJoke()
                    print(self.joke[0])
                else:
                    print(self.joke[1])
            if event.key() == QtCore.Qt.Key_Escape: # QtCore.Qt.Key_Escape is a value that equates to what the operating system passes to python from the keyboard when the escape key is pressed.
                # Yes: Close the window
                qobj.removeEventFilter(self)
            # print(setup)
            # time.sleep(5)
            # print(delivery)

            self.count+=1
        return super(MyEventHandler, self).eventFilter(qobj, event)

def get_maya_main_window():
    # store the memory address for the main maya window
    pointer = omui.MQtUtil.mainWindow()
    # return shiboken.wrapInstance(long(pointer), QtWidgets.QWidget) # long has been dropped in python 3.0
    return shiboken.wrapInstance(int(pointer), QtWidgets.QWidget)

# flag = False
# print(joke['setup'])
# r = requests.get('https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=twopart&contains=%3F')
# joke = r.json()
# print(joke['setup'])
# setup = joke['setup']
# delivery = joke['delivery']


handler = MyEventHandler()
maya_window = get_maya_main_window()
maya_window.installEventFilter(handler)





# cmds.inViewMessage(amg='<hl>Selected item is not a reference node.</hl>.', pos='midCenter', dragKill=True )
# print(r.json())