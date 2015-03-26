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
class GetPublish(QWidget):
 
    def __init__(self, parent=None):
        super(GetPublish, self).__init__(parent)
        self.setWindowTitle("Publish configuration")
 
        # créer un lineEdit
        self.lineEdit = QLineEdit(self)
        self.QGBox_P0 = QGroupBox("Publish configuration")
        self.QGBox_P0.setMinimumWidth(1000)
        vbox_P0 = QVBoxLayout()
        vbox_P0.addWidget(self.lineEdit)
        self.QGBox_P0.setLayout(vbox_P0)
        
        # QHBoxLayout + 2 QGroupBox
        self.QGBox_H1P = QGroupBox("Release ")
        self.gbox_H1P = QGridLayout()
        self.QGBox_H1P.setLayout(self.gbox_H1P)
        self.QGBox_H2P = QGroupBox("Reference ")
        self.gbox_H2P = QGridLayout()
        self.QGBox_H2P.setLayout(self.gbox_H2P)

        hbox_H0_P = QHBoxLayout()
        hbox_H0_P.addWidget(self.QGBox_H1P)
        hbox_H0_P.addWidget(self.QGBox_H2P)

        # créer un bouton
        self.bouton_P = QPushButton("Cancel", self)
        self.bouton_P.clicked.connect(self.ok_Publish)
        hbox_button_P = QHBoxLayout()
        hbox_button_P.addStretch(1)
        hbox_button_P.addWidget(self.bouton_P)
        # positionner les widgets dans la fenêtre
        posit_P = QVBoxLayout()
        posit_P.addWidget(self.QGBox_P0)
        posit_P.addLayout(hbox_H0_P)
        posit_P.addLayout(hbox_button_P)

        self.setLayout(posit_P)
 
    def ok_Publish(self):
        # emettra un signal "fermeturegetPublish()" avec l'argument cité
        self.emit(SIGNAL("fermeturegetPublish(PyQt_PyObject)"), unicode(self.lineEdit.text())) 
        # fermer la fenêtre
        self.close()
 
