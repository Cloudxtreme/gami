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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import gami.gui.qt

class GUIInterface(gami.gui.qt.GamiQT):
    """ View interface in QT4 for welcome page """

    app = None

    def __init__(self, app):
        self.app = app
        self.build()

    def build(self):
        label = QLabel(self.var("description"))
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        label.setSizePolicy(sizePolicy)

        ### Grid layout
        grid = QGridLayout()
        grid.setHorizontalSpacing(0)
        grid.setSizeConstraint(QLayout.SetMaximumSize)
        gridWidget = QWidget()
        gridWidget.setLayout(grid)

        ### Network task
        #icon = QIcon().fromTheme("dialog-error")
        self.ntaskImage = QLabel(" ")
        self.ntaskImage.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.ntaskImage.setPixmap(QIcon().fromTheme("task-recurring").pixmap(50))
        self.ntask = QLabel(self.var("wait"))

        ### Harddisk task
        #icon = QIcon().fromTheme("dialog-error")
        self.htaskImage = QLabel(" ")
        self.htaskImage.setPixmap(QIcon().fromTheme("task-recurring").pixmap(50))
        self.htask = QLabel(self.var("wait"))


        self.content = QVBoxLayout()
        self.content.addWidget(label, Qt.AlignTop)
        self.content.addWidget(gridWidget, Qt.AlignTop)
        self.content.setSizeConstraint(QLayout.SetMinimumSize)
        grid.addWidget(self.ntaskImage, 1, 1, 1, 1)
        grid.addWidget(self.ntask, 1, 2, 1, 3)
        grid.addWidget(self.htaskImage, 2, 1, 4, 1)
        grid.addWidget(self.htask, 2, 2, 4, 1)

        #self.content.addWidget(image_label, Qt.AlignTop)
        #self.content.addItem(QSpacerItem(10, 50, QSizePolicy.Expanding, QSizePolicy.Minimum))
        #self.app.Content.setStyleSheet("text-align: top; background-color: red;")

    def setHarddriveTask(self, value):
        """ Set harddrive status """

        if value == True:
            self.htask.setText(self.var("test.hd.space.passed"))
            self.htaskImage.setPixmap(QIcon().fromTheme("task-accepted").pixmap(50))
        else:
            self.htask.setText(self.var("test.hd.space.failed"))
            self.htaskImage.setPixmap(QIcon().fromTheme("dialog-error").pixmap(50))

    def setInternetTask(self, value):
        """ Set internet connection status """

        if value == True:
            self.ntask.setText(self.var("test.net.passed"))
            self.ntaskImage.setPixmap(QIcon().fromTheme("task-accepted").pixmap(50))
        else:
            self.ntask.setText(self.var("test.net.failed"))
            self.ntaskImage.setPixmap(QIcon().fromTheme("dialog-error").pixmap(50))
            

    def display(self):
        self.build()
        self.appendLayout(self.content)
        self.app.titleLabel.setText(u" Sprawdzanie połączenia internetowego i przestrzeni dyskowej")
