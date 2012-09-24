# -*- coding: utf-8 -*-
## Gentoo Advanced and Modular Installer
## Copyleft - Damian Kęska
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import sip
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import gami.gui.qt

class GamiQT:
    """ Class for steps widgets, usage: class GUIInterface(GamiQT) """

    template = dict()

    def QLabelImage(self, img):
        icon = QImage()
        icon.load(img)
        image_label = QLabel(" ")
        image_label.setPixmap(QPixmap.fromImage(icon))

        return image_label

    def var(self, variable, value=None):
        """ Store template values 
            var("test", "any value") # set "test" value to "any value"
            var("test") # get value of "test"
        """

        if value == None:
            if variable in self.template:
                return self.template[variable]
        else:
            self.template[variable] = value
            return True

    def appendLayout(self, TLayStyle):
        """ Append content of step to Gami layout """
        self.app.Content.setLayout(TLayStyle)


class GUIInterface:
    """ QT4 frontend for Gentoo Advanced Modular Installer """

    Gami = None
    window = None
    app = None
    layouts = {'welcome': ''}

    def __init__(self, GamiObject):
        """ Create initial window to put contents of installer to (layout) """

        self.guiPath = str(gami.gui.qt.__path__[0])
        self.Gami = GamiObject
        self.Gami.Gui = self
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setWindowTitle("Instalator systemu Gentoo Linux")

        # styles
        #style = QStyleFactory.create('Cleanlooks')
        #self.app.setStyle(style)

        self.window.setMinimumSize(600, 350)
        self.layout = QVBoxLayout()
        self.layout.setMargin(0)

        # Title layout {
        TLay = QWidget()
        TLay.setAttribute(Qt.WA_TranslucentBackground, True)
        TLay.setStyleSheet("margin: 0; padding: 0; background-color: rgb(20,20,20, 50%);")
        TLay.setMaximumHeight(60)  
        TLay.setMinimumHeight(60)
        

        TLayStyle = QHBoxLayout()
        TLayStyle.setMargin(0)

        self.titleLabel = QLabel(" Trwa wczytywanie instalatora...")

        #TLayStyle.setAttribute(Qt.WA_TranslucentBackground, True)
        TLayStyle.addWidget(self.titleLabel)

        # Separator
        Line = QFrame()
        Line.setGeometry(QRect(10, 70, 351, 16))
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Line.sizePolicy().hasHeightForWidth())
        Line.setSizePolicy(sizePolicy)
        Line.setFrameShape(QFrame.HLine)
        Line.setFrameShadow(QFrame.Sunken)

        TLay.setLayout(TLayStyle)
        # Title layout }

        # Empty space {
        
        self.Content = QContentWidget()

        # Empty Space }
        
        # Down layout {
        HBox = QWidget()
        HBoxLayout = QHBoxLayout()
        HBoxLayout.setSpacing(10)
        HBoxLayout.setMargin(0)

        buttonBack = QPushButton("Wstecz")
        buttonNext = QPushButton("Dalej")

        # Signals
        self.window.connect(buttonBack, SIGNAL("clicked()"), self.Gami.previousStep)
        self.window.connect(buttonNext, SIGNAL("clicked()"), self.Gami.nextStep)

        self.Gami.Hooking.connectHook("Gami.previousStep", self.buttonPrevious)
        self.Gami.Hooking.connectHook("Gami.nextStep", self.buttonNext)

        #buttonBack.setMinimumWidth(50)
        buttonBack.setMaximumWidth(100)
        buttonBack.setMinimumWidth(90)
        buttonBack.setMinimumHeight(45)
        buttonBack.setDisabled(True)

        #buttonNext.setMinimumWidth(50)
        buttonNext.setMaximumWidth(100)
        buttonNext.setMinimumWidth(90)
        buttonNext.setMinimumHeight(45)


        HBoxLayout.addWidget(buttonBack, 1, alignment=Qt.Alignment(2))
        HBoxLayout.addWidget(buttonNext, 0, alignment=Qt.Alignment(2))
        HBox.setLayout(HBoxLayout)
        HBox.setStyleSheet("margin: 4px;")

        # Down layout }

        self.layout.addWidget(TLay, Qt.AlignTop)
        self.layout.addWidget(self.Content, Qt.AlignTop)
        self.layout.addWidget(Line)
        self.layout.addWidget(HBox)

        self.window.setLayout(self.layout)

        # initialize first step
        self.Gami.Hooking.executeHooks(self.Gami.Hooking.getAllHooks("Gami.initStep"))

        self.window.show()

        self.app.exec_()

    def buttonPrevious(self, data=''):
        print("qt.buttonPrevious()")

    def buttonNext(self, layout):
        return self.changeLayout(layout)

    def changeLayout(self, layoutID):
        if os.path.isfile(self.guiPath+"/"+layoutID+".py"):
            exec("import gami.gui.qt."+layoutID)
            exec("self.layouts[layoutID] = gami.gui.qt."+layoutID+".GUIInterface(self)")
            return self.layouts[layoutID]
        else:
            print("Layout not found")
            return False

class QContentWidget(QWidget):
    """ Extended QWidget class with support for replacing layout """

    def setLayout(self, layout):
        self.clearLayout()
        QWidget.setLayout(self, layout)

    def clearLayout(self):
        if self.layout() is not None:
            old_layout = self.layout()
            for i in reversed(range(old_layout.count())):
                old_layout.itemAt(i).widget().setParent(None)
            sip.delete(old_layout)

            
