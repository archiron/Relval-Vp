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
 
        self.text_ext = "_dev" # default
        self.to_transmit = []
        self.transmit_rel = ""
        self.transmit_ref = ""
        self.miniAOD = False
        self.pmx = False

        # créer un lineEdit
        self.label01 = QLabel("Web folder customization : ", self)
        self.label01.setMaximumWidth(150)
        self.label01.setMinimumWidth(150)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setMaximumWidth(300)
        self.lineEdit.connect(self.lineEdit, SIGNAL("textChanged(QString)"), self.changeText)
        self.QGBox_P0 = QGroupBox("Publish configuration")
        hbox_P0 = QHBoxLayout()
        hbox_P0.addWidget(self.label01)
        hbox_P0.addWidget(self.lineEdit)
        hbox_P0.addStretch(1)
        self.QGBox_P0.setLayout(hbox_P0)

		# creation du grpe FastSim
        self.labelFastSim = QLabel("FastvsFull Tag : ", self)
        self.labelFastSim.setMaximumWidth(150)
        self.labelFastSim.setMinimumWidth(150)
        self.lineEditFastSim = QLineEdit(self)
        self.lineEditFastSim.setMinimumWidth(500)
#        self.lineEditFastSim.connect(self.lineEdit, SIGNAL("textChanged(QString)"), self.changeTextFastSim)
        self.QGBoxFastSim_P = QGroupBox("FastSim")
        hboxFastSim_P = QHBoxLayout()
        hboxFastSim_P.addWidget(self.labelFastSim)
        hboxFastSim_P.addWidget(self.lineEditFastSim)
        hboxFastSim_P.addStretch(1)
        self.QGBoxFastSim_P.setLayout(hboxFastSim_P)
        
        # QHBoxLayout + 2 QGroupBox
        self.QGBox_H1P = QGroupBox("Release ")
        self.gbox_H1P = QVBoxLayout()
        self.QGBox_H1P.setLayout(self.gbox_H1P)
        self.t_rel = QLabel('release : ' )
        self.gbox_H1P.addWidget(self.t_rel) 
        self.test_new = QLabel('test new : ' )
        self.gbox_H1P.addWidget(self.test_new) 
        self.gbox_H1P.addStretch(1)
        self.QGBox_H2P = QGroupBox("Reference ")
        self.gbox_H2P = QVBoxLayout()
        self.t_ref = QLabel('reference : ' )
        self.gbox_H2P.addWidget(self.t_ref) 
        self.test_ref = QLabel('test ref : ' )
        self.gbox_H2P.addWidget(self.test_ref) 
        self.gbox_H2P.addStretch(1)
        self.QGBox_H2P.setLayout(self.gbox_H2P)

		# creation du grpe local/external
        self.QGBox2_P = QGroupBox("local/external")
        self.QGBox2_P.setMaximumHeight(150)
        self.QGBox2_P.setMinimumHeight(150)
        self.QGBox2_P.setMaximumWidth(100)		
        self.radio21_P = QRadioButton("local") # par defaut
        self.radio22_P = QRadioButton("non local")
        self.radio22_P.setChecked(True)
        self.connect(self.radio21_P, SIGNAL("clicked()"), self.radio21_PClicked)
        self.connect(self.radio22_P, SIGNAL("clicked()"), self.radio22_PClicked)
        vbox2_P = QVBoxLayout()
        vbox2_P.addWidget(self.radio21_P)
        vbox2_P.addWidget(self.radio22_P)
        vbox2_P.addStretch(1)
        self.QGBox2_P.setLayout(vbox2_P)
				
		# creation du grpe std/dev
        self.QGBox4_P = QGroupBox("std/dev")
        self.QGBox4_P.setMaximumHeight(150)
        self.QGBox4_P.setMinimumHeight(150)
        self.QGBox4_P.setMaximumWidth(100)		
        self.radio41_P = QRadioButton("std")
        self.radio42_P = QRadioButton("dev") # par defaut
        self.radio42_P.setChecked(True)
        self.connect(self.radio41_P, SIGNAL("clicked()"), self.radio41_PClicked)
        self.connect(self.radio42_P, SIGNAL("clicked()"), self.radio42_PClicked)
        vbox4_P = QVBoxLayout()
        vbox4_P.addWidget(self.radio41_P)
        vbox4_P.addWidget(self.radio42_P)
        vbox4_P.addStretch(1)
        self.QGBox4_P.setLayout(vbox4_P)
				
		# creation du grpe OvalFile
        self.QGBox3_P = QGroupBox("OvalFile")
        self.QGBox3_P.setMaximumHeight(150)
        self.QGBox3_P.setMinimumHeight(150)
        self.vbox3_P = QVBoxLayout()
        self.t_rel_default = QLabel("Default web folder name : " )
        self.vbox3_P.addWidget(self.t_rel_default)
        self.tag_startup = QLabel("Tag Startup : " )
        self.vbox3_P.addWidget(self.tag_startup)
        self.data_version = QLabel("Data Version : " )
        self.vbox3_P.addWidget(self.data_version)
        self.vbox3_P.addStretch(1)
        self.QGBox3_P.setLayout(self.vbox3_P)

        hbox_H0_P = QHBoxLayout()
        hbox_H0_P.addWidget(self.QGBox_H1P)
        hbox_H0_P.addWidget(self.QGBox_H2P)
        hbox_H0_P.addWidget(self.QGBox2_P)
        hbox_H0_P.addWidget(self.QGBox4_P)
        hbox_H0_P.addWidget(self.QGBox3_P)

        # créer un bouton
        self.bouton_P = QPushButton("Cancel", self)
        self.bouton_P.clicked.connect(self.ok_Publish)
        hbox_button_P = QHBoxLayout()
        hbox_button_P.addStretch(1)
        hbox_button_P.addWidget(self.bouton_P)
        # positionner les widgets dans la fenêtre
        posit_P = QVBoxLayout()
        posit_P.addWidget(self.QGBox_P0)
        posit_P.addWidget(self.QGBoxFastSim_P)
        posit_P.addLayout(hbox_H0_P)
        posit_P.addLayout(hbox_button_P)

        self.setLayout(posit_P)
 
    def ok_Publish(self):
        QtCore.QCoreApplication.processEvents()
        # emettra un signal "fermeturegetPublish()" avec l'argument cité
        self.emit(SIGNAL("fermeturegetPublish(PyQt_PyObject)"), '_' + unicode(self.lineEdit.text()) + ':' + unicode(self.lineEditFastSim.text()) ) 
        # fermer la fenêtre
        self.close()

    def radio21_PClicked(self): # to be removed ?
        if self.radio21_P.isChecked():
            print 'local'
        QtCore.QCoreApplication.processEvents()

    def radio22_PClicked(self): # to be removed ?
        if self.radio22_P.isChecked():
            print 'external'
        QtCore.QCoreApplication.processEvents()
        
    def radio41_PClicked(self):
        if self.radio41_P.isChecked():
            self.text_ext = "_DQM_std"
            if self.miniAOD:
                self.text_ext = "_miniAOD" + self.text_ext 
            if self.pmx:
                self.text_ext = "_pmx" + self.text_ext 
            self.t_rel_default.setText("Default web folder name : " + self.transmit_rel[6:] + self.text_ext)
        QtCore.QCoreApplication.processEvents()

    def radio42_PClicked(self):
        if self.radio42_P.isChecked():
            self.text_ext = "_dev"
            if self.miniAOD:
                self.text_ext = "_miniAOD" + self.text_ext 
            if self.pmx:
                self.text_ext = "_pmx" + self.text_ext 
            self.t_rel_default.setText("Default web folder name : " + self.transmit_rel[6:] + self.text_ext)
        QtCore.QCoreApplication.processEvents()

    def changeText(self):
        temp = '_' + unicode(self.lineEdit.text())
        self.t_rel_default.setText("Default web folder name : " + self.transmit_rel[6:] + temp + self.text_ext)        
        
#    def changeTextFastSim(self):
        #temp = '_' + unicode(self.lineEditFastSim.text())
        #self.t_rel_default.setText("Default web folder name : " + self.transmit_rel[6:] + temp + self.text_ext)        
        
