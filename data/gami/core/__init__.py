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

import os, sys, gettext
import gami
from gami.core.utils import *
from gami.core.storage import *
from gami.core.partman import *

if sys.version_info[0] >= 3:
    import configparser
else:
    import ConfigParser as configparser

class Gami:
    """ Gentoo Advanced and Modular Installer core logic class """

    # private variables
    _modules = dict()
    _steps = dict()

    # interface
    Config = None
    Hooking = None
    Logging = None
    Storage = None
    Gui = None


    def __init__(self, args=''):
        # args will be parsed to determinate to load sqlite3 base or create new and put it in to memory
        # ...blah blah blah...
        
        # parse configuration file
        self.Config = ConfigManager()
        self.Logging = Logging(self)
        self.Hooking = Hooking(self)
        self.Storage = Storage()
        self.Partman = Partman()
        self.corePath = gami.core.__path__[0]

        #print("Testing storage:")
        #self.Storage.set('stage', '1')
        #print self.Storage.get('stage')
        #self.Storage.set('stage', '2')
        #print self.Storage.get('stage')

        # Default test configuration
        self.Storage.set("required_space", "6000") # in mbytes

        self.Hooking.connectHook("Gami.initStep", self.initStep)

    def initStep(self, a=''):
        stage = self.Storage.getStageById(1)
        name = str(stage['name'])

        items = self.Hooking.getAllHooks("Gami.nextStep")
        data = ""

        for item in items:
            if "gami.gui" in str(item.im_class):
                data = item(name)

        self.setStep(name, data)

    def setStep(self, stepID, data):
        """ Sets current step """

        if stepID in self._steps:
            return self._steps[stepID].reload()

        if os.path.isfile(self.corePath.replace("/core", "/steps")+"/"+stepID+".py"):
            exec("import gami.steps."+stepID)
            exec("self._steps[stepID] = gami.steps."+stepID+".GamiStep(self, data)")
            return self._steps[stepID]
            

    def nextStep(self):
        nextStage = self.Storage.getCurrentStage()+1 # next stage
        allStages = self.Storage.countStages() # get all stages

        if nextStage > allStages:
            return False

        stage = self.Storage.getStageById(nextStage)
        stageName = str(stage['name'])        


        items = self.Hooking.getAllHooks("Gami.nextStep")
        data = ""

        for item in items:
            if "gami.gui" in str(item.im_class):
                data = item(stageName)

        self.setStep(stageName, data)

    def previousStep(self):
        self.Hooking.executeHooks(self.Hooking.getAllHooks("Gami.previousStep"))
        print("Gami.previousStep()")


class GamiStepTemplate:
    view = None
    app = None

    def __init__(self, app, guiTemplate):
        self.view = guiTemplate # view
        self.app = app # front controler (like in MVC but its not a MVC)
        self.initialize() # custom init required
