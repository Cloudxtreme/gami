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

from time import strftime, localtime
from StringIO import StringIO
from collections import defaultdict
import logging, traceback, inspect

class Hooking:
    """ Hooking library """

    Hooks = defaultdict(list) # list of all hooks
    Logging = None

    def __init__(self, Parent=None):
        """ Initialize Hooking library, check Logging class if present """

        self.Parent = Parent


    def connectHook(self, name, method):
        """ Connect to hook's socket """
        self.Hooks[name].append(method)

    def removeHook(self, name, method):
        if not name in self.Hooks:
            return True

        self.Hooks[name].remove(method)

        if not self.Hooks[name]:
            del self.Hooks[name]

        return True 

    def getAllHooks(self, name):
        """ Get all hooked methods to execute them """
        return self.Hooks.get(name, False)


    def executeHooks(self, hooks, data=True):
        """ Executes all functions from list. Takes self.getAllHooks as hooks """

        if hooks:
            for Hook in hooks:
                try:
                    data = Hook(data)
                except Exception as e:
                    buffer = StringIO()
                    traceback.print_exc(file=buffer)

                    if self.Parent is not None:
                        self.Parent.Logging.output(buffer.getvalue(), "error", savetoLogs=True, execHook=False, skipDate=False) # Logging class support
                    else:
                        print(buffer.getvalue())

        return data    

class Logging:
    """ Simple logger with stack tracking, saving to file, gettext and priority support """

    logger = None

    # -1 = Don't log any messages even important too
    # 0 = Don't log any messages, only if important (critical errors)
    # 1 = Log everything but debugging messages
    # 2 = Debug messages

    loggingLevel = 1 
    session = ""
    parent = None
    app = "gami"
    logFile = "/tmp/gami.log"

    def __init__(self, Parent):
        self.parent = Parent
        self.initializeLogger()

    def convertMessage(self, message, stackPosition):
        return strftime("%d/%m/%Y %H:%M:%S", localtime())+", "+stackPosition+": "+message

    def initializeLogger(self):
        try:
            self.logger = logging.getLogger(self.app)
            handler = logging.FileHandler(self.logFile)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
            return True
        except Exception as e:
            self.logger = None
            print("Cannot get access "+self.logFile+", check your permissions")
        return False

    def turnOffLogger(self):
        self.logger = None
        return True

    def output(self, message, utype='', savetoLogs=True, execHook=True, skipDate=False):
        """ Output to log file and to console """

        if not skipDate:
            message = self.convertMessage(message, inspect.stack()[1][3])
        
        if utype == "debug" and self.loggingLevel > 1:
            if self.logger is not None and savetoLogs:
                self.logger.debug(message)

            print(message)

        elif utype == "" and self.loggingLevel > 0:
            if self.logger is not None and savetoLogs:
                self.logger.info(message)

            print(message)

        elif utype == "warning" and self.loggingLevel > 0:
            if self.logger is not None and savetoLogs:
                self.logger.warning(message)

            print(message)

        elif utype == "critical" and self.loggingLevel > -1:
            if self.logger is not None and savetoLogs:
                self.logger.critical(message)

            print(message)

        # save all messages to show in messages console
        self.session += message + "\n"

        # update console for example
        try:
            Hooks = self.parent.Hooking.getAllHooks("onLogChange")

            if Hooks:
                self.parent.Hooking.executeHooks(Hooks, self.session)

        except Exception as e:
            if execHook:
                self.parent.Logging.output(self.parent._("Error")+": "+self.parent._("Cannot execute hook")+"; onLogChange; "+str(e), "warning", True, False)
            else:
                print(self.parent._("Error")+": "+self.parent._("Cannot execute hook")+"; onLogChange; "+str(e))

class ConfigManager:
    def parseConfig(self, configPath=None):
        """ Parse configuration file - default is in /etc/gami/gami.conf but can be specified in first argument configPath """
        
        if configPath is None:
            configPath = '/etc/gami/gami.conf'

        if os.path.isfile(configPath):
            Parser = configparser.ConfigParser()

            try:
                Parser.read(configPath)
            except Exception as e:
                print("Cannot load configuration file, exiting...")
                sys.exit(os.EX_CONFIG)
        else:
            print("Cannot load configuration file - file not found, exiting...")
            sys.exit(os.EX_CONFIG)
