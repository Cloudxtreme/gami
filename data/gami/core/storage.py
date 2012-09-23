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

import sqlite3

class MySum:
    def __init__(self):
        self.count = 0

    def step(self, value):
        self.count += value

    def finalize(self):
        return self.count

class Storage:
    """ Internal database to store eg. keys, datas - uses SQLite3 """

    # SQLite stuff
    socket = None
    cursor = None
    sql = None
    Type = "SQLite3"
    Stage = 1

    def dict_factory(self, cursor, row):
        """ Put results to dictionary """

        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __init__(self, databaseDir=':memory:'):
        self.socket = sqlite3.connect(databaseDir, check_same_thread = False)

        # MySQL-like results
        self.socket.create_aggregate("mysum", 1, MySum)
        self.socket.row_factory = self.dict_factory

        self.socket.isolation_level = None
        self.cursor = self.socket.cursor()

        # new database must be built
        self.buildStructure()
        self.addStage("welcome", 1)
        self.addStage("precheck", 2)


    def buildStructure(self):
        """ Create tables """

        # Installer stages (eg. welcome, selecting locale and language, managing disk space, compiling kernel)
        self.cursor.execute("CREATE TABLE `stages` (id int(2) primary key, passed int(1), data text, name varchar(60));")

        # Fast and small storage up to 2048 bytes for single key
        self.cursor.execute("CREATE TABLE `storage` (keyname varchar(60) primary key, value varchar(2024));")


    # `stages`
    def addStage(self, name, id):
        self.cursor.execute("INSERT INTO `stages` (id, passed, name, data) VALUES ('"+str(int(id))+"', 0, '"+str(name)+"', '');")
        return True

    def passStage(self, id):
        self.cursor.execute("UPDATE `stages` SET passed=1 WHERE id='"+str(int(id))+"';")
        return True

    def getCurrentStage(self):
        return self.Stage

    def setCurrentStage(self, id):
        self.Stage = int(id)
        return True

    def countStages(self):
        query = self.cursor.execute("SELECT id FROM `stages`")
        a = query.fetchall()

        return len(a)


    def getStageById(self, id):
        query = self.cursor.execute("SELECT * FROM `stages` WHERE id='"+str(int(id))+"';")
        results = query.fetchone()

        return results

    # `storage`

    def get(self, key):
        """ Returns `value` from `storage` table """

        query = self.cursor.execute("SELECT value FROM `storage` WHERE keyname='"+key+"';")
        results = query.fetchone()

        if results:
            return results['value']

    def set(self, key, value):
        """ Set storage `value` in `storage` table. Returns True if key was created first time and None if it was just updated. """

        # if key does not exists
        if self.get(key) is None:
            self.cursor.execute("INSERT INTO `storage` (keyname, value) VALUES ('"+str(key)+"', '"+str(value)+"');")
            return True
        else:
            self.cursor.execute("UPDATE `storage` SET value='"+str(value)+"' WHERE keyname='"+str(key)+"';")
        


