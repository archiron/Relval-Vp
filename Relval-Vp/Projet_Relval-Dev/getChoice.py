#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

import os,sys,subprocess

from getEnv import env
from fonctions import cmd_test, liste, cmd_folder_creation, get_collection_list, get_choix_calcul, clean_files, copy_files, cmd_fetch, cmd_relval, cmd_listeRECO, cmd_listeDQM, list_search, explode_item
from fonctions import list_simplify
		
#############################################################################
class GetChoice(QWidget):
 
    def __init__(self, parent=None):
        super(GetChoice, self).__init__(parent)
        self.setWindowTitle("Files choice")
 
        # QHBoxLayout + 2 QGroupBox
#        self.QGBox_H1b = QGroupBox("Release list")
#        self.gbox_H1 = QGridLayout()
#        self.QGBox_H1b.setLayout(self.gbox_H1)
        self.QGBox_H1b = QGroupBox("Release list")
        self.QVL_H1b = QVBoxLayout(self.QGBox_H1b)
        self.QSArea_H1b = QScrollArea()
        self.QSArea_H1b.setWidgetResizable(True)
        self.scrolldwidget1 = QWidget()
        self.gbox_H1 = QGridLayout(self.scrolldwidget1)        
        self.QVL_H1b.addWidget(self.QSArea_H1b)
        self.QSArea_H1b.setWidget(self.scrolldwidget1)
        self.QGBox_H1b.setLayout(self.QVL_H1b)

#        self.QGBox_H2b = QGroupBox("Reference list")
#        self.gbox_H2 = QGridLayout()
#        self.QGBox_H2b.setLayout(self.gbox_H2)
        self.QGBox_H2b = QGroupBox("Reference list")
        self.QVL_H2b = QVBoxLayout(self.QGBox_H2b)
        self.QSArea_H2b = QScrollArea()
        self.QSArea_H2b.setWidgetResizable(True)
        self.scrolldwidget2 = QWidget()
        self.gbox_H2 = QGridLayout(self.scrolldwidget2)        
        self.QVL_H2b.addWidget(self.QSArea_H2b)
        self.QSArea_H2b.setWidget(self.scrolldwidget2)
        self.QGBox_H2b.setLayout(self.QVL_H2b)

        vbox_H0 = QVBoxLayout()
        vbox_H0.addWidget(self.QGBox_H1b)
        vbox_H0.addWidget(self.QGBox_H2b)

        # créer un bouton
        self.bouton = QPushButton("Cancel", self)
        self.bouton.clicked.connect(self.ok_Choice)
        hbox_button = QHBoxLayout()
        hbox_button.addStretch(1)
        hbox_button.addWidget(self.bouton)
        # positionner les widgets dans la fenêtre
        posit = QVBoxLayout()
        posit.addLayout(vbox_H0)
        posit.addLayout(hbox_button)

        self.setLayout(posit)
 
    def ok_Choice(self):
        # emettra un signal "fermeturegetChoice()" avec l'argument cité
#        self.emit(SIGNAL("fermeturegetChoice(PyQt_PyObject)"), unicode(self.lineEdit.text())) 
        self.emit(SIGNAL("fermeturegetChoice(PyQt_PyObject)"), "Au revoir !") 
        # fermer la fenêtre
        self.close()
 
