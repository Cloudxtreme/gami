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
        self.view.var("description", u"W tym kroku zostanie sprawdzione <b>połączenie z internetem</b> oraz ilość dostępnego miejsca na dysku twardym.<br/><br/><b>Wymagana ilość miejsca:</b> 5 GiB + opcjonalnie 0,5-2 GiB dla pamięci SWAP")

        self.view.var("test.net.passed", u"Komputer jest podłączony do internetu")
        self.view.var("test.net.failed", u"Brak połączenia z internetem")

        self.view.var("test.hd.space.passed", u"Na komputerze jest wystarczająca ilość wolnego miejsca")
        self.view.var("test.hd.space.failed", u"Brak wolnego miejsca na dysku twardym")
        self.view.var("wait", u"Wczytywanie danych...")
        self.view.display()

        self.view.setHarddriveTask(True)
        self.view.setInternetTask(False)

    def reload(self):
        self.view.display()
