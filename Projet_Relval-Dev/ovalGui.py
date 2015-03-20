#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

import os,sys,subprocess

from getEnv import env
from fonctions import cmd_test, liste, cmd_folder_creation, get_collection_list, get_choix_calcul, clean_files, copy_files, cmd_relval, cmd_listeRECO, cmd_listeDQM, list_search, explode_item
		
#############################################################################
class ovalGui(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('DQMGui publish v0.2.0')

        self.cmsenv = env()
        self.texte = self.cmsenv.cmsAll()
        self.choix_calcul = 'Full'   # default
        self.choix_job = '8nh'       # default
        self.choix_etape = 'analyze' # default
		
		# creation du grpe liste des collections
        self.QGBox31 = QGroupBox("Collections")
        self.QGBox31.setVisible(True)
        self.check31 = QCheckBox("Pt10Startup_UP15")
        self.check32 = QCheckBox("Pt35Startup_UP15")
        self.check31.setChecked(True)
        self.check32.setChecked(True)
        qform31 = QFormLayout() # new
        qform31.addRow(self.check31, self.check32) # new
        self.QGBox31.setLayout(qform31) # new
        
		# creation du tableau
        self.toto_list = []
        self.titi_list = []
        for i in range(3):
            print i
            line_1 = str(i) + "G"
            line_2 = str(i) + "M"
            line_3 = str(i) + "D"
            it = [line_1, line_2, line_3]
            self.toto_list.append(it) # toto est en liste de liste
        for i in range(5):
            self.titi_list.append(str(i)) # titi est en string ( int )
        for items in self.toto_list:
            print "toto : ", items
            
        # creation du grpe liste des datas
        self.QGBox32 = QGroupBox("Data Sets")
        self.QGBox32.setMinimumHeight(150)
        self.layout = QGridLayout()
        self.radio01 = QRadioButton("analyze") # Liste par defaut
        self.radio02 = QRadioButton("finalize")
        self.radio03 = QRadioButton("grand")
        self.radio01.setChecked(True)
        self.layout.addWidget(self.radio01, 0, 0)
        self.layout.addWidget(self.radio02, 0, 1)
        self.layout.addWidget(self.radio03, 1, 0, 1, 2)
        
        self.list = QListWidget()
        print self.toto_list
        print self.titi_list
        self.list.addItems(self.titi_list) # ne fonctionne pas si on n'a pas de string
#        self.list.addItems(self.toto_list)
        it = QListWidgetItem(self.list)
        i = 0
        self.bouton = []
        for items in self.titi_list:
            t = QRadioButton(items)
            self.bouton.append(t)
            self.layout.addWidget(self.bouton[i])
            self.connect(self.bouton[i], SIGNAL("clicked()"), self.boutonClicked)
            i +=1
        self.QGBox32.setLayout(self.layout)
        
        #Layout intermédiaire : création et peuplement des gpes radios
        self.layoutH_radio = QHBoxLayout()
        self.layoutH_radio.addWidget(self.QGBox31)
#        self.layoutH_radio.addStretch(1)
        self.layoutH_radio.addWidget(self.QGBox32)

		# creation du label resumé
        self.labelResume = QLabel(self.trUtf8(self.texte), self)
		# creation du grpe Folders paths
        self.QGBox8 = QGroupBox("Folders paths")
        vbox8 = QVBoxLayout()
        vbox8.addWidget(self.labelResume)
        self.QGBox8.setLayout(vbox8)

        # Création du bouton quitter, ayant pour parent la "fenetre"
        self.boutonQ = QPushButton(self.trUtf8("Quitter ?"),self)
        self.boutonQ.setFont(QFont("Comic Sans MS", 14,QFont.Bold,True))
        self.boutonQ.setIcon(QIcon("../images/smile.png"))
        self.connect(self.boutonQ, SIGNAL("clicked()"), qApp, SLOT("quit()"))

        #Layout intermédiaire : boutons
        self.layoutH_boutons = QHBoxLayout()
        self.layoutH_boutons.addStretch(1)
        self.layoutH_boutons.addWidget(self.boutonQ)

        #Layout intermédiaire : ComboBox + labelcombo
        self.layoutV_combobox = QVBoxLayout()
        self.layoutV_combobox.addWidget(self.QGBox8)
        
        # creation des onglets
        self.onglets = QTabWidget()
        self.generalTab = QWidget()
        self.onglets.insertTab(0, self.generalTab, "General")
        #Set Layout for Tabs Pages
        self.generalTab.setLayout(self.layoutV_combobox)   

        #Layout principal : création et peuplement
        self.layout_general = QVBoxLayout()
        self.layout_general.addLayout(self.layoutH_radio)
        self.layout_general.addWidget(self.onglets)
        self.layout_general.addLayout(self.layoutH_boutons)
        self.setLayout(self.layout_general)
        
    def boutonClicked(self):
#        if self.radio21.isChecked():
#            self.choix_etape = 'store'
        i = 0
        for items in self.titi_list:
            print self.bouton[i].text()
            if self.bouton[i].isChecked():
                print "checked"
            i += 1
        QtCore.QCoreApplication.processEvents()

       