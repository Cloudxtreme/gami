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

import parted
import re
import subprocess
import os

class PartmanException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

class Partman:
    """ Parted interface """

    def getAllDevices(self, physical=False):
        """ Get all devices eg. /dev/sda, /dev/sda1, /dev/sdb, /dev/sdb1, /dev/sdb2 and return in a list format. physical=True|False - show only physical devices instead of partitions? """

        try:
            fdiskOutput = subprocess.check_output(["fdisk", "-l"]) # get "fdisk -l" output
            allDisks = re.findall("\/dev\/([A-Za-z0-9]+)", fdiskOutput)
        except Exception as e:
            raise PartmanException("Cannot access fdisk, "+str(e)+", maybe not a root?")

        ret = list()

        for device in allDisks:
            isPartition = True

            try:
                n = int(device[-1:])
            except Exception:
                isPartition = False

            # list only physical drives like /dev/sda or /dev/sdb not partitions like /dev/sda
            if isPartition == True and physical == True:
                continue

            ret.append("/dev/"+device)

        return ret

    def getDeviceSize(self, devPath, unit="MB"):
        """ Get device size and return in specified unit (B, MB, GB etc.) example: getDeviceSize("/dev/sda", unit="MB") """

        if not os.path.exists(devPath):
            raise PartmanException("No such file or directory while trying to open "+str(devPath))

        if not devPath[0:5] == "/dev/":
            raise PartmanException("File is outside of /dev directory, cancelling.")

        size = False

        try:
            dev = parted.device.Device(devPath)
            size = dev.getSize(unit)
        except Exception as e:
            raise PartmanException("parted reported error: "+str(e))

        return size

            
