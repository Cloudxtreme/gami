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
        self.view.var("welcome_label", u"Witaj w instalatorze systemu <b>Gentoo Linux</b>, ten instalator ma za zadanie ułatwić Ci instalację systemu przy pomocy kilku prostych kroków. Jednak pamiętaj, że wymaga on od Ciebie pewnej wiedzy na temat systemów Uniksowych i nie zrobi za Ciebie wszystkiego.<br/><br/><b>Powodzenia!</b><br/><br/>Aby otrzymać pomoc przy instalacji odwiedź nasze forum: <a href=\"http://fastpc.pl\">www.fastpc.pl</a><br/>Zobacz też dokumentację systemu Gentoo Linux: <a href=\"http://www.gentoo.org/doc/pl/index.xml\">http://www.gentoo.org/doc/pl/index.xml</a><br/><br/><img src=\"./usr/share/gami/logo.png\" align=\"right\"/>")
        self.view.display()

    def reload(self):
        self.view.display()
