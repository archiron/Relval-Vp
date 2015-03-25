#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys,subprocess
import urllib2
import re
from getEnv import env

def self.radio01Clicked(self):
    if self.radio01.isChecked():
        self.QGBox2.setEnabled(False)
        self.QGBox2.setVisible(False)
#        self.label62.setVisible(False) # new
#        self.lineedit3.setVisible(False) # new
        self.choix_etape = 'analyze' # default
        self.choix_calcul = 'Full'
    QtCore.QCoreApplication.processEvents()

