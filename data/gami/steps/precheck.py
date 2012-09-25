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
import os
import urllib2

class GamiStep(gami.core.GamiStepTemplate):
    def initialize(self):
        # for this step we need to resize the window a little bit
        self.app.Gui.window.setMinimumSize(800, 400)

        self.view.var("description", u"W tym kroku zostanie sprawdzione <b>połączenie z internetem</b> oraz ilość dostępnego miejsca na dysku twardym.<br/><br/><b>Wymagana ilość miejsca:</b> 5 GiB + opcjonalnie 0,5-2 GiB dla pamięci SWAP")

        self.view.var("test.net.passed", u"Komputer jest podłączony do internetu")
        self.view.var("test.net.failed", u"Brak połączenia z internetem")

        self.view.var("test.hd.space.passed", u"Na komputerze jest wystarczająca ilość wolnego miejsca")
        self.view.var("test.hd.space.failed", u"Brak wolnego miejsca na dysku twardym")

        self.view.var("test.root.passed", u"Instalator jest uruchomiony z odpowiednimi uprawnieniami")
        self.view.var("test.root.failed", u"Wymagane jest uruchomienie ponowne instalatora z uprawnieniami konta root")
        self.view.var("wait", u"Wczytywanie danych...")
        self.reload()

    def reload(self):
        self.view.display()

        hd = self.checkRequiredSpace()
        net = self.checkConnection()
        root = self.checkPrivileges()

        self.view.setHarddriveTask(hd)
        self.view.setInternetTask(net)
        self.view.setRootTask(root)

        if hd == False or net == False or root == False:
            self.app.Gui.nextButtonState(False)
        else:
            self.app.Gui.nextButtonState(True)
        

    def checkRequiredSpace(self):
        """ Check required disk space """

        try:
            required = int(self.app.Storage.get("required_space")) # Get required space information from storage

            devices = self.app.Partman.getAllDevices(physical=True) # only psyhical devices

            for device in devices:
                if self.app.Partman.getDeviceSize(device, "MB") > required:
                    return True
        except gami.core.partman.PartmanException as e:
            print("Cannot access partition, not a root?")
            return False

        return False

    def checkPrivileges(self):
        """ Check if user is root """

        if not os.environ['USER'] == "root":
            return False

        return True

    def checkConnection(self):
        """ Check internet connection """

        try:
            response=urllib2.urlopen('http://google.com',timeout=1)
            return True
        except urllib2.URLError:
            return False

