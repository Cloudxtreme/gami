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
        label = QLabel(self.var("welcome_label"))
        label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        label.setWordWrap(True)

        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        label.setSizePolicy(sizePolicy)

        self.content = QVBoxLayout()
        self.content.setSizeConstraint(QLayout.SetMaximumSize)
        self.content.addWidget(label, Qt.AlignTop)
        #self.content.addItem(QSpacerItem(10, 50, QSizePolicy.Expanding, QSizePolicy.Minimum))
        #self.app.Content.setStyleSheet("text-align: top; background-color: red;")

    def display(self):
        self.build()
        self.appendLayout(self.content)
        self.app.titleLabel.setText(" Wprowadzenie")
