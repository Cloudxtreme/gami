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

import gami.core

class GamiStep(gami.core.GamiStepTemplate):
    def initialize(self):
        self.view.var("description", u"W tym kroku zostanie sprawdzione połączenie z internetem oraz ilość dostępnego miejsca na dysku twardym.")
        print("View:")
        print self.view
        self.view.display()

    def reload(self):
        self.view.display()
