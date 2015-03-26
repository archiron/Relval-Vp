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
 
        # créer un lineEdit
        self.lineEdit = QLineEdit(self)
        self.QGBox_0 = QGroupBox("Files list")
        self.QGBox_0.setMinimumWidth(1000)
        vbox_0 = QVBoxLayout()
        vbox_0.addWidget(self.lineEdit)
        self.QGBox_0.setLayout(vbox_0)
        
        # QHBoxLayout + 2 QGroupBox
        self.QGBox_H1 = QGroupBox("Release list")
        self.TextEdit_H1 = QTextEdit(self)
        self.TextEdit_H1.append("Coucou ! \n")
        vbox_H1 = QVBoxLayout()
        vbox_H1.addWidget(self.TextEdit_H1)
        self.QGBox_H1.setLayout(vbox_H1)
        self.QGBox_H2 = QGroupBox("Reference list")
        self.TextEdit_H2 = QTextEdit(self)
        self.TextEdit_H2.append("Coucou ! \n")
        vbox_H2 = QVBoxLayout()
        vbox_H2.addWidget(self.TextEdit_H2)
        self.QGBox_H2.setLayout(vbox_H2)
        
        self.QGBox_H1b = QGroupBox("Release list b")
        self.gbox_H1 = QGridLayout()
        self.QGBox_H1b.setLayout(self.gbox_H1)
        self.QGBox_H2b = QGroupBox("Reference list b")
        self.gbox_H2 = QGridLayout()
        self.QGBox_H2b.setLayout(self.gbox_H2)

        vbox_H0 = QVBoxLayout()
        vbox_H0.addWidget(self.QGBox_H1)
        vbox_H0.addWidget(self.QGBox_H1b)
        vbox_H0.addWidget(self.QGBox_H2)
        vbox_H0.addWidget(self.QGBox_H2b)

        # créer un bouton
        self.bouton = QPushButton("Cancel", self)
        self.bouton.clicked.connect(self.ok_Choice)
        hbox_button = QHBoxLayout()
        hbox_button.addStretch(1)
        hbox_button.addWidget(self.bouton)
        # positionner les widgets dans la fenêtre
        posit = QVBoxLayout()
        posit.addWidget(self.QGBox_0)
        posit.addLayout(vbox_H0)
        posit.addLayout(hbox_button)

        self.setLayout(posit)
 
    def ok_Choice(self):
        # emettra un signal "fermeturegetChoice()" avec l'argument cité
        self.emit(SIGNAL("fermeturegetChoice(PyQt_PyObject)"), unicode(self.lineEdit.text())) 
        # fermer la fenêtre
        self.close()
 
